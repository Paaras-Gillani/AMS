SHJ INTERNATIONALS
Attendance Management System
============================

PROJECT OVERVIEW
----------------

This is a lightweight web-based Attendance Management System designed
for the floor manager of SHJ Internationals.

The system allows the manager to manage employees, record daily
attendance, schedule employee offs in advance, and review monthly
attendance information.

Only the manager can log in and manage the attendance records.


MAIN FEATURES
-------------

1. Manager Login
   - Simple manager username and password.
   - Only the manager can access the system.
   - Login credentials are currently stored in app.py.

2. Employee Management
   - Add new employees.
   - Store employee name and designation.
   - Edit employee information.
   - Mark employees as resigned/removed from the active employee list.

3. Daily Attendance
   - Select any date.
   - Mark each employee as:
       * Present
       * Absent
       * Off
   - Attendance is stored in the SQLite database.
   - Previously saved attendance can be viewed and updated.

4. Pre-Scheduled Offs
   - Manager can schedule an employee's off in advance.
   - Select the employee.
   - Select the date.
   - Enter the reason for the scheduled off.
   - Scheduled offs are displayed in a separate list.
   - Scheduled offs automatically appear as "Off" on the attendance
     page for the selected date.

5. Monthly Reports
   - Manager can select a month.
   - View attendance information for employees.
   - Present, absent and off records are stored for reporting.

6. Lightweight Design
   - Built using Python and Flask.
   - Uses SQLite for data storage.
   - No large frontend framework is required.
   - Basic CSS styling is included directly in app.py.
   - Suitable for lightweight hosting such as PythonAnywhere.


TECHNOLOGIES USED
-----------------

Python
Flask
SQLite
HTML
CSS


PROJECT STRUCTURE
-----------------

The project should have the following structure:

    app.py
    database.db
    requirements.txt
    README.txt
    static/
        logo.png


FILES
-----

app.py
    Main Flask application containing the website, database logic,
    authentication, attendance management, employee management,
    scheduled offs and reports.

database.db
    SQLite database containing employee, attendance and scheduled
    off information.

requirements.txt
    Contains the Python packages required to run the application.

README.txt
    Project documentation and setup information.

static/logo.png
    Company logo displayed in the website header.


DEFAULT LOGIN
-------------

Current default manager login:

Username:
    manager

Password:
    password123

IMPORTANT:
Change the username and password in app.py before using the system
for real office data.


DATABASE
--------

The application uses SQLite.

The database is automatically created when the application starts.

The main database tables are:

employees
    Stores employee information.

attendance
    Stores daily attendance records.

scheduled_offs
    Stores pre-scheduled employee offs and their reasons.


RUNNING LOCALLY
---------------

Install the required packages:

    pip install -r requirements.txt

Then start the application:

    python app.py

Open the address shown by Flask in your browser.


PYTHONANYWHERE DEPLOYMENT
-------------------------

The application can be hosted on PythonAnywhere.

Recommended project location:

    /home/USERNAME/

Upload the project files to the account.

Make sure the following exists:

    /home/USERNAME/app.py
    /home/USERNAME/database.db
    /home/USERNAME/requirements.txt
    /home/USERNAME/static/logo.png

Configure the PythonAnywhere Web application to use:

    app.py

The WSGI configuration should import the Flask application:

    from app import app as application

After changing files or configuration, reload the web application.


LOGO
----

The company logo should be placed inside:

    static/logo.png

The application automatically displays this logo in the website header.


IMPORTANT SECURITY NOTE
-----------------------

This application currently uses a simple hard-coded manager login.

The credentials are stored directly in app.py.

This approach is suitable for a simple internal/lightweight system,
but it is not recommended for a high-security production system.

If the application becomes more widely used, authentication should
be upgraded to use securely stored passwords and stronger security
controls.


BACKUP
------

The most important file containing attendance data is:

    database.db

Make regular backups of this file.

If the database file is lost or deleted, the stored employee,
attendance and scheduled-off records may be lost.


FUTURE IMPROVEMENTS
-------------------

Possible future features include:

- Edit and delete scheduled offs
- Weekly recurring offs
- Employee joining and resignation dates
- Employee promotion history
- Attendance search
- Better monthly reports
- CSV/Excel export
- Printable reports
- Dashboard with attendance statistics
- Mobile-friendly improvements
- Stronger authentication
- Database backup and restore
- Manager activity history


PROJECT PURPOSE
---------------

The purpose of this system is to provide SHJ Internationals with a
simple, fast and lightweight way for the floor manager to manage
employee attendance and scheduled offs from anywhere through a web
browser.
