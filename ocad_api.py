import requests
from bs4 import BeautifulSoup

BASE = "https://selfservice.ocadu.ca/SelfService/Courses"
SEARCH_PAGE_URL = "https://selfservice.ocadu.ca/SelfService/Courses/Search?keyword="

def get_token_and_session():
    session = requests.Session()
    resp = session.get(SEARCH_PAGE_URL)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    token_tag = soup.find("input", {"name": "__RequestVerificationToken"})
    if not token_tag:
        raise Exception("Can't find __RequestVerificationToken in page")

    token = token_tag["value"]
    return session, token

def search_courses(keyword, term_code, session, token):
    url = f"{BASE}/PostSearchCriteria"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/json; charset=UTF-8",
        "x-requested-with": "XMLHttpRequest",
        "__isguestuser": "true",
        "__RequestVerificationToken": token,
    }

    payload = {
        "keyword": keyword,
        "terms": [term_code],
        "requirement": None,
        "subrequirement": None,
        "courseIds": None,
        "academicLevels": [],
        "academicLevelsBadge": [],
        "courseLevels": [],
        "courseLevelsBadge": [],
        "courseTypes": [],
        "courseTypesBadge": [],
        "days": [],
        "daysBadge": [],
        "endDate": None,
        "endTime": 1440,
        "endsByTime": None,
        "faculty": [],
        "facultyBadge": [],
        "group": None,
        "keywordComponents": [],
        "locations": [],
        "locationsBadge": [],
        "onlineCategories": [],
        "onlineCategoriesBadge": [],
        "openAndWaitlistedSections": False,
        "openAndWaitlistedSectionsBadge": False,
        "openSections": False,
        "openSectionsBadge": False,
        "pageNumber": 1,
        "quantityPerPage": 30,
        "requirementText": None,
        "searchResultsView": "CatalogListing",
        "sectionIds": None,
        "sortDirection": 0,
        "sortOn": 2,
        "startDate": None,
        "startTime": 0,
        "startsAtTime": None,
        "subRequirementText": None,
        "subrequirement": None,
        "subrequirementText": "",
        "synonyms": [],
        "termFiltersBadge": [
            {"Value": term_code, "Description": "", "Count": 0, "Selected": True}
        ],
        "terms": [term_code],
        "topicCodes": [],
        "topicCodesBadge": [],
    }

    resp = session.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data.get("Courses", [])

def get_sections(course_id, section_ids, session, token):
    url = f"{BASE}/Sections"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/json; charset=UTF-8",
        "x-requested-with": "XMLHttpRequest",
        "__isguestuser": "true",
        "__RequestVerificationToken": token,
    }
    payload = {"courseId": course_id, "sectionIds": section_ids}

    resp = session.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data.get("SectionsRetrieved", {}).get("TermsAndSections", [])

def get_section_details(section_id, session, token):
    url = f"{BASE}/SectionDetails"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/json; charset=UTF-8",
        "x-requested-with": "XMLHttpRequest",
        "__isguestuser": "true",
        "__RequestVerificationToken": token,
    }
    payload = {"sectionId": section_id, "studentId": None}

    resp = session.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()
