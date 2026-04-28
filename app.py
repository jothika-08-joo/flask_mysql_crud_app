from flask import request, jsonify, render_template, url_for, redirect, Flask, flash
from werkzeug.security import generate_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecret"

con=mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='mydatabase'

)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method=='GET':
        return render_template("signup.html")
    username=request.form.get('username','').strip()
    password=request.form.get('password','')
    if not username or not password:
        flash("please enter your name and password")
        return redirect('signup')

    cursor=con.cursor()
    cursor.execute("select id from users where username=%s",(username, ))
    existing_user=cursor.fetchone()

    if existing_user:
        cursor.close()
        flash("username is already exist")
        return redirect('signup')

    password_hash=generate_password_hash(password)   
    cursor=con.cursor()
    cursor.execute("insert into users (username, password_hash) values(%s, %s)",
    (username, password_hash)
    )    
    con.commit()
    cursor.close()
    flash("successfully signup")
    return redirect("/")

@app.route('/add')
def add():
    return render_template('add_tasks.html')
 
@app.route('/add_tasks', methods=['POST'])
def add_tasks():
    title=request.form.get('title', '').strip()
    completed= "completed" if request.form.get('completed')=="1" else "pending"
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
    completed="completed" if request.form.get('completed')=="1" else "pending"
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