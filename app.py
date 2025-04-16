from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = "bookings.db"


def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            car TEXT NOT NULL,
            date TEXT NOT NULL,
            timeslot TEXT NOT NULL,
            UNIQUE(car, date, timeslot)
        )
    """)
    conn.commit()
    conn.close()


@app.route('/')
def index():
    cars = ["車1 - Zinger1", "車2 - Zinger2",
            "車3 - 小貨車", "車4 - 大藍", "車5 - 大白", "車6 - 小牛"]
    timeslots = ["上午", "下午"]
    return render_template("index.html", cars=cars, timeslots=timeslots)


@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    car = request.form['car']
    date = request.form['date']
    timeslot = request.form['timeslot']
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO bookings (name, car, date, timeslot) VALUES (?, ?, ?, ?)",
                       (name, car, date, timeslot))
        conn.commit()
    except sqlite3.IntegrityError:
        return "⚠️ 該車輛在該日期及時段已被預約"
    conn.close()
    return redirect(url_for('index'))


@app.route('/bookings')
def show_bookings():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, car, date, timeslot FROM bookings ORDER BY date, timeslot")
    data = cursor.fetchall()
    conn.close()
    return render_template("bookings.html", bookings=data)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
