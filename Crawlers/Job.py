import re


def striphtml(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


class Job:
    def __init__(self, title, desc, company, location, id, date, url=None):
        self.id = id
        self.title = title
        if desc is not None:
            self.desc = striphtml(desc)
        self.company = company
        self.location = location
        self.date = date
        self.url = url

    def __str__(self):
        return f"Job ID: {self.id}\nTitle: {self.title}\nDescription: {self.desc}\nCompany: {self.company}\nLocation: {self.location}\nDate: {self.date}\nUrl: {self.url}"
