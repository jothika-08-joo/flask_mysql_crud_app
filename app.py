from flask import jsonify, render_template, url_for, redirect, Flask
import mysql.connector

app = Flask(__name__)

con=mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='mydatabase'

)

@app.route('/get_tables', methods=['GET'])
def get_tables():
    cursor=con.cursor()
    cursor.execute("SHOW TABLES;")
    tables=[t[0] for t in cursor.fetchall()]
    cursor.close()
    return jsonify(tables)    

@app.route('/add_users')
def add_users():
    cursor=con.cursor()
    cursor.execute("INSERT INTO users(id,name) VALUES (1,'JOTHIKA')")
    con.commit()
    cursor.close()
    return "user added"

@app.route('/get_users')
def  get_users():
    cursor=con.cursor()
    cursor.execute(("SELECT * FROM users"))
    data=cursor.fetchall()
    con.commit()
    cursor.close()
    return jsonify(data)

@app.route('/update_users')
def update_users():
    cursor=con.cursor()
    cursor.execute("UPDATE users SET name='ARUN' WHERE id=1")
    con.commit()
    cursor.close()
    return "updated successfully"    

@app.route('/delete_users')
def delete_users():
    cursor=con.cursor()
    cursor.execute("DELETE FROM users WHERE id=1")
    con.commit()
    cursor.close()
    return "deleted successfully"


'''
@app.route('/')
def home():
    return render_template("base.html")
    return redirect(url_for("add_tasks"))
'''    
        

    

if __name__=='__main__':
    print("connecting to db..")
    app.run(debug=True)