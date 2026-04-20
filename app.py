from flask import request, jsonify, render_template, url_for, redirect, Flask
import mysql.connector

app = Flask(__name__)

con=mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='mydatabase'

)
 
@app.route('/add_tasks', methods=['POST'])
def add_tasks():
    data=request.get_json()
    cursor=con.cursor()
    cursor.execute("INSERT INTO todo(title, completed) VALUES (%s, %s)",
    (data['title'], data['completed'])
    )
    con.commit()
    cursor.close()
    return "user added"

@app.route('/get_tasks',  methods=['GET'])
def get_tasks():
    cursor=con.cursor()
    cursor.execute("select * from todo")
    tasks=cursor.fetchall()
    cursor.close()
    return jsonify(tasks)

@app.route('/update_tasks/<int:id>', methods=['PUT'])
def update_tasks(id):
    data=request.get_json()
    cursor=con.cursor()
    cursor.execute(
        "UPDATE todo SET title=%s, completed=%s where id=%s",
        (data['title'], data['completed'], id)
        )
    con.commit()
    cursor.close()
    return jsonify({"message":"updated successfully"})

@app.route('/delete_tasks/<int:id>', methods=['DELETE'])
def delete_tasks(id):
    cursor=con.cursor()
    cursor.execute(
        "DELETE FROM todo WHERE id=%s",
        (id, )
    )
    con.commit()
    cursor.close()
    return jsonify({"message":"deleted successfully"})
'''
@app.route('/')
def home():
    return render_template("base.html")
    return redirect(url_for("add_tasks"))
'''    
        

    

if __name__=='__main__':
    print("connecting to db..")
    app.run(debug=True)