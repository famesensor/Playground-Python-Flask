from flask import Flask, render_template, request, redirect,url_for
import pymysql.cursors 

app = Flask(__name__)
conn = pymysql.connect('localhost','root','','studentdb')

@app.route("/")
def showData():
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM student")
        rows = cur.fetchall()
        return render_template('index.html', datas=rows)

@app.route("/insert",methods=['POST'])
def insert():
    if request.method=='POST' : 
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        with conn.cursor() as cursor:
            sql = "Insert into student(f_name,l_name,phone) value(%s,%s,%s)"
            cursor.execute(sql,(fname,lname,phone))
            conn.commit()
        return redirect(url_for('showData'))

@app.route("/student")
def showForm():
    return render_template('addstudent.html')

@app.route("/delete/<string:id_data>",methods=["GET"])
def delete(id_data):
    with conn:
        cur = conn.cursor()
        cur.execute("delete from student where s_id=%s",(id_data))
        conn.commit()
    return redirect(url_for('showData'))

@app.route("/update",methods=["POST"])
def update():
    if request.method=='POST' :
        s_id = request.form['id']
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        with conn.cursor() as cursor:
            sql = "update student set f_name = %s, l_name = %s, phone = %s where s_id = %s"
            cursor.execute(sql,(fname,lname,phone,s_id))
            conn.commit()
        return redirect(url_for('showData'))


if __name__ == "__main__" :
    app.run(debug=True)