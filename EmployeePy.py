
from flask import *
from flaskext.mysql import MySQL
#import pymysql

 
#mysql = MySQL()
app = Flask(__name__) #Initialize flask
mysql = MySQL() #instance of MySQL
#Database connection details
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app) #initialize mysql 

@app.route("/")  #Routes the application to start from 127.0.0.1:5000
def index():  
    return render_template("index.html"); #Index page
 
@app.route("/add")  #Redirects to add.html page
def add():  
    return render_template("add.html")  #Page to add employees

@app.route("/savedetails",methods = ["POST","GET"])  #add.html redirects to savedetails function
def saveDetails():  
    msg = "msg"  
    if request.method == "POST": #If method is post, capture the field values
        	Name = request.form["Name"]
        	Designation = request.form["Designation"]  
        	Address = request.form["Address"] 
        	Phone = request.form["Phone"] 
        	conn = mysql.connect() #establish connection
        	conn.autocommit("True") #Set autocommit to true
        	cursor = conn.cursor() 
        	cursor.execute("INSERT INTO test.employee_table (emp_name,emp_des,emp_addr,emp_phone) VALUES (%s,%s,%s,%s)",(Name,Designation,Address,Phone))
        	msg = "Employee successfully added"  
        	return render_template("success.html",msg = msg) #After inserting success.html page is rendered
        	cursor.close()      
        

@app.route("/view") #View page to list all the employees in the table
def view():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT * from test.employee_table")
	rows = cursor.fetchall()
	if rows is None:
	    return "No records available to display"
	else:
	    return render_template("view.html",rows = rows)
	cursor.close()
    
@app.route("/delete")  #delete directs to delete.html which captures the Employee name and redirects to deleterecord method
def delete():  
    return render_template("delete.html")  
 
@app.route("/deleterecord",methods = ["POST"])  
#@app.route("/deleterecord")
def deleterecord():  
    emp_name = request.form["Name"] 
    conn = mysql.connect()
    conn.autocommit("True")
    cur = conn.cursor()  
    param = '{}%'.format(emp_name) #captures the partial value input and formats to process wildcard search and then delete the record.
    cur.execute("delete from test.employee_table where emp_name like %s", (param,))
    msg = "Record successfully deleted"          
    return render_template("delete_record.html",msg = msg) 
    cur.close()

@app.route("/search")  #Redirects to search page
def search():  
    return render_template("search.html") 

@app.route("/searchrecord",methods = ["POST"])  
def searchrecord():  
    if request.method == "POST": #captures the values of Employee Name or Designation or Phone Number and searches the database
        Name = request.form["Name"]
        #Name = 'MukeshAmbani'
        #Name = '{}%'.format(request.form["Name"])
        #Designation = '{}%'.format(request.form["Designation"])  
        Designation = request.form["Designation"]
        Phone = request.form["Phone"]
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * from test.employee_table where emp_name like %s OR emp_des = %s OR emp_phone=%s", (Name,Designation,Phone))
        #cursor.execute("SELECT * from test.employee_table where emp_name = 'MukeshAmbani'")
        rows = cursor.fetchall()
        if rows is None:
            return "Search did not retrieve records"
        else:
            return render_template("view.html",rows = rows) #Renders the retrieved result to view.html
        cursor.close()


if __name__ == "__main__":
    app.run(debug = True)
