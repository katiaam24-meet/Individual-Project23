from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import calendar 
from datetime import datetime  
app = Flask(__name__, static_url_path='/static')



Config = {
  "apiKey": "AIzaSyA32hxUzry7M2jpqSLbmV8yzUIACfEC6Kg",
  "authDomain": "mydailylife-df3a4.firebaseapp.com",
  "databaseURL": "https://mydailylife-df3a4-default-rtdb.firebaseio.com",
  "projectId": "mydailylife-df3a4",
  "storageBucket": "mydailylife-df3a4.appspot.com",
  "messagingSenderId": "928894590486",
  "appId": "1:928894590486:web:f58e4052f0b4fe69565f37",
  "measurementId": "G-YFP1CHDLS5",
  "databaseURL" : "https://mydailylife-df3a4-default-rtdb.firebaseio.com/"
}

firebase =pyrebase.initialize_app(Config)
auth= firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
           login_session['user'] =auth.sign_in_with_email_and_password(email, password)
           return redirect(url_for('home'))
       except:
           error = "Authentication failed"
           return render_template("signin.html")
   else:
        return render_template("signin.html")



    


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']
        try:
            login_session['user'] =auth.create_user_with_email_and_password(email, password)
            user={}
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
            print(error)
    return render_template("signup.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

def index():
    return render_template('index.html')


reminders = []


@app.template_filter('enumerate')
def do_enumerate(iterable):
    return enumerate(iterable)

@app.route('/reminder', methods=['GET', 'POST'])
def reminder():
    if request.method == 'POST':
        reminder_text = request.form['reminder']
        if reminder_text:
            reminders.append(reminder_text)
            return redirect(url_for('reminder'))

    return render_template('reminders.html', reminders=reminders)

@app.route('/delete_reminder/<int:index>')
def delete_reminder(index):
    if 0 <= index < len(reminders):
        reminders.pop(index)
    return redirect(url_for('reminder'))




@app.route('/scheduling')
def calendar_view():
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    
    cal = calendar.monthcalendar(current_year, current_month)
    calendar_data = []
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append('')
            else:
                week_data.append(day)
        calendar_data.append(week_data)

    return render_template('scheduling.html', calendar_data=calendar_data)


@app.route('/add_event', methods=['POST','GET'])
def add_event():
    if request.method == 'POST':
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        event = {"name" : event_name, "date": event_date, "UID": login_session['user']['localId']}
        try:
            db.child('Events').push(event)
            return redirect(url_for('show_events'))
        except:
            print('KAtia is the problem')
    return render_template('scheduling.html')



@app.route('/events', methods=['GET', 'POST'])
def show_events ():
    events = db.child('Events').get().val()
    UID = login_session['user']['localId']
    filtered = []
    for key in events:
        if events[key]['UID'] == UID:
            filtered.append(events[key])
    return render_template('events.html', events = filtered)


@app.route('/contact', methods=['GET', 'POST'])
def contact ():
    return render_template('contact.html')

@app.route('/home', methods=['GET', 'POST'])
def home ():
    return render_template('home.html')


@app.route('/surprise', methods=['GET', 'POST'])
def surprise ():
    return render_template('about.html')

@app.route('/tips', methods=['GET', 'POST'])
def tips ():
    return render_template('life_tips.html')





if __name__ == '__main__':
    app.run(debug=True)