from flask import request, render_template, url_for, redirect, Flask, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecret"

def is_logged_in():
    return 'user_id' in session

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
        flash(" Enter your name and password are required")
        return redirect(url_for('signup'))

    cursor=con.cursor()
    cursor.execute("select id from users where username=%s",(username, ))
    existing_user=cursor.fetchone()

    if existing_user:
        cursor.close()
        flash("username is already exist")
        return redirect(url_for('signup'))

    password_hash=generate_password_hash(password)   
    cursor=con.cursor()
    cursor.execute("insert into users (username, password_hash) values(%s, %s)",
    (username, password_hash)
    )    
    con.commit()
    cursor.close()
    flash("successfully signup")
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='GET':
        return render_template('login.html')    
    username=request.form.get('username','').strip()
    password=request.form.get('password','')
    if not username or not password:
        flash("ENTER YOUR USERNAME AND PASSWORD")
        return redirect(url_for('login'))
    cursor=con.cursor()
    cursor.execute("select id, password_hash from users where username=%s",
    (username, ))  
    existing_person=cursor.fetchone()
    
    
    if not existing_person:
        cursor.close()
        flash("GO  AND SIGNUP")
        return redirect(url_for('signup'))
    
    c=existing_person[1]
    cursor.close()

    v=check_password_hash(c, password)
    if v:
        flash("successful login")
        session['user_id']=existing_person[0]
        return redirect(url_for('get_tasks'))
    else:
        flash("enter a correct password")
        return redirect(url_for('login'))
   
@app.route('/add')
def add():
    if not is_logged_in():
        flash("please login")
        return redirect(url_for('login'))
    return render_template('add_tasks.html')
 
@app.route('/add_tasks', methods=['POST'])
def add_tasks():
    if not is_logged_in():
        flash("please login")
        return redirect(url_for('login'))
    user_id=session['user_id']    
    title=request.form.get('title', '').strip()
    completed= "completed" if request.form.get('completed')=="1" else "pending"
    if not title:
        flash("enter a title")
        return redirect(url_for('add'))
    cursor=con.cursor()
    cursor.execute("INSERT INTO todo (title, completed, user_id) VALUES (%s, %s, %s)",
    (title, completed, user_id)
    )
    con.commit()
    cursor.close()
    return redirect('/get_tasks')

@app.route('/get_tasks',  methods=['GET'])
def get_tasks():
    if not is_logged_in():
        flash("please login")
        return redirect(url_for('login'))
    user_id=session['user_id']    
    cursor=con.cursor()
    cursor.execute(("select * from todo where user_id =%s"),
    (user_id, ))
    tasks=cursor.fetchall()
    cursor.close()
    return render_template('view_tasks.html', tasks=tasks)
    
@app.route('/update/<int:id>')
def update(id):
    if not is_logged_in():
        flash("please login")
        return redirect(url_for('login'))
    user_id=session['user_id']    
    cursor=con.cursor()
    cursor.execute(
        "select * from todo where user_id=%s AND id=%s",
        (user_id, id)
    )
    task=cursor.fetchone()
    cursor.close()
    return render_template("update_tasks.html", task=task)

@app.route('/update_tasks/<int:id>', methods=['POST'])
def update_tasks(id):
    if not is_logged_in():
        flash("please login")
        return redirect(url_for('login'))
    user_id=session['user_id']   
    title=request.form['title']
    completed="completed" if request.form.get('completed')=="1" else "pending"
    cursor=con.cursor()
    cursor.execute(
        "UPDATE todo SET title=%s, completed=%s where user_id=%s AND id=%s",
        (title, completed, user_id, id)
        )
    con.commit()
    cursor.close()
    return redirect('/get_tasks')


@app.route('/delete_tasks/<int:id>', methods=['POST'])
def delete_tasks(id):
    if not is_logged_in():
        flash("please login")
        return redirect(url_for('login'))
    user_id=session['user_id']    
    cursor=con.cursor()
    cursor.execute(
        "DELETE FROM todo WHERE user_id=%s AND id=%s",
        (user_id, id)
    )
    con.commit()
    cursor.close()
    return redirect('/get_tasks')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash("successfully logged out")
    return redirect(url_for('login'))

@app.route('/')
def home():
    if is_logged_in():
        return redirect(url_for('get_tasks'))
    
    return redirect(url_for('signup'))
    
    
        

    

if __name__=='__main__':
    print("connecting to db..")
    app.run(debug=True)