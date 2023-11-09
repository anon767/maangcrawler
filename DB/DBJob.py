from typing import List

from sqlalchemy import String, and_
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from Crawlers.Job import Job


class Base(DeclarativeBase):
    pass


class DBjob(Base):
    __tablename__ = "jobs"
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    desc: Mapped[str] = mapped_column(String(300))
    date: Mapped[str] = mapped_column(String(300))
    location: Mapped[str] = mapped_column(String(300))
    url: Mapped[str] = mapped_column(String(300))
    company: Mapped[str] = mapped_column(String(30))

    def store_job(self, job: Job):
        with Session(engine) as session:
            try:
                job = DBjob(id=job.id, title=job.title, location=job.location, desc=job.desc, date=job.date,
                            url=job.url,
                            company=job.company)
                session.add(job)
                session.commit()
            except Exception:
                print("Job already stored")

    def search(self, q: str) -> List:
        queries = q.split(" ")

        clauses = []
        clauses.extend([DBjob.desc.like('%{0}%'.format(k)) for k in queries])
        # clauses.extend([DBjob.title.like('%{0}%'.format(k)) for k in queries])
        # clauses.extend([DBjob.company.like('%{0}%'.format(k)) for k in queries])
        # clauses.extend([DBjob.location.like('%{0}%'.format(k)) for k in queries])

        with Session(engine) as session:
            query = session.query(DBjob).filter(
                and_(*clauses))
        return query.all()


engine = create_engine("sqlite:///database.db", echo=True)

with engine.connect() as conn:
    pass
DBjob.metadata.create_all(engine)
