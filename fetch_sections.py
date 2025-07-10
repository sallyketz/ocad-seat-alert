import requests

def get_sections(course_id, section_ids):
    url = "https://selfservice.ocadu.ca/SelfService/Courses/Sections"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "courseId": course_id,
        "sectionIds": section_ids
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Failed to fetch sections: {response.status_code}")
        print(response.text)
        return {}
    return response.json()

if __name__ == "__main__":
    course_id = "5044"  
    section_ids = ["21586", "21587"]
    data = get_sections(course_id, section_ids)

    sections_info = data.get("SectionsRetrieved", {}).get("TermsAndSections", [])
    for term_and_sections in sections_info:
        term = term_and_sections.get("Term", {})
        print(f"Term: {term.get('Description')} ({term.get('Code')})")
        sections = term_and_sections.get("Sections", [])
        for section_wrapper in sections:
            section = section_wrapper.get("Section", {})
            print(f" Section: {section.get('SectionNameDisplay')}")
            print(f"  Title: {section.get('SectionTitleDisplay')}")
            if section.get("HasUnlimitedSeats"):
                print(f"  Seats: Unlimited")
            else:
                print(f"  Seats: {section.get('AvailableSeats', 'unknown')} available")
            print("  Meeting times:")
            for mt in section.get("FormattedMeetingTimes", []):
                print(f"   - {mt.get('DaysOfWeekDisplay')} {mt.get('StartTimeDisplay')} to {mt.get('EndTimeDisplay')} @ {mt.get('BuildingDisplay')} {mt.get('RoomDisplay')}")
            print()
