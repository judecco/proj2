from flask import Flask, render_template, request, redirect
import mysql.connector

db = mysql.connector.connect( host="localhost", user="root", password="root", database="manchester")

cursor = db.cursor()



application=Flask(__name__)

@application.route("/")
def homePage():
    cursor.execute("Select * from consultants")
    data=cursor.fetchall()
    return render_template("Homepage.html", records=data)

@application.route("/saveEditedForm", methods=["POST"])
def saveEditedForm():
    regno=request.form["regno"]
    name=request.form["na"]
    department=request.form["dept"]
    salary=request.form["sal"]
    subject=request.form["subject"]
    marks=request.form["marks"]

    sqlquery="update consultants set name='{0}', salary={1}, marks={2}, subject='{4}', dept='{5}' where regno={3}".format(name, salary, marks, regno, subject, department)
    cursor.execute(sqlquery)
    db.commit()
    return redirect("/")


@application.route("/editRecordForm/<regno>")
def editRecordForm(regno):
    cursor.execute("Select * from consultants where regno={0}".format(regno))
    data=cursor.fetchone()
    return render_template("EditForm.html", record=data)

@application.route("/filterrecords", methods=["POST"])
def filterrecords():
    if request.form["dept"]=="all":
        return redirect("/")
    else:
        cursor.execute("Select * from consultants where dept='{0}'".format(request.form["dept"]))
        data=cursor.fetchall()
        return render_template("Homepage.html", records=data)

@application.route("/filtersubject", methods=["POST"])
def filtersubject():
    if request.form["subject"]=="all":
        return redirect("/")
    else:
        cursor.execute("Select * from consultants where subject='{0}'".format(request.form["subject"]))
        data=cursor.fetchall()
        return render_template("Homepage.html", records=data)


@application.route("/addnewRecord")
def addNewRecord():
    return render_template("input.html")
    

@application.route("/saveRecord", methods=["POST"])
def saveRecord():
    cursor.execute("select ifnull(max(regno),0)+1 from consultants")
    newregno=cursor.fetchone()
    name=request.form["na"]
    department=request.form["dept"]
    salary=request.form["sal"]
    subject=request.form["subject"]
    marks=request.form["marks"]
    client=request.form["client"]
    sqlquery= "insert into consultants values({0}, '{1}', '{2}', {3}, '{4}', {5}, '{6}')".format(newregno[0], name, department, salary, subject, marks, client)
    cursor.execute(sqlquery)
    db.commit()
    return redirect("/")

@application.route("/deleteEmployee/<regno>")
def deleteEmployee(regno):
    cursor.execute("delete from consultants where regno={0}".format(regno))
    return redirect("/")

@application.route("/personaldetails/<regno>")
def personalInformation(regno):
    cursor.execute("Select * from consultants where regno={0}".format(regno))
    data=cursor.fetchone()
    return render_template("personalInformation.html", record=data)

application.run(debug=True)