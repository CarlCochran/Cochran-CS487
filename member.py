from datetime import date

class Member:
    
    def __init__(self):

        #Member personal information
        self.memNum = []
        self.lname = []
        self.fname = []
        self.mi = []
        self.zipCode = []

        #Member's date of entry and exit from active duty
        self.startYear = []
        self.startMonth = []
        self.qualifiedServiceDays = []
        self.qualifiedServiceMonths = []
        
        self.totalEntitlementDays = []
        self.entitlementRemainingDays = []
        self.entitlementRate = []
        

    def add(self, memNum, lname, fname, mi, zipCode, startYear, startMonth,
            startDay, endYear, endMonth, endDay):
        self.memNum = memNum
        self.lname = lname
        self.fname = fname
        self.mi = mi
        self.zipCode = zipCode

        self.startYear = startYear
        self.startMonth = startMonth
        self.startDay = startDay
        self.endYear = endYear
        self.endMonth = endMonth
        self.endDay = endDay

        #Use service dates to calculate days of entitlement
        self.calculateEntitlement()
        

    def calculateEntitlement(self):
        #Ch33 Entitlement is based only on service dates on and after 9/11/2001
        d0 = date(2001, 9, 11)
        dStart = date(self.startYear, self.startMonth, self.startDay)
        dEnd = date(self.endYear, self.endMonth, self.endDay)
        self.totalService = dEnd - dStart
        
        if ((dStart - d0).days < 0):
            self.qualifiedServiceDays = (dEnd - d0).days
        else:
            self.qualifiedServiceDays = self.totalService.days

        self.qualifiedServiceMonths = float(self.qualifiedServiceDays) / (365.2425/12)

        #Ch33 Rate is based on months of service
        #100% for  36+ months
        #90%  for  30.0-35.9
        #80%  for  24.0-29.9
        #70%  for  18.0-23.9
        #60%  for  12.0-17.9
        #50%  for   6.0-11.9
        #40%  for   1.5-5.9
        #0%   for   0.0-1.4

        if (self.qualifiedServiceMonths >= 36):
            self.entitlementRate = 1
        elif (self.qualifiedServiceMonths >= 30):
            self.entitlementRate = 0.9
        elif (self.qualifiedServiceMonths >= 24):
            self.entitlementRate = 0.8
        elif (self.qualifiedServiceMonths >= 18):
            self.entitlementRate = 0.7
        elif (self.qualifiedServiceMonths >= 12):
            self.entitlementRate = 0.6
        elif (self.qualifiedServiceMonths >= 6):
            self.entitlementRate = 0.5
        elif (self.qualifiedServiceMonths >= 1.5):
            self.entitlementRate = 0.4
        else:
            self.entitlementRate = 0

        



