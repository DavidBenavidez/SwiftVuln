from sqlalchemy import ForeignKey, ForeignKeyConstraint, func, create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.schema import Sequence

Base = declarative_base()

class ScanDetails(Base):
    __tablename__ = 'scan_details'
    id = Column(Integer, primary_key=True, nullable=False)
    scan_id = Column('scan_id', String, ForeignKey("scan.scan_id", ondelete="CASCADE"), nullable=False)
    host = Column('host', String, nullable=False)
    nvt = Column('nvt', String, nullable=False)
    cvss_score = Column('cvss_score', Float, nullable=False)
    summary = Column('summary', String, nullable=False)
    link = Column('link', String)


class Scan(Base):
    __tablename__ = 'scan'

    scan_id = Column('scan_id', String, primary_key=True, nullable=False)
    scan_name = Column('scan_name', String, nullable=False)

    parent = relationship(ScanDetails, backref="parent", passive_deletes='all')


class scanFuncs:
    def __init__(self):
        self.engine = create_engine('sqlite:///swiftvuln.db', echo=True)
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def addScan(self, scan):
        session = self.Session()
        new_scan = Scan()

        new_scan.scan_id = scan['scan_id']
        new_scan.scan_name = scan['scan_name']

        session.merge(new_scan)
        session.commit()
        
        session.close()
    
    def deleteScan(self, scan_id):
        session = self.Session()
        
        toDelete = session.query(Scan).filter(Scan.scan_id==scan_id)

        for item in toDelete:
            session.delete(item)

        session.commit()
        session.close()

    def getCount(self):
        session = self.Session()
        rows = session.query(func.count(Scan.scan_id)).scalar()
        print("ROWS: %d" % rows)
        session.close()
    
    def getScans(self):
        session = self.Session()
        scans = session.query(Scan).all()
        for scan in scans:
            print('====================')
            print(scan.scan_id)
            print(scan.scan_name)
            print('====================')
        session.close()

class scanDetailsFuncs:
    def __init__(self):
        self.engine = create_engine('sqlite:///swiftvuln.db', echo=True)
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def getCount(self):
        session = self.Session()
        rows = session.query(func.count(ScanDetails.id)).scalar()
        print("ROWS: %d" % rows)
        session.close()
        
    def addScan(self, scan):
        session = self.Session()
        new_scan = ScanDetails()
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
        scans = session.query(ScanDetails).all()

        for scan in scans:
            print('====================')
            print(scan.scan_id)
            print(scan.host)
            print(scan.nvt)
            print(scan.cvss_score)
            print(scan.summary)
            print('====================')
        session.close()