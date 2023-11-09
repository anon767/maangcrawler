import json
from typing import List

import requests
from .Crawler import Crawler
from .Job import Job

APPLEURL = "https://jobs.apple.com/api/role/search"
CSRFURL = "https://jobs.apple.com/api/csrfToken"


class Apple(Crawler):
    def __init__(self):
        self.parsed_json = self.parse_job_page()

    def parse_job_page(self, i=1):
        headers = {}
        response = requests.get(CSRFURL)
        headers['cookie'] = '; '.join([x.name + '=' + x.value for x in response.cookies])
        headers['host'] = "jobs.apple.com"
        headers["Accept"] = "*/*"
        headers["Content-Type"] = "application/json"
        headers["X-Apple-CSRF-Token"] = response.headers["X-Apple-CSRF-Token"]

        r = requests.post(
            url=APPLEURL,
            data=json.dumps(
                {"query": "", "filters": {"range": {"standardWeeklyHours": {"start": None, "end": None}}}, "page": i,
                 "locale": "en-us", "sort": "relevance"}),
            headers=headers,
        )

        return json.loads(r.text)

    def get_jobs(self) -> List[Job]:
        jobs = []
        for i in range(1, 100):
            parsed = self.parse_job_page(i)
            for j in parsed["searchResults"]:
                jobs.append(Job(company="apple", title=j["postingTitle"], date=j["postingDate"], desc=j["jobSummary"],
                                id=j["reqId"], location=j["locations"][0]["name"],
                                url="https://jobs.apple.com/en-us/details/{}".format(j["reqId"])))

        return jobs


if __name__ == '__main__':
    apple = Apple()
    print(apple.get_jobs())
