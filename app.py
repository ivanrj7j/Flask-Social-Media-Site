from flask import Flask
from flask import *
from flask import sessions
from hashlib import md5
from flask_sqlalchemy import *
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/softalk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'jfksfjfhjghjghfjghdjghkjgjhghkghdkgjhkgjhkgjh'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    password = db.Column(db.String())
    name = db.Column(db.String())
    following = db.Column(db.Integer, default=0)
    followers = db.Column(db.Integer, default=0)
    post = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime(), default=datetime.now())
    latitude = db.Column(db.String())
    longitude = db.Column(db.String())
    pic = db.Column(db.String(), default='profile/default.JPG')

    

@app.route('/')
def hello():
    if "email" in session:
        email = session['email']
        profile = User.query.filter_by(email=email).first()
        profile = profile.pic
        name = session['name']
        log= True
    else:
        email = "Me"
        log= False
        profile = "profile/default.JPG"
        name = 'Me'
    return render_template('index.html', title='Softalk', log=log, pic=profile, name=name)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if "email" in session:
        return redirect('/')
    else:
        email = "Me"
        log= False
    return render_template('signup.html', title='Softalk', log=False)

@app.route('/insert', methods=['GET', 'POST'])
def method_name():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        lat = request.form['lat']
        lon = request.form['lon']
        password = md5(password.encode('UTF-8')).hexdigest()
        try:
            result = User.query.filter_by(email=email).first()
            if result == None:
                user = User(email=email, password=password, name=name, latitude=lat, longitude=lon)
                db.session.add(user)
                db.session.commit()
                session["email"] = email
                session["name"] = name
                return 's'
            else:
                return 'f'
            user = User(email=email, password=password, name=name, latitude=lat, longitude=lon)
            db.session.add(user)
            db.session.commit()
            session["email"] = email
            session["name"] = name
            return 's'
        except:
            return 'f'
        return f"f"

    else:
        return redirect('/')
    
@app.route('/signout', methods=['GET', 'POST'])
def signout():
    if "email" in session and "name" in session:
        session.pop('email', None)
        session.pop('name', None)
        return redirect('/')
    else:
        
        return redirect('/')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if "email" in session:
        return redirect('/')
    else:
        email = "Me"
        log= False
    return render_template('signin.html', title='Softalk', log=False)

@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # name = request.form['name']
        lat = request.form['lat']
        lon = request.form['lon']
        password = md5(password.encode('UTF-8')).hexdigest()
        try:
            user = User.query.filter_by(email=email, password=password).first()
            if user == None:
                return 'f'
            else:
                session["email"] = email
                session["name"] = user.name
                return 's'
            return 's'
        except:
            return 'f'
        return f"f"

    else:
        return redirect('/')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.args.get('query'):
        querry = request.args.get('query')
        if "email" in session:
            log = True
            email = session['email']
            name = session['name']
            profile = User.query.filter_by(email=email).first()
            profile = profile.pic
            results = User.query.filter(User.name.like('%'+querry+'%')).all()
            
        else:
            email = "Me"
            log= False
            name = "name"
        return render_template('search.html', log=log, title='Results for '+querry, email=email, name=name, pic=profile, users=results)
    else:
        return redirect('/')
   
   
    

if __name__ == '__main__':
    app.run(debug=True)