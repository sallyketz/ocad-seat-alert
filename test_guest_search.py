import requests

def test_guest_course_search():
    url = "https://selfservice.ocadu.ca/SelfService/Courses/PostSearchCriteria"

    headers = {
        "__isguestuser": "true",
        "__requestverificationtoken": "CfDJ8B0GSlrVWN9Dn-qVRI-h8-0NxeR_IKq_9CzR7aRPxBOpm2CsGPSr3wiRjIQQvmdQN73TMyZ-vz79b9UwQ29R_dWLFwoEkgceJ018phBh7FyGamzHvDVPFdoBaloK0ypPW1wJTxBR5_qGJsc04p4z3Zo",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/json, charset=UTF-8",
        "origin": "https://selfservice.ocadu.ca",
        "referer": "https://selfservice.ocadu.ca/SelfService/Courses/Search?keyword=HUMN",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    cookies = {
        "ocaduSelfService": "CfDJ8B0GSlrVWN9Dn-qVRI-h8-0mlktp5FzNBif1S08rP7fDMOrUHZ2fXDfz79tHWD3OnvDN0IGQQMW7FMDvsVk9aGcpFGSkvURj9z40ii4sIpoRN3np3Y5nKLJaxiFThQ7N87S-JHuqx7AIPaAFwNM4dgQPL9kPWEUHp5pcd5biMm6HivO9973aokUGgWCa2f2F3IzL-ZyK_gCZMCJGV-Jk-K-MXrOSyUU5YCDRRocPBLfsrvn4exfp28Cu0utaQfTlb4fn0w5AmnO1qC-8U_yZu34a_xxgrBT8hNkcWT4JOCEv5lcmUsI9Okqe0xjq3pWrxbxQ9FD5HcXIYYjc593WQV8-ivw4LKYPjogNiHZ1Bad_JqiQsocVIE892r0dVHmNGNOSYEkYB9eSv4XLusIp3fLKJm-Gs9JNa_eOJ5TtfEfPDtxw43bcPhq_vIa38KPGJG1-SQNq0py0S-HW5VMINZtiYSAxx4mic5nrana2GEsBHAM524GKbhRH-5mSRsHwps08GKPwlaZwnDnBe2DPg9TBI7-rdK5mnqNIJgCe8eG2MrpJawG_cCyFZK-0yowpX5r9FLFIBHJXusyBpzbnMXBC5ak8c9UgVp1zQXMej2hYm89PTBT6hGXFYgfl4iS2kbytwqua2wJNaqaSYLN2z1xv4dFn4BqoaftR91xFUrbs5WCDJmIW3vY0iC_1vXdzdGYlERQggui1dz8tXxzmh3b5PQpf4bOGprI644VzQjyv99itQlEM-GTQ7-_ZuBeuMDm8vh_MRXzKuur8Y7R6JHDcq8Kuq-lZth6wE3pgV3-NADARwx_WufVVNFyruTNj1c3wnL6dsC8zOhnHgnj78EkinS-xqGk2jGzgR5td-jJDN6aVs2m2Ky5tzKwc4gQ9iYm99v_TQ6UPbYMzBLEpcfXRs63zbV8Dn-4vIishNoQ4SG8OVzqkZIjORQ62tJTx4IIwVb5BZMpSjc7vJ46GXjyYGUtnrFrHmrYD7zpD8JRWYhmVYbtDDXgKNxmUBFtSCn_E5mIPPD17v03jlEp6W8sm7eoEpyoDhN7G6C7NjUCjRygWgPO_rC3bpWo8Gut0KLnK1X9EV9mm-5yrcwRKlnyoBvfLq4a7i7A0s-VhXjYdkrBmbprrOMDK6BRTp-icSXsr-ZLJSlttcCWv7J8vM5-ayA6wQd8irrK5e8YaFKnA2hrrtvIw6vrtaNbYhZK_C0PxzNF_eKL4_yD6_e4ent79A67fyICiCqJMuVE7dwEiPX9R0uvqcM3XSgJHQgtMDbMWPT6CirkeyzkWSR7CjrXccNNHg6o7djqH2jcR1N60R_P1c-HptyNqX1EhD2MlKBQzC-SflDgMUXuG_UR1rRaSRPsHS1BIThk3t6SOW5TSEbxr6DaUwU7RdL_n7L9jWDupmw47aGYVb62I2hwX5I4"
    }

    payload = {
        "keyword": "HUMN",
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

    response = requests.post(url, headers=headers, cookies=cookies, json=payload)

    print("Status code:", response.status_code)
    print("Response headers:", response.headers)
    print("Response text (first 1000 chars):", response.text[:1000])

if __name__ == "__main__":
    test_guest_course_search()
