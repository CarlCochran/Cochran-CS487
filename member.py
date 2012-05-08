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
        self.startDay = []
        self.endYear = []
        self.endMonth = []
        self.endDay = []

        #Member's Qualification
        self.qualifiedServiceDays = []
        self.qualifiedServiceMonths = []

        self.entitlementRate = []        
        self.entitlementRemainingMonths = []
        self.entitlementRemainingDays = []

        

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

        #Insufficient built-in date math for 'datetime' - full months are counted
        #as 30 days regardless of their length.
        #Initialize date objects to determine the months and days between them
        serviceMonths = 0          #rate is based on months of service
        serviceDays = 0            #Used to calculate partial months    
        dStart = date(int(self.startYear), int(self.startMonth), int(self.startDay))
        if dStart < d0:
            dStart = d0            #Qualified active duty only after 9/11/2001
        dEnd = date(int(self.endYear), int(self.endMonth), int(self.endDay))
        dTemp = dStart



        #count qualified days and months
        dayDelta = d0-date(2001,9,10)       #one day for incrementing
        monthDelta = d0-date(2001,8,11)     #one month for incrementing
        
        #First partial month:
        if dStart.day > 1:
            while dTemp.day >= dStart.day and dStart.month == dTemp.month and dTemp <= dEnd:
                dTemp = dTemp + dayDelta #Day will always end up as 1
                serviceDays = serviceDays + 1

        #All full months:
        while dTemp < dEnd:
            dTemp = dTemp + monthDelta
            serviceMonths = serviceMonths + 1

        #Last partial month:
        while dTemp <= dEnd:
            dTemp = dTemp + dayDelta
            serviceDays = serviceDays + 1

        #If partial months >= 1 month, change to months
        while serviceDays > 29:
            serviceMonths = serviceMonths + 1
            serviceDays = serviceDays - 30
        
        self.qualifiedServiceDays = serviceDays
        self.qualifiedServiceMonths = serviceMonths

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


        #All members (who are entitled) start with 36 Months, 0 Days
        if self.entitlementRate > 0:
            self.entitlementRemainingMonths = 36
        else:
            self.entitlementRemainingMonths = 0

        self.entitlementRemainingDays = 0
        



