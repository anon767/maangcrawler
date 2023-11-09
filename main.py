from typing import List

from flask import *
from tqdm import tqdm

from Crawlers.Amazon import Amazon
from Crawlers.Apple import Apple
from Crawlers.Crawler import Crawler
from Crawlers.Google import Google
from Crawlers.Job import Job
from Crawlers.Meta import Meta
from Crawlers.Netflix import Netflix
from Crawlers.Microsoft import Microsoft

from DB.DBJob import DBjob

job_pages = {"microsoft": Microsoft(), "meta": Meta(), "amazon": Amazon(), "apple": Apple(), "netflix": Netflix(), "google": Google()}
DB = DBjob()

app = Flask("maangsearch")


def crawl_jobs():
    print("Crawling Jobs")
    jobs = []
    page: Crawler
    for key, value in tqdm(enumerate(job_pages)):
        print(f"\nLoading {value}")
        jobs.extend(job_pages[value].get_jobs())
    return jobs


def store_jobs(jobs: List[Job]):
    print("Storing Jobs")
    for job in tqdm(jobs):
        DB.store_job(job)


@app.route("/", methods=['POST', 'GET'])
@app.route("/home", methods=['POST', 'GET'])
def main():
    jobs = []
    if "job" in request.args:
        search_word = request.args.get("job")
        jobs = DB.search(search_word)
    return render_template("home.html", jobs=jobs)


@app.route("/update", methods=['GET'])
def update():
    jobs = crawl_jobs()
    store_jobs(jobs)


jobs = crawl_jobs()
store_jobs(jobs)

if __name__ == "__main__":
    app.run(debug=False)
