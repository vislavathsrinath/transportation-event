# Import necessary libraries
from flask import Flask, render_template, request
import sqlite3
from gevent.pywsgi import WSGIServer

# Create Flask app
app = Flask(__name__)

# Function to get events by person ID
def get_db():
    conn = sqlite3.connect('Transportation.db')
    return conn

 #   try:
        # Replace 'events' and 'time' with actual column names in your database
      #  cursor.execute("SELECT time, type, link FROM Events WHERE person = ? ORDER BY time", (person_id,))
       # events = cursor.fetchall()
       # print(events)
   # except sqlite3.Error as e:
    #    print(f"Error fetching events: {e}")
    #    events = None  # You might want to return a specific value or raise an exception here

  #  conn.close()
   # return events

#@app.route('/')
#def search():
    #person_id = request.form.get('person_id')
    #events = get_events_by_person(person_id)
#    return render_template('index.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/searchbyperson')
def search_by_person():
    person_id = request.args.get('person_id')  
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Events WHERE person=?", [person_id])
    events = cur.fetchall()
    conn.close()
    return render_template('result.html', events=events)
    
@app.route('/searchbylink')
def search_by_link():
    link_id = request.args.get('link_id')
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Events WHERE link = ? ORDER BY time", [link_id]) 
    events = cur.fetchall()
    conn.close()
    return render_template('result.html', events=events)

@app.route('/linkdetails')
def link_details():
    link_id = request.args.get('link_id')
    conn = get_db()
    cur = conn.cursor()
    query = "SELECT freespeed, capacity, modes FROM Links WHERE link_id = '%s'"
    cur.execute(query % link_id) 
    events = cur.fetchall()
    print(events)
    conn.close()
    return render_template('result.html', events=events)

@app.route('/timerange')
def events_in_time_range():
    link_id = request.args.get('link_id')
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Events WHERE link = ? AND time BETWEEN ? AND ? ORDER BY time", [link_id]) 
    events = cur.fetchall()
    print(events)
    conn.close()
    return render_template('result.html', events=events)


# Run the application
if __name__ == '__main__':
    app.run(debug= True)