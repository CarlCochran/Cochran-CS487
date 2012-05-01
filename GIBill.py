from easygui import *
import member
import MySQLdb as db


def addMember(num):
    msg = "Enter New Member Information"
    title = "Add New Member"
    msg = "Member Number: ",num
    fieldNames = ["Last Name","First Name","Middle Initial","Zip Code","Year Entered Service","Month Entered Service","Day Entered Service","Year Left Service","Month Left Service","Day Left Service"]
    fieldValues = []        #init to blank
    fieldValues = multenterbox(msg,title,fieldNames)

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
        desc = cur.description                            #for column headers
        msg = ""
        for field in range(11):
            msg += "%-20s %-20s\n" %(desc[field][0],str(row[field]))
        choices = ["Edit","Cancel"]
        reply = buttonbox(msg,choices=choices)
        if reply == "Cancel":
            cur.close()
            con.close()
            return None
        else:
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

            return x

    except db.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        return None        
  
    

#Main Routine
msgbox(msg='Post 9/11 GI Bill Member and Accounting System')
while 1:
    a = choicebox(msg='Choose Mode',title='A',choices=('Add Member','View/Edit Member'))
    if a == None:                                  #Cancel was clicked
        exit()
        
    b = enterbox(msg='Enter 9-digit member number with no dashes.')
    if a == 'Add Member':
        x = addMember(b)
    else:
        x = editMember(b)




    
    


        
        

