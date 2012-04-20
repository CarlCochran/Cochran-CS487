from datetime import date
from easygui import *
import member


def addMember(num):
    msg = "Enter New Member Information"
    title = "Hi"
    msg = "Member Number: ",num
    fieldNames = ["Last Name","First Name","Middle Initial","Zip Code","Year Entered Service","Month Entered Service","Day Entered Service","Year Left Service","Month Left Service","Day Left Service"]
    fieldValues = []        #init to blank
    fieldValues = multenterbox(msg,title,fieldNames)

    while 1:
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            errmsg = errmsg + ('"%s" is a required field.' % fieldNames[i])
        if errmsg == "": break                      #no errors
        fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
        
    
    x = Member.add(num, lname, fname, mi, zipCode, startYear, startMonth, startDay, endYear, endMonth, endDay)
    
def editMember(num):
    print num
    

#Main Routine
msgbox(msg='Post 9/11 GI Bill Member and Accounting System')
while 1:
    a = choicebox(msg='Choose Mode',title='A',choices=('Add Member','Edit Member'))
    b = enterbox(msg='Enter 9-digit member number with no dashes.')
    if a == 'Add Member':
        addMember(b)
    else:
        editMember(b)




    
    


        
        

