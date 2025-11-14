from flask import Flask, render_template, request, redirect, url_for
import os
import mysql.connector
from mysql.connector import errors

app = Flask(__name__)

# Read DB config from environment to match data.py
DB_CONFIG = {
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', ''),
    'host': os.environ.get('MYSQL_HOST', '127.0.0.1'),
    'port': int(os.environ.get('MYSQL_PORT', 3306)),
    'database': os.environ.get('MYSQL_DATABASE', 'event_management'),
    'charset': 'utf8mb4',
}


def get_db_connection():
    """Return a mysql.connector connection. Caller should close it.

    Rows are returned as dictionaries using cursor(dictionary=True).
    """
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Add Venue
@app.route('/add_venue', methods=['GET', 'POST'])
def add_venue():
    if request.method == 'POST':
        venue_name = request.form['VenueName']
        location = request.form['Location']
        capacity = request.form['Capacity']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Venue (VenueName, Location, Capacity) VALUES (%s, %s, %s)',
                       (venue_name, location, capacity))
        conn.commit()
        cursor.close()
        conn.close()

        # Show success message
        return render_template('success.html', message='Venue data inputted successfully!')

    return render_template('add_venue.html')

# Add Event
@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        event_name = request.form['EventName']
        event_date = request.form['EventDate']
        event_time = request.form['EventTime']
        venue_id = request.form['VenueID']
        organizer_id = request.form['OrganizerID']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Event (EventName, EventDate, EventTime, VenueID, OrganizerID) VALUES (%s, %s, %s, %s, %s)',
                       (event_name, event_date, event_time, venue_id or None, organizer_id or None))
        conn.commit()
        cursor.close()
        conn.close()

        # Show success message
        return render_template('success.html', message='Event data inputted successfully!')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Venue')
    venues = cursor.fetchall()
    cursor.execute('SELECT * FROM Organizer')
    organizers = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('add_event.html', venues=venues, organizers=organizers)

# Add Participant
@app.route('/add_participant', methods=['GET', 'POST'])
def add_participant():
    if request.method == 'POST':
        participant_name = request.form['ParticipantName']
        email = request.form['Email']
        phone = request.form['Phone']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Participant (ParticipantName, Email, Phone) VALUES (%s, %s, %s)',
                       (participant_name, email, phone))
        conn.commit()
        cursor.close()
        conn.close()

        # Show success message
        return render_template('success.html', message='Participant data inputted successfully!')

    return render_template('add_participant.html')

# View Venues
@app.route('/view_venues')
def view_venues():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Venue')
    venues = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_venues.html', venues=venues)

# View Events
@app.route('/view_events')
def view_events():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Event')
    events = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_events.html', events=events)

# View Participants
@app.route('/view_participants')
def view_participants():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Participant')
    participants = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_participants.html', participants=participants)

if __name__ == '__main__':
    app.run(debug=True)
