# Import statements below: selecting different libraries that we want to import
from flask import render_template
from flask import Flask #import from flask class
from flask import request #import from request class, this will deal with the data that come through from the route
import connect
import psycopg2
import uuid #import uuid class, this will generate unique id number
from flask import redirect
from flask import url_for

app = Flask(__name__) # Create an instance of the class for our use

dbconn = None

def genID(): #generate version 4 which is make a random unique ID numbers
    return uuid.uuid4().fields[1]

def getCursor(): # create connection with database by using conn and get the query by using cursor
    global dbconn
    if dbconn == None:
        conn = psycopg2.connect(dbname=connect.dbname, user=connect.dbuser, password=connect.dbpass, host=connect.dbhost, port=connect.dbport)
        conn.autocommit = True
        dbconn = conn.cursor()
        return dbconn
    else:
        return dbconn

#each route is a decorator for flask to know which functon to call
@app.route("/") #dinoting default route and the route that will go to when get to top level url that being visting.
def home(): #home function that tells flask to return to the home template
    return render_template("home.html")

@app.route("/youth/")
def youth():
    cur = getCursor()
    getCursor().execute("select groupid, familyname, firstname, activitynightid, attendancestatus from Youthattendancetable6;")
    select_result = cur.fetchall()
    column_names = [desc[0] for desc in cur.description] #getting out all the description from each of the column that was selected by the query
    return render_template('youthname.html',youthresult=select_result, youthcols=column_names) #return to the templates and define variables for Jinja

@app.route('/youthname', methods=['GET']) #allow method get
def getyouthname():
    familyname = request.args.get("familyname") #when click on the familyname, get the information of this person
    cur = getCursor()
    cur.execute("select * from Youthattendancetable6 where familyname=%s", (familyname,)) ##execute the query, search on the familyname and passing in
    select_result = cur.fetchall() #get result of the query,get back all the results
    column_names = [desc[0] for desc in cur.description] #display the columns from the description
    return render_template('youthresult.html',youthresult=select_result, youthcols=column_names)


@app.route("/adult/")
def adult():
    cur = getCursor()
    getCursor().execute("select familyname, firstname, groupid, leftdate, activitynightid, attendancestatus, notes from Adultattendancetable3;")
    select_result = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    return render_template('adultname.html',adultresult=select_result, adultcols=column_names)

@app.route('/adultname', methods=['GET']) #allow method get
def getadultname():
    print(request.args)
    familyname = request.args.get("familyname")
    cur = getCursor()
    cur.execute("select * from Adultattendancetable3 where familyname=%s", (familyname,))
    select_result = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    return render_template('adultresult.html',adultresult=select_result, adultcols=column_names)

@app.route('/addnewnight', methods=['GET','POST']) #allow methods get and post
def addnewnight():
    if request.method == 'POST':     #when the form is submitted, come through the flask
        print(request.form)          #print the infomration from the form
        id = genID()                 #generate unique ID number for activitynightid
        print(id)
        groupid = request.form.get('groupid')             #getting the following informations from the form
        nighttitle = request.form.get('nighttitle')
        description = request.form.get('description')
        activitynightdate = request.form.get('activitynightdate')
        cur = getCursor()                #connect to database, then insert the information to activitynight
        cur.execute("insert into activitynight(activitynightid, groupid, nighttitle, description, activitynightdate) VALUES (%s,%s,%s,%s,%s);",(str(id), groupid, nighttitle, description, activitynightdate,))
        cur.execute("SELECT * FROM activitynight where activitynightid=%s",(str(id),)) #display the result for new added activity night
        select_result = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        return render_template('activitynight.html',activitynightresult=select_result, activitynightcols=column_names)
    else:
        return render_template('addnewnight.html')

@app.route('/member/update', methods=['GET', 'POST'])
def memberupdate():
    if  request.method == 'POST':
        attendancestatus = request.form.get('attendancestatus')
        activitynightid = request.form.get('activitynightid')
        cur = getCursor()    #once the form being filled in, connect to database, then update the information of the selected person
        cur.execute("UPDATE Youthattendancetable6 SET attendancestatus=%s where activitynightid=%s",(attendancestatus, activitynightid,))
        cur.execute("SELECT * FROM Youthattendancetable6 where activitynightid=%s", (activitynightid,))  #display the result
        select_result = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        print(f"{column_names}")
        return render_template('youthresult.html',youthresult=select_result, youthcols=column_names)
    else:
        return render_template('youthupdate.html')

@app.route('/adultmember/update', methods=['GET', 'POST'])
def adultupdate():
    if  request.method == 'POST':
        familyname = request.form.get('familyname')
        firstname = request.form.get('firstname')
        notes = request.form.get('notes')           #adult need to update their notes
        attendancestatus = request.form.get('attendancestatus')  #adult need to update their attendance status
        activitynightid = request.form.get('activitynightid')    
        cur = getCursor()
        cur.execute("UPDATE Adultattendancetable3 SET attendancestatus=%s, notes=%s where familyname =%s and activitynightid=%s",(attendancestatus, notes, familyname, activitynightid,))
        cur.execute("SELECT * FROM Adultattendancetable3 where familyname =%s", (familyname,))
        select_result = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        print(f"{column_names}")
        return render_template('adultresult.html',adultresult=select_result, adultcols=column_names)
    else:
        return render_template('adultupdate.html')

@app.route('/leftdate/update', methods=['GET', 'POST'])
def leftdateupdate():
    if  request.method == 'POST':
        leftdate = request.form.get('leftdate')      #adult need to update their leftdate
        familyname = request.form.get('familyname')
        firstname = request.form.get('firstname')
        cur = getCursor()
        cur.execute("UPDATE Adultattendancetable3 SET leftdate=%s where familyname=%s",(leftdate, familyname,))
        cur.execute("SELECT * FROM Adultattendancetable3 where familyname=%s", (familyname,))
        select_result = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        print(f"{column_names}")
        return render_template('adultresult.html',adultresult=select_result, adultcols=column_names)
    else:
        return render_template('leftdate.html')