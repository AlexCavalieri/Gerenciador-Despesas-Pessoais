from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Routes for adding, viewing, editing, and deleting expenses

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

@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    if request.method == 'GET':
        # Fetch expense details from the database based on the expense_id
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        expense = cursor.fetchone()
        conn.close()

        if expense:
            # Render a form pre-filled with expense details for editing
            return render_template('edit_expense.html', expense=expense)
        else:
            # Expense not found
            flash("Expense not found", "error")
            return redirect(url_for('expenses'))
    elif request.method == 'POST':
        # Get updated expense details from the form
        date = request.form['date']
        category = request.form['category']
        description = request.form['description']
        amount = request.form['amount']

        # Update the expense in the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE expenses SET date = ?, category = ?, description = ?, amount = ? WHERE id = ?", 
                        (date, category, description, amount, expense_id))
        conn.commit()
        conn.close()

        # Flash success message and redirect to expenses page
        flash("Expense successfully updated", "success")
        return redirect(url_for('expenses'))

@app.route('/delete_expense/<int:expense_id>')
def delete_expense(expense_id):
    # Delete the expense with the given expense_id from the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

    # Flash success message and redirect to expenses page
    flash("Expense successfully deleted", "success")
    return redirect(url_for('expenses'))

if __name__ == '__main__':
    app.run(debug=True)
