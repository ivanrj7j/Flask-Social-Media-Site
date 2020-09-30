from flask import Flask
from flask import *
from flask import sessions
from hashlib import md5
from flask_sqlalchemy import *
from datetime import datetime
from sqlalchemy import desc

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


class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    message = db.Column(db.String())
    typ = db.Column(db.String())
    date = db.Column(db.DateTime(), default=datetime.now())

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String())
    user = db.Column(db.String())
    mess = db.Column(db.String())
    date = db.Column(db.DateTime(), default=datetime.now())

class Frnds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower = db.Column(db.String())
    user = db.Column(db.String())
    date = db.Column(db.DateTime(), default=datetime.now())
    

@app.route('/')
def hello():
    if "email" in session:
        email = session['email']
        profile = User.query.filter_by(email=email).first()
        profile = profile.pic
        name = session['name']
        log= True
        notifications = Notifications.query.filter_by(email=email).order_by(desc(Notifications.id)).all()
        totn = str(len(notifications))
    else:
        email = "Me"
        log= False
        profile = "profile/default.JPG"
        name = 'Me'
        notifications = [{'date':'hi', 'message':'wow'}]
        totn=0
    return render_template('index.html', title='Softalk', log=log, pic=profile, name=name, notifications=notifications[:3], totaln=totn)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if "email" in session:
        return redirect('/')
    else:
        email = "Me"
        log= False
    return render_template('signup.html', title='Softalk', log=False)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
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
            notifications = Notifications.query.filter_by(email=email).order_by(desc(Notifications.id)).all()
            totn = str(len(notifications))
        else:
            email = "Me"
            log= False
            name = "name"
            notifications = [{'date':'hi', 'message':'wow'}]
            totn=0
        return render_template('search.html', log=log, title='Results for '+querry, email=email, name=name, pic=profile, users=results, notifications=notifications[:3], totaln=totn)
    else:
        return redirect('/')
   
   
@app.route('/view/<email>', methods=['GET', 'POST'])
def view(email):
    if "email" in session and "name" in session:
        log = True
        pic = User.query.filter_by(name=session['name']).first()
        pic = pic.pic
        em = session['email']
        name = session['name']
        notifications = Notifications.query.filter_by(email=email).order_by(desc(Notifications.id)).all()
        totn = str(len(notifications))
    else:
        log = False
        pic = "profile/default.JPG"
        em = 'Email'
        name = 'Name'
        notifications = [{'date':'hi', 'message':'wow'}]
        totn=0
    user_name = User.query.filter_by(email = email).first()
    if user_name == None:
        return redirect('/')
    check = Frnds.query.filter_by(user=email, follower=em).first()
    if check == None:
        frnds = False
    else:
        frnds = True
    # user = 
    return render_template('view.html', log=log, title = user_name.name, pic=pic, result=user_name, email=em, f=frnds, notifications=notifications[:3], totaln=totn)


@app.route('/frm', methods=['GET', 'POST'])
def frm():
    if request.method == "POST":
        follower = request.form['follower']
        user = request.form['user']
        action = request.form['action']
        if action == 'follow':
            
            friend = Frnds(follower=follower, user=user)
            db.session.add(friend)
            db.session.commit()
            message = f"Hey, {follower} has started to follow you!"
            notification = Notifications(email=user, message=message, typ='follow')
            db.session.add(notification)
            db.session.commit()
        elif action == 'unfollow':
            delete = db.engine.execute(f"DELETE FROM `frnds` WHERE `frnds`.`follower`='{follower}' AND `frnds`.`user`='{user}'")
            db.session.add(delete)
            db.session.commit()
        else:
            pass
        
        return f"{user} {follower}"
    else:
        pass

@app.route('/notifications', methods=['GET', 'POST'])
def noti():
    if "email" in session:
        profile = User.query.filter_by(email=session['email']).first()
        profile = profile.pic
        notifications = Notifications.query.filter_by(email=session['email']).order_by(desc(Notifications.id)).all()
        totn = str(len(notifications))
        return render_template('n.html', log=True, pic=profile, title = 'Notifications', email=session['email'], notifications=notifications[:3], totaln=totn, name=session['name'], content = notifications)
    else:
        return redirect('/')

@app.route('/friends', methods=['GET', 'POST'])
def friends():
    if "email" in session:
        profile = User.query.filter_by(email=session['email']).first()
        profile = profile.pic
        notifications = Notifications.query.filter_by(email=session['email']).order_by(desc(Notifications.id)).all()
        totn = str(len(notifications))
        follower = Frnds.query.filter_by(user=session['email']).order_by(desc(Frnds.id)).all()

        return render_template('f.html', log=True, pic=profile, title = 'Notifications', email=session['email'], notifications=notifications[:3], totaln=totn, name=session['name'], follower = follower)
    else:
        return redirect('/')

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if "email" in session:
        profile = User.query.filter_by(email=session['email']).first()
        profile = profile.pic
        notifications = Notifications.query.filter_by(email=session['email']).order_by(desc(Notifications.id)).all()
        totn = str(len(notifications))
        follower = Frnds.query.filter_by(user=session['email']).order_by(desc(Frnds.id)).all()
        following = Frnds.query.filter_by(follower=session['email']).order_by(desc(Frnds.id)).all()
        fdfsadf = db.engine.execute(f"SELECT * FROM `messages` WHERE `user`='{session['email']}' OR `sender`='{session['email']}' ORDER BY `id` DESC")
        return render_template('m.html', log=True, pic=profile, title = 'Notifications', email=session['email'], notifications=notifications[:3], totaln=totn, name=session['name'], follower = follower, following=following, mess=fdfsadf)
    else:
        return redirect('/')

@app.route('/message/<user>', methods=['GET', 'POST'])
def message(user):
    if "email" in session:
        cc = User.query.filter_by(email=user).first()
        if cc == None:
            return redirect('/')
        profile = User.query.filter_by(email=session['email']).first()
        profile = profile.pic
        notifications = Notifications.query.filter_by(email=session['email']).order_by(desc(Notifications.id)).all()
        totn = str(len(notifications))
        follower = Frnds.query.filter_by(user=session['email']).order_by(desc(Frnds.id)).all()
        following = Frnds.query.filter_by(follower=session['email']).order_by(desc(Frnds.id)).all()
        messages = db.engine.execute(f"SELECT * FROM `messages` WHERE `user`='{user}' AND `sender`='{session['email']}' OR `user`='{session['email']}' AND `sender`='{user}' ORDER BY `id` DESC")

        return render_template('message.html', log=True, pic=profile, title = 'Messages', email=session['email'], notifications=notifications[:3], totaln=totn, name=session['name'], follower = follower, following=following, me=user, messages=messages)
    else:
        return redirect('/')

@app.route('/sendm', methods=['GET', 'POST'])
def sendm():
    if request.method == 'POST':
        sender = request.form['sender']
        user = request.form['user']
        mess = request.form['mess']
        messit = Messages(sender=sender, user=user, mess=mess)
        db.session.add(messit)
        db.session.commit()
        notificm = f"Hey, {user}, {sender} sent you a message!"
        notification = Notifications(email=user, typ='message', message=notificm)
        db.session.add(notification)
        db.session.commit()

        return mess
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)