from flask import request, render_template, url_for, redirect, Flask, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import pooling
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')


db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', 3306))
}

# Create a connection pool
try:
    db_pool = pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,
        **db_config
    )
except mysql.connector.Error as err:
    print(f"Error creating connection pool: {err}")
    db_pool = None

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
    elif len(username)>=100 or len(password)>=10:
        flash("ENTER THE USERNAME WITHIN 100 CHAR AND PASSWORD 10 CHAR")  
        return(redirect(url_for('signup')))  
    elif not username.isalnum():
        flash("ENTER ONLY CHARACTERS AND NUMBERS AS A USERNAME")  
        return(redirect(url_for('signup')))  
    try:    
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
    except mysql.connector.Error as err:
        print(f"error:{err}")
        flash("DATABASE ERROR TRY AGAIN")
        return redirect(url_for('signup'))
    finally:
        if 'cursor' in locals():
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
    try:    
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
    except mysql.connector.Error as err:
        print(f"ERROR:{err}")
        flash("DATABASE ERROR TRY AGAIN")
        return redirect(url_for('login'))
    finally:
        if 'cursor' in locals():
            cursor.close()
                

   
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
    elif len(title)>20:
        flash("ENTER A TASK WITH IN 20 CHARS")
        return redirect(url_for('add'))   
    try:     
        db =  get_db()        
        cursor=db.cursor()
        cursor.execute("INSERT INTO todo (title, completed, user_id) VALUES (%s, %s, %s)",
        (title, completed, user_id)
        )
        db.commit()
    except mysql.connector.Error as err:
        print(f"ERROR:{err}")
        flash("database connecting error try again")
        return redirect(url_for('add'))
    finally:      
        if 'cursor' in locals():
            cursor.close()
    return redirect('/get_tasks') 

@app.route('/get_tasks',  methods=['GET'])
@login_required
def get_tasks():
    user_id=session['user_id']    
    try:
        db = get_db()
        cursor=db.cursor()
        cursor.execute(("select * from todo where user_id =%s"),
        (user_id, ))
        tasks=cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"ERROR:{err}")
        flash("DB ERROR TRY AGAIN")
        return redirect(url_for('get_tasks'))  
    finally:
        if 'cursor' in locals():
             cursor.close()
    return render_template('view_tasks.html', tasks=tasks)
    
@app.route('/update/<int:id>')
@login_required
def update(id):
    user_id=session['user_id']
    try:
        db = get_db()    
        cursor=db.cursor()
        cursor.execute(
        "select * from todo where user_id=%s AND id=%s",
        (user_id, id)
        )
        task=cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"ERROR:{err}")
        flash("database connecting error try again")
        return redirect(url_for('get_tasks'))
    finally:   
        if 'cursor' in locals():   
             cursor.close()
    return render_template("update_tasks.html", task=task)

@app.route('/update_tasks/<int:id>', methods=['POST'])
@login_required
def update_tasks(id):
    user_id=session['user_id']   
    title=request.form['title']
    if not title:
        flash("ENTER A TITLE")
        return redirect(url_for('get_tasks'))
    completed="completed" if request.form.get('completed')=="1" else "pending"
    try:
        db = get_db()
        cursor=db.cursor()
        cursor.execute(
            "UPDATE todo SET title=%s, completed=%s where user_id=%s AND id=%s",
            (title, completed, user_id, id)
            )
        db.commit()
    except mysql.connector.Error as err:
        print(f"ERROR:{err}")
        flash("database connecting error try again")
        return redirect(url_for('get_tasks'))    
    finally:   
        if 'cursor' in locals():   
             cursor.close()    
    return redirect(url_for('get_tasks'))


@app.route('/delete_tasks/<int:id>', methods=['POST'])
@login_required
def delete_tasks(id):
    user_id=session['user_id']  
    try:  
        db = get_db()
        cursor=db.cursor()
        cursor.execute(
            "DELETE FROM todo WHERE user_id=%s AND id=%s",
            (user_id, id)
        )
        db.commit()
    except mysql.connector.Error as err:
        print(f"ERROR",{err})    
        flash("DATABASE ERROR TRY AGAIN")
        return redirect(url_for('get_tasks'))
    finally:  
        if 'cursor' in locals():
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
    
    
        

    

def init_db():
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        # Create Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL
            )
        """)
        # Create Todo table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todo (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(20) NOT NULL,
                completed VARCHAR(20) DEFAULT 'pending',
                user_id INT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        db.commit()
        print("Database initialized successfully!")
    except mysql.connector.Error as err:
        print(f"Error initializing database: {err}")
        raise err # Re-raise to catch it in __main__
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()
        db.close()

if __name__=='__main__':
    try:
        print("Initializing database...")
        init_db()
    except Exception as e:
        print(f"Pre-start database check failed: {e}")
        
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000, debug=True)
