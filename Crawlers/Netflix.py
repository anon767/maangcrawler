import json
from typing import List

import requests
from .Crawler import Crawler
from .Job import Job

NETFLIXURL = "https://jobs.netflix.com/api/search?page={}"


class Netflix(Crawler):
    def __init__(self):
        self.parsed_json = self.parse_job_page()

    def parse_job_page(self, i=1):
        self.website = requests.get(NETFLIXURL.format(i))
        return json.loads(self.website.text)

    def get_jobs(self) -> List[Job]:
        jobs = []
        for i in range(1, 50):
            parsed_jobs = self.parse_job_page(i)
            for j in parsed_jobs["records"]["postings"]:
                jobs.append(Job(company="netflix", title=j["text"], date=j["created_at"], desc=j["description"],
                                id=j["external_id"], location=j["location"],
                                url="https://jobs.netflix.com/jobs/{}".format(j["external_id"])))
        return jobs


if __name__ == '__main__':
    netflix = Netflix()
    netflix.get_jobs()
