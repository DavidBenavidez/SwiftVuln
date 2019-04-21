from sqlalchemy import func, create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.schema import Sequence

Base = declarative_base()

class Scan(Base):
    __tablename__ = 'scan'
    id = Column(Integer, primary_key=True)
    scan_id = Column('scan_id', String)
    host = Column('Host', String)
    nvt = Column('nvt', String)
    cvss_score = Column('cvss_score', Float)
    summary = Column('summary', String)
    link = Column('link', String)


class scanFuncs:
    def __init__(self):
        self.engine = create_engine('sqlite:///scans.db', echo=True)
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def getCount(self):
        session = self.Session()
        rows = session.query(func.count(Scan.id)).scalar()
        print("ROWS: %d" % rows)
        session.close()
        
    def addScan(self, scan):
        session = self.Session()
        new_scan = Scan()
        new_scan.scan_id = scan['scan_id']
        new_scan.host = scan['host'] 
        new_scan.nvt = scan['nvt'] 
        new_scan.cvss_score = scan['score']
        new_scan.summary = scan['summary']
        if 'link' in scan:
            new_scan.link = scan['link']

        session.add(new_scan)
        session.commit()
        
        session.close()

    def getScans(self):
        session = self.Session()
        scans = session.query(Scan).all()

        for scan in scans:
            print('====================')
            print(scan.scan_id)
            print(scan.host)
            print(scan.nvt)
            print(scan.cvss_score)
            print(scan.summary)
        session.close()