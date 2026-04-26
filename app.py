from flask import request, jsonify, render_template, url_for, redirect, Flask, flash

import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecret"

con=mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='mydatabase'

)

@app.route('/add')
def add():
    return render_template('add_tasks.html')
 
@app.route('/add_tasks', methods=['POST'])
def add_tasks():
    title=request.form.get('title', '').strip()
    completed= 1 if request.form.get('completed')=="1" else "0"
    if not title:
        flash("enter a title")
        return redirect(url_for('add'))
    cursor=con.cursor()
    cursor.execute("INSERT INTO todo(title, completed) VALUES (%s, %s)",
    (title, completed)
    )
    con.commit()
    cursor.close()
    return redirect('/get_tasks')

@app.route('/get_tasks',  methods=['GET'])
def get_tasks():
    cursor=con.cursor()
    cursor.execute("select * from todo")
    tasks=cursor.fetchall()
    cursor.close()
    return render_template('view_tasks.html', tasks=tasks)

@app.route('/update/<int:id>')
def update(id):
    cursor=con.cursor()
    cursor.execute(
        "select * from todo where id=%s",
        (id, )
    )
    task=cursor.fetchone()
    cursor.close()
    return render_template("update_tasks.html", task=task)

@app.route('/update_tasks/<int:id>', methods=['POST'])
def update_tasks(id):
    title=request.form['title']
    completed=request.form['completed']
    cursor=con.cursor()
    cursor.execute(
        "UPDATE todo SET title=%s, completed=%s where id=%s",
        (title, completed, id)
        )
    con.commit()
    cursor.close()
    return redirect('/get_tasks')


@app.route('/delete_tasks/<int:id>', methods=['POST'])
def delete_tasks(id):
    cursor=con.cursor()
    cursor.execute(
        "DELETE FROM todo WHERE id=%s",
        (id, )
    )
    con.commit()
    cursor.close()
    return redirect('/get_tasks')

@app.route('/')
def home():
    
    return render_template("base.html")
    
    
        

    

if __name__=='__main__':
    print("connecting to db..")
    app.run(debug=True)