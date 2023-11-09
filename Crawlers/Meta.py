import json
import time
from typing import List

from .Crawler import Crawler
from .Job import Job

METAURL = "https://www.metacareers.com/jobs/"

from seleniumwire import webdriver
from seleniumwire.utils import decode
from datetime import date


class Meta(Crawler):

    def parse_job_page(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        driver.get("https://www.metacareers.com/jobs/")
        time.sleep(10)
        for request in driver.requests:
            if request.response:
                if request.url == "https://www.metacareers.com/graphql":
                    body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))

                    parsed = json.loads(body)["data"]
                    if "job_search" in parsed:
                        driver.quit()
                        return parsed

    def get_jobs(self) -> List[Job]:
        jobs = []
        parsed = self.parse_job_page()["job_search"]
        for j in parsed:
            location = "N/A"
            if len(j["locations"]) > 0:
                location = j["locations"][0]
            jobs.append(Job(company="meta", title=j["title"], date=date.today(), desc=j["teams"][0],
                            id=j["id"], location=location, url="https://www.metacareers.com/jobs/{}".format(j["id"])))

        return jobs


if __name__ == '__main__':
    meta = Meta()
    print(meta.get_jobs())
