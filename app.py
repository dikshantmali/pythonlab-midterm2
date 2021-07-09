from flask import Flask,render_template,request
import sqlite3
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add')
def add():
    return render_template("add.html")

@app.route('/savedetails', methods=['POST','GET'])
def savedetails():
    mag='msg'
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]  
            phonenumber = request.form["phonenumber"]
            seminarname = request.form["seminarname"]
            noofperson = request.form["noofperson"]
            with sqlite3.connect("Hall.db") as con:  
                cur = con.cursor()   
                cur.execute("INSERT into Hall (name, email, phonenumber,seminarname,noofperson) values (?,?,?,?,?)",(name,email,phonenumber,seminarname,noofperson))  
                con.commit()  
                msg = "Hall Entry successfully Added"   
        except:
            # con.rollback()      
            msg = "We can not add the seminar Hall to the list"
        finally: 
            return render_template("success.html", msg=msg) 
        con.close()

@app.route("/view")  
def view():  
    con = sqlite3.connect("Hall.db")
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Hall")   
    rows = cur.fetchall()  
    return render_template("view.html",rows = rows)


@app.route("/delete")
def delete():
    return render_template("delete.html")


@app.route("/deleterecord", methods = ["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("Hall.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from Hall where id = ?", id)
            msg = "Seminar Hall Successfully Removed"
        except:
            msg = "can't be deleted" 
        finally:
            return render_template("delete_record.html", msg=msg)


if __name__ == "__main__":
    app.run(debug = True)