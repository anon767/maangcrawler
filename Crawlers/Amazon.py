import json
from typing import List

import requests
from .Crawler import Crawler
from .Job import Job

AMAZONURL = "https://www.amazon.jobs/en/search.json?base_query=&loc_query=&latitude=&longitude=&loc_group_id=&invalid_location=false&country=&city=&region=&county=&offset={}&result_limit={}"
JOBSPERPAGE = 100


class Amazon(Crawler):
    def __init__(self):
        self.parsed_json = self.parse_job_page()
        self.total_jobs = self.parsed_json["hits"]

    def parse_job_page(self, i=0):
        website = requests.get(AMAZONURL.format(JOBSPERPAGE * i, JOBSPERPAGE))
        return json.loads(website.text)

    def get_jobs(self) -> List[Job]:
        jobs = []
        for i in range(0, self.total_jobs // JOBSPERPAGE):
            parsed_jobs = self.parse_job_page(i)
            for j in parsed_jobs["jobs"]:
                jobs.append(Job(company=j["company_name"], title=j["title"], date=j["posted_date"],
                                desc=j["description_short"], id=j["id_icims"],
                                location=j["location"], url="https://www.amazon.jobs/en/jobs/{}".format(j["id_icims"])))
        return jobs


if __name__ == '__main__':
    amazon = Amazon()
    print(amazon.get_jobs())
