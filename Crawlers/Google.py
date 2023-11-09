import json
from datetime import date
from typing import List

import requests

from .Crawler import Crawler
from .Job import Job

GOOGLEURL = "https://www.google.com/about/careers/applications/_/HiringCportalFrontendUi/data/batchexecute"
JOBSPERPAGE = 100


class Google(Crawler):
    def __init__(self):
        self.parsed_json = self.parse_job_page()

    def parse_job_page(self, i=1):
        headers = {}
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        website = requests.post(GOOGLEURL,
                                data={
                                    "f.req": '[[["r06xKb","[[null,[],[],[],null,null,[],{},null,null,null,null,null,[],[],null,[2]]]",null,"3"]]]'.format(
                                        i)},
                                headers=headers)
        text = "\n".join(website.text.splitlines()[2:])
        return json.loads(json.loads(text)[0][2])

    def get_jobs(self) -> List[Job]:
        jobs = []
        for i in range(1, 100):
            try:
                for j in self.parse_job_page(i)[0]:
                    jobs.append(Job(company="Google", title=j[1], date=date.today(),
                                    desc=j[3][1], id=j[0],
                                    location=j[8],
                                    url="https://www.google.com/about/careers/applications/jobs/results/{}".format(
                                        j[0])))
            except Exception:
                return jobs
        return jobs


if __name__ == '__main__':
    google = Google()
    google.get_jobs()
