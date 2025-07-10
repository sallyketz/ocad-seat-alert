import requests

url = "https://selfservice.ocadu.ca/SelfService/Courses/PostSearchCriteria"
headers = {
    "Content-Type": "application/json; charset=utf-8"
}

payload = {
    "keyword": "HUMN",
    "terms": ["2025FA"],
    "pageNumber": 1,
    "quantityPerPage": 30,
    "sortDirection": "Ascending",
    "sortOn": "None",
    "searchResultsView": "CatalogListing",
    "subjects": [],
    "academicLevels": [],
    "courseLevels": [],
    "courseTypes": [],
    "days": [],
    "faculty": [],
    "locations": [],
    "onlineCategories": [],
    "openAndWaitlistedSections": None,
    "openSections": None,
    "sectionIds": None,
    "courseIds": None,
    "requirement": None,
    "subrequirement": None,
    "group": None,
    "startTime": None,
    "endTime": None,
    "startDate": None,
    "endDate": None,
    "endsByTime": None,
    "startsAtTime": None,
    "requirementText": None,
    "subRequirementText": "",
    "topicCodes": [],
    "synonyms": [],
    "keywordComponents": [],
    "subjectsBadge": [],
    "academicLevelsBadge": [],
    "courseLevelsBadge": [],
    "courseTypesBadge": [],
    "daysBadge": [],
    "facultyBadge": [],
    "locationsBadge": [],
    "onlineCategoriesBadge": [],
    "openAndWaitlistedSectionsBadge": "",
    "openSectionsBadge": "",
    "termFiltersBadge": []
}

response = requests.post(url, headers=headers, json=payload)
data = response.json()
courses = data.get("Courses", [])
print(f"Found {len(courses)} courses")
for c in courses:
    code = f"{c['SubjectCode']}-{c['Number']}"
    title = c['Title']
    print(f"{code}: {title}")