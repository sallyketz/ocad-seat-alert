import requests

def get_section_details(section_id):
    url = "https://selfservice.ocadu.ca/SelfService/Courses/SectionDetails"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "sectionId": section_id,
        "studentId": None
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Failed to fetch section details: {response.status_code}")
        print(response.text)
        return {}
    return response.json()

if __name__ == "__main__":
    section_id = "21586"
    details = get_section_details(section_id)

    section_name = details.get("SectionName", details.get("Number", "unknown"))
    seats_total = details.get("Capacity", "unknown")
    seats_available = details.get("Available", "unknown")
    seats_taken = details.get("Enrolled", "unknown")

    print(f"Section {section_name} seat info:")
    print(f"  Total seats: {seats_total}")
    print(f"  Seats taken: {seats_taken}")
    print(f"  Seats available: {seats_available}")
