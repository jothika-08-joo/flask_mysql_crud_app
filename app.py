from flask import request, render_template, url_for, redirect, Flask, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import pooling
from functools import wraps

app = Flask(__name__)
app.secret_key = "supersecret"


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'mydatabase'
}
#create a connection pool
db_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **db_config
)

def get_db():
    if 'db' not in g:
        g.db = db_pool.get_connection()
    return g.db   

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("please login to access this page")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function         


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method=='GET':
        return render_template("signup.html")
    username=request.form.get('username','').strip()
    password=request.form.get('password','')
    if not username or not password:
        flash(" Enter your name and password are required")
        return redirect(url_for('signup'))

    db = get_db()
    cursor=db.cursor()
    cursor.execute("select id from users where username=%s",(username, ))
    existing_user=cursor.fetchone()

    if existing_user:
        cursor.close()
        flash("username is already exist")
        return redirect(url_for('signup'))

    password_hash=generate_password_hash(password) 
    cursor.execute("insert into users (username, password_hash) values(%s, %s)",
    (username, password_hash)
    )    
    db.commit()
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
    db = get_db()    
    cursor=db.cursor()
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
@login_required
def add():
    return render_template('add_tasks.html')
 
@app.route('/add_tasks', methods=['POST'])
@login_required
def add_tasks():
    user_id=session['user_id']    
    title=request.form.get('title', '').strip()
    completed= "completed" if request.form.get('completed')=="1" else "pending"
    if not title:
        flash("enter a title")
        return redirect(url_for('add'))
    db =  get_db()    
    cursor=db.cursor()
    cursor.execute("INSERT INTO todo (title, completed, user_id) VALUES (%s, %s, %s)",
    (title, completed, user_id)
    )
    db.commit()
    cursor.close()
    return redirect('/get_tasks')

@app.route('/get_tasks',  methods=['GET'])
@login_required
def get_tasks():
    user_id=session['user_id']    
    db = get_db()
    cursor=db.cursor()
    cursor.execute(("select * from todo where user_id =%s"),
    (user_id, ))
    tasks=cursor.fetchall()
    cursor.close()
    return render_template('view_tasks.html', tasks=tasks)
    
@app.route('/update/<int:id>')
@login_required
def update(id):
    user_id=session['user_id']
    db = get_db()    
    cursor=db.cursor()
    cursor.execute(
        "select * from todo where user_id=%s AND id=%s",
        (user_id, id)
    )
    task=cursor.fetchone()
    cursor.close()
    return render_template("update_tasks.html", task=task)

@app.route('/update_tasks/<int:id>', methods=['POST'])
@login_required
def update_tasks(id):
    user_id=session['user_id']   
    title=request.form['title']
    completed="completed" if request.form.get('completed')=="1" else "pending"
    db = get_db()
    cursor=db.cursor()
    cursor.execute(
        "UPDATE todo SET title=%s, completed=%s where user_id=%s AND id=%s",
        (title, completed, user_id, id)
        )
    db.commit()
    cursor.close()
    return redirect('/get_tasks')


@app.route('/delete_tasks/<int:id>', methods=['POST'])
@login_required
def delete_tasks(id):
    user_id=session['user_id']    
    db = get_db()
    cursor=db.cursor()
    cursor.execute(
        "DELETE FROM todo WHERE user_id=%s AND id=%s",
        (user_id, id)
    )
    db.commit()
    cursor.close()
    return redirect('/get_tasks')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash("successfully logged out")
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
        return redirect(url_for('get_tasks'))
    
    
        

    

if __name__=='__main__':
    print("connecting to db..")
    app.run(debug=True)
