# Post 9/11 GI Bill Accounting System
# Carl COchran
# CS 487-03
# Professor: Virgil Bistriceanu
# Spring 2012

from easygui import *
import member
import MySQLdb as db
from datetime import *

def inputValidation(x):
    #Input Validation
                  
    chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -')   #Valid alphabetic set
    errmsg = ""                                                             #Init to no errors
    d1valid = False
    d2valid = False
    
    for i in range(len(x.lname)):                            #Check for invalid characters in name
        if x.lname == "":
            errmsg += ('Last Name must not be blank.\n')
            break
        if any ((c in chars) for c in x.lname[i]):
            continue
        else:
            errmsg += ('Last Name contains invalid characters.\n')
            break
        
    for i in range(len(x.fname)):
        if x.fname == "":
            errmsg += ('First Name must not be blank.\n')
            break
        if any ((c in chars) for c in x.fname[i]):
            continue
        else:
            errmsg += ('First Name contains invalid characters.\n')
            break
        
    if (len(x.mi)) > 1 or not any((c in chars) for c in x.mi) and x.mi != "":
        errmsg += ('Middle Initial contains invalid or too many characters.\n')
        
    try:
        con = db.connect(host = 'instance12186.db.xeround.com',port=3915, \
                       user='carl',passwd='graendal',db='gibillmembers')
        cur = con.cursor()
        cur.execute ("select * from ziprates where zipCode = %s", (x.zipCode))
        if not cur.fetchone():
            errmsg += ('Zip Code not in database\n')
        cur.close()
        con.close()
    except:
        errmsg += ('Rate database unavailable.  Contact your administrator.\n')

    try:
        d1 = date(int(x.startYear), int(x.startMonth), int(x.startDay))
        d1valid = True
    except:
        errmsg += ('Date of Entry is Invalid.  Use format YYYY / MM / DD\n')

    try:
        d2 = date(int(x.endYear), int(x.endMonth), int(x.endDay))
        d2valid = True
    except:
        errmsg += ('Date of Separation is Invalid.  Use format YYYY / MM / DD\n')

    if d1valid and d2valid:
        if d2 > date.today():
            errmsg += ('Date of separation must have already passed.\n')
        if d1 > d2:
            errmsg += ('Date of separation must be after date of entry.\n')
    
    return errmsg
     


        

def addMember(num):
    fields = ['id','lname','fname','mi','zipcode','yrEntered','moEntered','daEntered','yrLeft','moLeft','daLeft']

    #Check if member already exists
    try:
        con = db.connect(host = 'instance12186.db.xeround.com',port=3915, \
                         user='carl',passwd='graendal',db='gibillmembers');
        cur = con.cursor()
        cur.execute ("select * from members where id = %s", (num)) #to select one member
        if cur.fetchone():
            msgbox(msg = "ID already exists in database.")
            x = editMember(num)
            return x

        cur.close()
        con.close()
    except db.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        
    msg = "Enter New Member Information: ",num
    title = "Add New Member"
    fieldNames = ["Last Name","First Name","Middle Initial","Zip Code","Year Entered Service","Month Entered Service", \
                  "Day Entered Service","Year Exited Service","Month Exited Service","Day Exited Service"]
    fieldValues = []        #init to blank
    fieldValues = multenterbox(msg,title,fieldNames)

    if fieldValues == None: return None                             #Cancel was clicked               

    #Input Validation   
    while 1:   
        x = member.Member()
        x.add(num, fieldValues[0], fieldValues[1], fieldValues[2], fieldValues[3], fieldValues[4], \
              fieldValues[5], fieldValues[6], fieldValues[7], fieldValues[8], fieldValues[9])

        errmsg = inputValidation(x)
        if errmsg == "": break                                              #Passed validation
        fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)  #Failed validation
    

    #Connect to database for adding new member
    con = None
    try:
        con = db.connect(host = 'instance12186.db.xeround.com',port=3915, \
                         user='carl',passwd='graendal',db='gibillmembers');
        cur = con.cursor()
        cur.execute('INSERT INTO members (id,lname,fname,mi,zipcode,yrEntered,moEntered,daEntered,yrLeft, \
                    moLeft,daLeft,rate,monthsLeft,daysLeft) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s", \
                    "%s","%s","%s","%s","%s","%s")'% (x.memNum, x.lname, x.fname, x.mi, x.zipCode, x.startYear,\
                     x.startMonth, x.startDay, x.endYear, x.endMonth, x.endDay,\
                     x.entitlementRate, x.entitlementRemainingMonths, x.entitlementRemainingDays))
        con.commit()
        cur.close()
        con.close()

    except db.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])

    msgbox(msg = "Add Member Successful.")
    x = editMember(num)  
    return x


    
def editMember(num):
    fields = ['id','lname','fname','mi','zipcode','yrEntered','moEntered','daEntered','yrLeft','moLeft','daLeft',\
              'rate','monthsLeft','daysLeft','rate','monthsLeft','daysLeft']
    
    #Connect to database to look up existing member
    con = None
    try:
        con = db.connect(host = 'instance12186.db.xeround.com',port=3915, \
                         user='carl',passwd='graendal',db='gibillmembers');
        cur = con.cursor()
        cur.execute ("select * from members where id = %s", (num)) #to select one member
           
        row = cur.fetchone()
        if not row:                                      #Check whether id exists in DB
            msgbox(msg='No member found with this ID.')
            cur.close()
            con.close()
            return None

        
        desc = cur.description                            #for column headers
        msg = ""
        for field in range(14):
            msg += "%-20s %-20s\n" %(desc[field][0],str(row[field]))
        choices = ["Edit","Done","Delete Record"]
        reply = buttonbox(msg,choices=choices)
        if reply == "Done":
            cur.close()
            con.close()
            return None
        elif reply == "Edit":
            #Editing member will reset rate and remaining entitlement - save current or changed values
            save=[row[11],row[12],row[13]]

            x = member.Member()
            x.add(num, row[1], row[2], row[3], row[4], row[5], row[6], row[7], \
                  row[8], row[9], row[10])
            x.entitlementRate = save[0]
            x.entitlementRemainingMonths = save[1]
            x.entitlementRemainingDays = save[2]
            
            msg = "Enter New Member Information"
            title = "Edit Member Information"
            msg = "Member Number: ",x.memNum
            fieldNames = ["Last Name","First Name","Middle Initial","Zip Code","Year Entered Service", \
                          "Month Entered Service","Day Entered Service","Year Exited Service", \
                          "Month Exited Service","Day Exited Service","Entitlement Rate", \
                          "Months Remaining","Days Remaining"]
            fieldValues = []
            fieldValues = multenterbox(msg,title,fieldNames,(x.lname,x.fname,x.mi,x.zipCode,x.startYear, \
                          x.startMonth,x.startDay,x.endYear,x.endMonth,x.endDay,x.entitlementRate, \
                          x.entitlementRemainingMonths,x.entitlementRemainingDays))

           
            #Input Validation   
            while 1:   
                x = member.Member()
                x.add(num, fieldValues[0], fieldValues[1], fieldValues[2], fieldValues[3], fieldValues[4], \
                      fieldValues[5], fieldValues[6], fieldValues[7], fieldValues[8], fieldValues[9])

                errmsg = inputValidation(x)
                if errmsg == "": break                                              #Passed validation
                fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)  #Failed validation

            for i in range(1, 13):
                cur.execute("UPDATE members SET %s = '%s' WHERE id = %s"% (fields[i], fieldValues[i-1], num))
            con.commit()
            cur.close()
            con.close()

            msgbox(msg = "Update Successful.")
            x = editMember(num)
            return x

        #Delete Member Selected
        else:
            a = buttonbox(msg = 'Are you sure you want to delete this record?\n%s %s %s'% (row[0], \
                        row[1], row[2]), title = 'Delete Record', choices=('Confirm','Cancel'), \
                        image=None)
            if a:
                cur.execute('DELETE FROM members WHERE id = %s' % num)
                con.commit()
            cur.close()
            con.close()
                        
    except db.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        return None        
  
def validateTerm(num):
    pass

  

#Main Routine
msgbox(msg='Post 9/11 GI Bill Member and Accounting System\n\tby Carl Cochran')
while 1:
    a = choicebox(msg='Choose Mode',title='Post 9/11 GI Bill Member and Accounting System', \
                  choices=('Add Member','View/Edit Member','Validate Term'))
    if a == None:                                  #Cancel was clicked, exit program
        exit()
        
    b = enterbox(msg='Enter Member\'s 9-digit member number with no dashes.')
    if b == None:                                   #Cancel was clicked: return to main menu
        continue
    elif str.isdigit(b) and int(b) >= 100000000 and int(b) <= 999999999: #input validation: must be a number
                                                                         #from 100000000 to 999999999
        if a == 'Add Member':
            x = addMember(b)
        elif a == 'View/Edit Member':
            x = editMember(b)
        else:
            x = validateTerm(b)
    else:
        msgbox(msg='Invalid ID Number.  Must be exactly 9 digits long, only numbers 0-9.')


    
    


        
        

