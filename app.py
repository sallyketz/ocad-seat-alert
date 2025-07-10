from flask import Flask, request, render_template, jsonify
import os
import json
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from ocad_api import get_token_and_session, search_courses, get_sections, get_section_details
from email_config import SMTP_EMAIL, SMTP_PASSWORD

app = Flask(__name__)

from dotenv import load_dotenv

load_dotenv()  # load from .env file

app.config.update(

    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_USE_TLS=os.getenv("MAIL_USE_TLS") == "True",
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_DEFAULT_SENDER=os.getenv("MAIL_DEFAULT_SENDER")
)

mail = Mail(app)

SUBSCRIPTION_FILE = "subscriptions.json"

# on startup, get session and token
session, token = get_token_and_session()

# ------------------------ utility functions ------------------------

def load_subscriptions():
    if os.path.exists(SUBSCRIPTION_FILE):
        try:
            with open(SUBSCRIPTION_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # if broken, reset the file
            with open(SUBSCRIPTION_FILE, "w") as f:
                f.write("[]")
            return []
    return []

def save_subscriptions(subscriptions):
    with open(SUBSCRIPTION_FILE, "w") as f:
        json.dump(subscriptions, f, indent=2)

def send_email(subject, recipient, body):
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    mail.send(msg)

def fetch_section_details(section_id):
    try:
        details = get_section_details(section_id, session, token)
        if not details:
            print(f"fetch_section_details: no details found for section_id {section_id}")
            return None
        return details
    except Exception as e:
        print(f"fetch_section_details error for section_id {section_id}: {e}")
        return None

# ------------------------ seat checking logic ------------------------

def check_all_subscriptions():
    print("Running seat availability check...")

    subscriptions = load_subscriptions()
    updated_subs = []

    for sub in subscriptions:
        section = fetch_section_details(sub["section_id"])
        current_seats = section.get("Available", 0)

        if current_seats > sub.get("last_known_seats", 0) and current_seats > 0:
            # a seat opened
            send_email(
                recipient=sub["email"],
                subject="Seat Now Available!",
                body=format_section_alert_email(section),
            )

            print(f"alert sent to {sub['email']} for {sub['course_title']}")
        else:
            print(f"no change for {sub['course_title']}")

        sub["last_known_seats"] = current_seats
        updated_subs.append(sub)

    save_subscriptions(updated_subs)

# ------------------------ main site routes ------------------------

@app.route("/")
def index():
    term = request.args.get("term", "")
    keyword = request.args.get("keyword", "").strip()
    course_id = request.args.get("course_id", "").strip()

    courses = []
    sections = []
    error = None

    if keyword and term:
        try:
            courses = search_courses(keyword, term, session, token)
        except Exception as e:
            error = f"Error fetching courses: {str(e)}"

    if course_id and term and keyword:
        try:
            if not courses:
                courses = search_courses(keyword, term, session, token)

            selected = next((c for c in courses if str(c.get("Id")) == course_id), None)
            if selected and selected.get("MatchingSectionIds"):
                sections = get_sections(course_id, selected["MatchingSectionIds"], session, token)
                print("Fetched section data:", sections)
        except Exception as e:
            error = f"Error fetching sections: {str(e)}"

    return render_template(
        "index.html",
        courses=courses,
        sections=sections,
        term=term,
        keyword=keyword,
        course_id=course_id,
        error=error
    )

@app.route("/sections")
def sections():
    course_id = request.args.get("course_id")
    section_ids = request.args.getlist("section_ids")

    if not course_id or not section_ids:
        return jsonify({"error": "Missing course_id or section_ids"}), 400

    try:
        sections_data = get_sections(course_id, section_ids, session, token)
        return jsonify(sections_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/section_details")
def section_details():
    section_id = request.args.get("section_id")

    if not section_id:
        return jsonify({"error": "Missing section_id"}), 400

    try:
        details = get_section_details(section_id, session, token)
        return jsonify(details)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

import pprint

def format_section_alert_email(section_data):
    course_code = section_data.get("CourseName", "Unknown Code")
    section_code = f"{course_code}-{section_data.get('Number', '???')}"
    title = section_data.get("Title", "Untitled Course")

    start_date = section_data.get("StartDate", "N/A")[:10]
    end_date = section_data.get("EndDate", "N/A")[:10]

    available = section_data.get("Available", "N/A")
    capacity = section_data.get("Capacity", "N/A")

    # instructor
    instructors = section_data.get("InstructorItems", [])
    instructor_name = instructors[0].get("Name") if instructors else "TBA"

    # meeting info
    time_location = section_data.get("TimeLocationItems", [])
    if time_location:
        meeting_info = time_location[0].get("Time", "–")
        location_info = time_location[0].get("Location", "").strip()
        if location_info:
            meeting_info += f" in {location_info}"
    else:
        meeting_info = "– (Online)"

    return (
        f"{section_code} — {title}\n"
        f"Dates: {start_date} to {end_date}\n"
        f"Times: {meeting_info}\n"
        f"Seats: {available} available out of {capacity} total\n"
        f"Instructor: {instructor_name}"
    )

@app.route("/subscribe", methods=["POST"])
def subscribe():
    email = request.form.get("email")
    selected_section_ids = request.form.getlist("section_ids")

    if not email or not selected_section_ids:
        return "Missing email or section IDs.", 400

    subscriptions = load_subscriptions()

    for section_id in selected_section_ids:
        section_data = fetch_section_details(section_id)
        if section_data is None:
            return f"Could not retrieve details for section ID {section_id}. Please check and try again.", 400

        available_seats = section_data.get("Available", 0)
        correct_title = section_data.get("Title", "Unknown Title")

        subscription = {
            "email": email,
            "section_id": section_id,
            "course_title": correct_title,
            "last_known_seats": available_seats,
        }
        subscriptions.append(subscription)

        with app.app_context():
            send_email(
            recipient=email,
            subject="Subscription Confirmed",
            body="You'll be alerted when a seat opens in:\n\n" + format_section_alert_email(section_data),
        )

        if available_seats > 0:
            with app.app_context():
                send_email(
                recipient=email,
                subject="Seat Available Now!",
                body=(
                    "A section you just requested to be alerted to already has a seat(s) available:\n\n"
                    + format_section_alert_email(section_data)
                    + "\n\nRegister now through OCAD Self Service."
                ),
            )

    save_subscriptions(subscriptions)
    return "OK"


# ------------------------ scheduler setup ------------------------

scheduler = BackgroundScheduler()
scheduler.add_job(func=check_all_subscriptions, trigger="interval", seconds=15)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

# ------------------------ run the app ------------------------

if __name__ == "__main__":
    app.run(debug=True)

