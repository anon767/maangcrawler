import json
from typing import List

import requests
from .Crawler import Crawler
from .Job import Job

MICROSOFTURL = "https://gcsservices.careers.microsoft.com/search/api/v1/search?l=en_us&pg={}&pgSz=200&o=Relevance&flt=true"


class Microsoft(Crawler):
    def __init__(self):
        self.parsed_json = self.parse_job_page()
        self.total_jobs = self.parsed_json["operationResult"]["result"]["totalJobs"]
        self.jobs_per_page = len(self.parsed_json["operationResult"]["result"]["jobs"])

    def parse_job_page(self, i=1):
        self.website = requests.get(MICROSOFTURL.format(i))
        return json.loads(self.website.text)

    def get_jobs(self) -> List[Job]:
        jobs = []
        for i in range(1, self.total_jobs // self.jobs_per_page):
            parsed_jobs = self.parse_job_page(i)
            for j in parsed_jobs["operationResult"]["result"]["jobs"]:
                jobs.append(Job(company="microsoft", title=j["title"], date=j["postingDate"],
                                desc=j["properties"]["description"], id=j["jobId"],
                                location=j["properties"]["primaryLocation"],
                                url="https://jobs.careers.microsoft.com/global/en/job/{}".format(j["jobId"])))
        return jobs


if __name__ == '__main__':
    msoft = Microsoft()
    msoft.get_jobs()
