(app.py content starts)
from flask import Flask, request, redirect, session, render_template_string
import sqlite3
from functools import wraps
from datetime import date, datetime

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET_KEY"

DATABASE = "database.db"

MANAGER_USERNAME = "manager"
MANAGER_PASSWORD = "password123"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.executescript("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        designation TEXT,
        status TEXT DEFAULT 'active'
    );

    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        date TEXT,
        status TEXT,
        UNIQUE(employee_id, date)
    );
    """)
    db.close()

init_db()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect("/")
        return f(*args, **kwargs)
    return wrap

BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>{{ title }}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { font-family: Arial; margin:20px; }
a { margin-right:10px; text-decoration:none; }
table { border-collapse:collapse; width:100%; }
th, td { border:1px solid #ccc; padding:8px; text-align:center; }
th { background:#f4f4f4; }
.present { background:#e6ffea; }
.absent { background:#ffe6e6; }
.off { background:#fff5cc; }
.today { border:2px solid #007bff; }
.nav { margin-bottom:10px; }
button { padding:6px 12px; }
</style>
</head>
<body>

{% if session.logged_in %}
<div class="nav">
<a href="/attendance">Attendance</a>
<a href="/employees">Employees</a>
<a href="/reports">Reports</a>
<a href="/logout">Logout</a>
</div>
<hr>
{% endif %}

{{ content }}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        if request.form["username"] == MANAGER_USERNAME and request.form["password"] == MANAGER_PASSWORD:
            session["logged_in"] = True
            return redirect("/attendance")
        error = "Invalid credentials"

    content = f"""
    <h2>Manager Login</h2>
    <p style="color:red">{error}</p>
    <form method="post">
        <input name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button>Login</button>
    </form>
    """
    return render_template_string(BASE_HTML, title="Login", content=content)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/employees", methods=["GET", "POST"])
@login_required
def employees():
    db = get_db()
    if request.method == "POST":
        db.execute("INSERT INTO employees (name, designation) VALUES (?,?)",
                   (request.form["name"], request.form["designation"]))
        db.commit()

    employees = db.execute(
        "SELECT * FROM employees WHERE status='active' ORDER BY name"
    ).fetchall()

    rows = ""
    for e in employees:
        rows += f"""
        <tr>
        <form method="post" action="/employees/edit/{e['id']}">
            <td><input name="name" value="{e['name']}"></td>
            <td><input name="designation" value="{e['designation'] or ''}"></td>
            <td>
                <button>Save</button>
                <a href="/employees/resign/{e['id']}"
                onclick="return confirm('Resign employee?')">Resign</a>
            </td>
        </form>
        </tr>
        """

    content = f"""
    <h2>Employees</h2>
    <form method="post">
        <input name="name" placeholder="Name" required>
        <input name="designation" placeholder="Designation">
        <button>Add</button>
    </form>
    <br>
    <table>
        <tr><th>Name</th><th>Designation</th><th>Action</th></tr>
        {rows}
    </table>
    """
    db.close()
    return render_template_string(BASE_HTML, title="Employees", content=content)

@app.route("/employees/edit/<int:id>", methods=["POST"])
@login_required
def edit_employee(id):
    db = get_db()
    db.execute("UPDATE employees SET name=?, designation=? WHERE id=?",
               (request.form["name"], request.form["designation"], id))
    db.commit()
    db.close()
    return redirect("/employees")

@app.route("/employees/resign/<int:id>")
@login_required
def resign_employee(id):
    db = get_db()
    db.execute("UPDATE employees SET status='resigned' WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect("/employees")

@app.route("/attendance", methods=["GET", "POST"])
@login_required
def attendance():
    db = get_db()
    selected_date = request.args.get("date", date.today().isoformat())

    if request.method == "POST":
        for k, v in request.form.items():
            if k.startswith("emp_"):
                emp_id = k.split("_")[1]
                db.execute(
                    "INSERT OR REPLACE INTO attendance (employee_id, date, status) VALUES (?,?,?)",
                    (emp_id, selected_date, v),
                )
        db.commit()
        db.close()
        return redirect(f"/attendance?date={selected_date}")

    employees = db.execute(
        "SELECT * FROM employees WHERE status='active' ORDER BY name"
    ).fetchall()

    records = db.execute(
        "SELECT employee_id, status FROM attendance WHERE date=?",
        (selected_date,)
    ).fetchall()

    amap = {r["employee_id"]: r["status"] for r in records}
    db.close()

    rows = ""
    for e in employees:
        cur = amap.get(e["id"], "present")
        rows += f"""
        <tr class="{cur}">
        <td>{e['name']}</td>
        <td><input type="radio" name="emp_{e['id']}" value="present" {"checked" if cur=="present" else ""}></td>
        <td><input type="radio" name="emp_{e['id']}" value="absent" {"checked" if cur=="absent" else ""}></td>
        <td><input type="radio" name="emp_{e['id']}" value="off" {"checked" if cur=="off" else ""}></td>
        </tr>
        """

    today_class = "today" if selected_date == date.today().isoformat() else ""

    content = f"""
    <h2>Attendance</h2>
    <form method="get">
        <input type="date" name="date" value="{selected_date}" class="{today_class}">
        <button>Load</button>
    </form><br>

    <form method="post" onsubmit="return confirm('Save attendance?')">
    <table>
        <tr><th>Name</th><th>Present</th><th>Absent</th><th>Off</th></tr>
        {rows}
    </table><br>
    <button>Save Attendance</button>
    </form>
    """
    return render_template_string(BASE_HTML, title="Attendance", content=content)

@app.route("/reports")
@login_required
def reports():
    db = get_db()
    month = request.args.get("month", datetime.today().strftime("%Y-%m"))
    start = f"{month}-01"
    end = f"{month}-31"

    data = db.execute("""
        SELECT e.name,
        SUM(a.status='present') p,
        SUM(a.status='absent') a,
        SUM(a.status='off') o
        FROM employees e
        LEFT JOIN attendance a
        ON e.id=a.employee_id AND a.date BETWEEN ? AND ?
        WHERE e.status!='resigned'
        GROUP BY e.id
    """, (start, end)).fetchall()

    db.close()

    rows = ""
    for r in data:
        total = (r["p"] or 0) + (r["a"] or 0) + (r["o"] or 0)
        pct = round((r["p"] / total * 100), 1) if total else 0
        cls = "absent" if pct < 75 else "present" if pct >= 95 else ""
        rows += f"""
        <tr class="{cls}">
        <td>{r['name']}</td>
        <td>{r['p'] or 0}</td>
        <td>{r['a'] or 0}</td>
        <td>{r['o'] or 0}</td>
        <td>{pct}%</td>
        </tr>
        """

    content = f"""
    <h2>Monthly Report</h2>
    <form>
        <input type="month" name="month" value="{month}">
        <button>Load</button>
    </form><br>

    <table>
    <tr><th>Name</th><th>Present</th><th>Absent</th><th>Off</th><th>%</th></tr>
    {rows}
    </table>
    """
    return render_template_string(BASE_HTML, title="Reports", content=content)

if __name__ == "__main__":
    app.run()
(app.py content ends)
