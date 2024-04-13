from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_expense')
def add_expense():
    return render_template('add_expense.html')

@app.route('/expenses')
def expenses():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    return render_template('expenses.html', expenses=expenses)

@app.route('/add_expense', methods=['POST'])
def add_expense_post():
    date = request.form['date']
    category = request.form['category']
    description = request.form['description']
    amount = request.form['amount']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)", (date, category, description, amount))
    conn.commit()
    conn.close()
    return redirect(url_for('expenses'))

if __name__ == '__main__':
    app.run(debug=True)
