from sqlalchemy import ForeignKey, ForeignKeyConstraint, func, create_engine, Column, Integer, Float, Date, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.schema import Sequence

Base = declarative_base()

class ScanDetails(Base):
    __tablename__ = 'scan_details'
    id = Column(Integer, primary_key=True, nullable=False)
    scan_id = Column('scan_id', String, nullable=False)
    host = Column('host', String, nullable=False)
    nvt = Column('nvt', String, nullable=False)
    cvss_score = Column('cvss_score', Float, nullable=False)
    summary = Column('summary', String, nullable=False)
    link = Column('link', String)

class Scan(Base):
    __tablename__ = 'scan'
    scan_id = Column('scan_id', String, primary_key=True, nullable=False)
    scan_name = Column('scan_name', String, nullable=False)
    scan_date = Column('scan_date', Date, nullable=False)
    scan_score = Column('scan_score', Float, nullable=False)


class scanFuncs:
    def __init__(self):
        # self.engine = create_engine('sqlite:///swiftvuln.db', echo=True)
        self.engine = create_engine('sqlite:///swiftvuln.db')
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def addScan(self, scan):
        session = self.Session()
        new_scan = Scan()

        new_scan.scan_id = scan['scan_id']
        new_scan.scan_name = scan['scan_name']
        new_scan.scan_date = scan['scan_date']
        new_scan.scan_score = scan['scan_score']

        session.merge(new_scan)
        session.commit()
        
        session.close()

    def getScanScore(self, scan_id):
        session = self.Session()
        try:
            scan = session.query(Scan).filter(Scan.scan_id==scan_id).one()
        except:
            session.close()
            return(None)

        session.close()
        return(float(scan.scan_score))
    
    
    def getScansByRange(self, cur_date, date_range):
        session = self.Session()

        # List of scan id's to get from database
        scans_list = [] 

        # Get current year and month
        cur_date = (str(cur_date))
        cur_date = map(int, cur_date.split("-"))

        # Get all scans
        scans = session.query(Scan).all()
        
        # Range is 1,3,6,12
        # get month
        month = cur_date[1] - date_range

        for scan in scans:
            scan_date = str(scan.scan_date)
            scan_date = map(int, scan_date.split("-"))
            
            # if month is less than or equal 0, get scans from previous year  
            if(month <= 0):
                # check if scan date is from previous year
                if(scan_date[0] == (cur_date[0]-1)):
                    # Check scan month
                    if(scan_date[1] >= (12+month)):
                        scans_list.append(str(scan.scan_id))
                # If scan is from current year
                if(scan_date[0] == (cur_date[0])):
                    # Check scan month
                    if(scan_date[1] <= cur_date[1]):
                        scans_list.append(str(scan.scan_id))
            else:
                # check if scan date is from current year
                if(scan_date[0] == cur_date[0]):
                    # Check scan month
                    if(scan_date[1] >= month):
                        scans_list.append(str(scan.scan_id))        
        session.close()
        return(scans_list)
    
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
        #scan_id, scan_name
        scans = session.query(Scan).all()
        session.close()
        return(scans)

class scanDetailsFuncs:
    def __init__(self):
        # self.engine = create_engine('sqlite:///swiftvuln.db', echo=True)
        self.engine = create_engine('sqlite:///swiftvuln.db')
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def getCount(self):
        session = self.Session()
        rows = session.query(func.count(ScanDetails.id)).scalar()
        print("COUNT: %d" % rows)
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

    def deleteScan(self, scan_id):
        session = self.Session()
        
        toDelete = session.query(ScanDetails).filter(ScanDetails.scan_id==scan_id)

        for item in toDelete:
            session.delete(item)

        session.commit()
        session.close()

    def getScans(self):
        session = self.Session()
        #scan_id, host, nvt, cvss_score, summary
        scans = session.query(ScanDetails).all()
        session.close()
        return(scans)

    def getScanDetails(self, scan_id):
        session = self.Session()
        scans = session.query(ScanDetails).filter(ScanDetails.scan_id==scan_id).all()
        session.close()  
        return(scans)
    
    def getHostCount(self, host):
        session = self.Session()
        rows = session.query(func.count(ScanDetails.id)).filter(ScanDetails.host==host).scalar()
        session.close()
        return(rows)

# db = scanDetailsFuncs()

# scans = db.getScans()

# for scan in scans:
#     print(scan.cvss_score)