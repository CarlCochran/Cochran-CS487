from easygui import *
import member
import MySQLdb as db
from datetime import *

def inputValidation(x):
    #Input Validation
    chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -')   #Valid alphabetic set
    numbers = set('0123456789')                                             #Valid numeric set
    errmsg = ""                                                     #Init to no errors
    d1valid = False
    d2valid = False
    
    for i in range(len(x.lname)):                            #Check for invalid characters in name
        if any ((c in chars) for c in x.lname[i]):
            continue
        else:
            errmsg += ('Last Name contains invalid characters.\n')
            break
    for i in range(len(x.fname)):
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


        
    msg = "Enter New Member Information"
    title = "Add New Member"
    msg = "Member Number: ",num
    fieldNames = ["Last Name","First Name","Middle Initial","Zip Code","Year Entered Service","Month Entered Service","Day Entered Service","Year Left Service","Month Left Service","Day Left Service"]
    fieldValues = []        #init to blank
    fieldValues = multenterbox(msg,title,fieldNames)

    
    #Check for fields left blank
    while 1:
        if fieldValues == None: return None
        errmsg = ""
        for i in range(len(fieldNames)):
            if i == 2:                               #Skip middle initial, not required
                continue
            if fieldValues[i].strip() == "":
                errmsg += ('"%s" is a required field.' % fieldNames[i])
        print errmsg
        if errmsg == "": break                      #no errors
        fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

                           

    #Prepare Input Validation   
    while 1:
        lname = fieldValues[0]
        fname = fieldValues[1]
        mi = fieldValues[2]
        zc = fieldValues[3]
        ye = fieldValues[4]
        me = fieldValues[5]
        de = fieldValues[6]
        yl = fieldValues[7]
        ml = fieldValues[8]
        dl = fieldValues[9]
      
        x = member.Member()
        x.add(num, lname, fname, mi, zc, ye, me, de, yl, ml, dl)
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
                    moLeft,daLeft) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % \
                    (x.memNum, x.lname, x.fname, x.mi, x.zipCode, x.startYear,\
                    x.startMonth, x.startDay, x.endYear, x.endMonth, x.endDay))
        con.commit()
        cur.close()
        con.close()

    except db.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])


    x = editMember(num)  
    return x


    
def editMember(num):

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
        for field in range(11):
            msg += "%-20s %-20s\n" %(desc[field][0],str(row[field]))
        choices = ["Edit","Cancel","Delete Record"]
        reply = buttonbox(msg,choices=choices)
        if reply == "Cancel":
            cur.close()
            con.close()
            return None
        elif reply == "Edit":
            x = member.Member()
            x.add(num, row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
            msg = "Enter New Member Information"
            title = "Edit Member Information"
            msg = "Member Number: ",x.memNum
            fieldNames = ["Last Name","First Name","Middle Initial","Zip Code","Year Entered Service", \
                          "Month Entered Service","Day Entered Service","Year Left Service", \
                          "Month Left Service","Day Left Service"]
            fieldValues = []
            fieldValues = multenterbox(msg,title,fieldNames,(x.lname,x.fname,x.mi,x.zipCode,x.startYear, \
                          x.startMonth,x.startDay,x.endYear,x.endMonth,x.endDay))

            #Check for fields left blank
            while 1:
                if fieldValues == None: break
                errmsg = ""
                for i in range(len(fieldNames)):
                    if fieldValues[i].strip() == "":
                        errmsg += ('"%s" is a required field.' % fieldNames[i])
                print errmsg
                if errmsg == "": break                      #no errors
                fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
            lname = fieldValues[0]
            fname = fieldValues[1]
            mi = fieldValues[2]
            zc = int(fieldValues[3])
            ye = int(fieldValues[4])
            me = int(fieldValues[5])
            de = int(fieldValues[6])
            yl = int(fieldValues[7])
            ml = int(fieldValues[8])
            dl = int(fieldValues[9])

      
            x = member.Member()
            x.add(num, lname, fname, mi, zc, ye, me, de, yl, ml, dl)
            print x.memNum, x.lname, x.fname, x.mi, x.zipCode, x.startYear, \
                  x.startMonth, x.startDay, x.endYear, x.endMonth, x.endDay


            cur.execute('INSERT INTO members (id,lname,fname,mi,zipcode,yrEntered,moEntered,daEntered,yrLeft, \
                            moLeft,daLeft) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % \
                            (x.memNum, x.lname, x.fname, x.mi, x.zipCode, x.startYear,\
                            x.startMonth, x.startDay, x.endYear, x.endMonth, x.endDay))
            con.commit()
            cur.close()
            con.close()

            x = editMember(num)
            return x

        else:
            a = buttonbox(msg = 'Are you sure you want to delete this record?\n%s %s %s'% (row[0], \
                        row[1], row[2]), title = 'Delete Record', choices=('Confirm','Cancel'), \
                        image=None)
            print num
            if a:
                cur.execute('DELETE FROM members WHERE id = %s' % num)
                con.commit()
            cur.close()
            con.close()
                        
    except db.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        return None        
  
    

#Main Routine
msgbox(msg='Post 9/11 GI Bill Member and Accounting System\n\tby Carl Cochran')
while 1:
    a = choicebox(msg='Choose Mode',title='Post 9/11 GI Bill Member and Accounting System', \
                  choices=('Add Member','View/Edit Member'))
    if a == None:                                  #Cancel was clicked, exit program
        exit()
        
    b = enterbox(msg='Enter 9-digit member number with no dashes.')
    if b == None:                                   #Cancel was clicked: return to main menu
        continue
    elif str.isdigit(b) and int(b) >= 100000000 and int(b) <= 999999999: #input validation: must be a number
                                                                         #from 100000000 to 999999999
        if a == 'Add Member':
            x = addMember(b)
        else:
            x = editMember(b)
    else:
        msgbox(msg='Invalid ID Number.  Must be exactly 9 digits long, only numbers 0-9.')


    
    


        
        

