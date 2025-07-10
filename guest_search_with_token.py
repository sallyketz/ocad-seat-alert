import requests
from bs4 import BeautifulSoup

def get_guest_token_and_cookies():
    session = requests.Session()
    url = "https://selfservice.ocadu.ca/SelfService/Courses/Search"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    token_tag = soup.find("input", {"name": "__RequestVerificationToken"})

    if not token_tag:
        raise Exception("Could not find verification token in HTML")

    token = token_tag["value"]
    cookies = session.cookies.get_dict()

    return token, cookies, session

def search_courses_guest(keyword="HUMN"):
    token, cookies, session = get_guest_token_and_cookies()

    url = "https://selfservice.ocadu.ca/SelfService/Courses/PostSearchCriteria"

    headers = {
        "__requestverificationtoken": token,
        "__isguestuser": "true",
        "Content-Type": "application/json, charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Origin": "https://selfservice.ocadu.ca",
        "Referer": f"https://selfservice.ocadu.ca/SelfService/Courses/Search?keyword={keyword}",
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest"
    }

    payload = {
        "keyword": keyword,
        "terms": [],
        "requirement": None,
        "subrequirement": None,
        "courseIds": None,
        "sectionIds": None,
        "requirementText": None,
        "subrequirementText": "",
        "group": None,
        "startTime": None,
        "endTime": None,
        "openSections": None,
        "subjects": [],
        "academicLevels": [],
        "courseLevels": [],
        "synonyms": [],
        "courseTypes": [],
        "topicCodes": [],
        "days": [],
        "locations": [],
        "faculty": [],
        "onlineCategories": None,
        "keywordComponents": [],
        "startDate": None,
        "endDate": None,
        "startsAtTime": None,
        "endsByTime": None,
        "pageNumber": 1,
        "sortOn": "None",
        "sortDirection": "Ascending",
        "subjectsBadge": [],
        "locationsBadge": [],
        "termFiltersBadge": [],
        "daysBadge": [],
        "facultyBadge": [],
        "academicLevelsBadge": [],
        "courseLevelsBadge": [],
        "courseTypesBadge": [],
        "topicCodesBadge": [],
        "onlineCategoriesBadge": [],
        "openSectionsBadge": "",
        "openAndWaitlistedSectionsBadge": "",
        "subRequirementText": None,
        "quantityPerPage": 30,
        "openAndWaitlistedSections": None,
        "searchResultsView": "CatalogListing"
    }

    response = session.post(url, headers=headers, json=payload, cookies=cookies)

    print("Status code:", response.status_code)
    print("First 1000 chars of response:", response.text[:1000])

if __name__ == "__main__":
    search_courses_guest()
