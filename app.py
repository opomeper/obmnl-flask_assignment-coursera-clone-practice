""" CRUD Application Design using Additional Features in Flask """
# Import libraries
from flask import Flask, request, redirect, render_template, url_for

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route('/')
def get_transactions():
    """Retrieve all transactions and calculate the balance."""
    # Render the transactions template with the current transactions and balance
    balance = sum(transaction['amount'] for transaction in transactions) # Calculate the balance
    return render_template('transactions.html', transactions = transactions, balance = balance)

# Create operation
@app.route('/add/', methods=['GET', 'POST'])
def add_transaction():
    """ Add a new transaction."""
    # check if the request method is POST
    if request.method == 'POST':
        # Create a new transaction object using form field values
        transaction = {
            'id': len(transactions) + 1,            # Generate a unique ID
            'date': request.form['date'],           # Get the 'date' field value from the form
            'amount': float(request.form['amount']) # Get the 'amount' field value from the form and convert it to float
        }
        transactions.append(transaction) # Add the new transaction to the list

        # Redirect to the transactions list page after adding the new transaction
        return redirect(url_for('get_transactions'))

    # If the request method is GET, render the form template to display the add transaction form
    return render_template('form.html')


# Update operation
@app.route('/edit/<int:transaction_id>/', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Extract the updated data from the form
        date = request.form['date']             # Get the 'date' field value from the form
        amount = float(request.form['amount'])  # Get the 'amount' field value from the form and convert it to float

        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break
            
        return redirect(url_for('get_transactions'))

    for transaction in transactions:
        if transaction_id == transaction['id']:
            return render_template('edit.html', transaction = transaction)

# Delete operation
@app.route('/delete/<int:transaction_id>/')
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break

    return redirect(url_for('get_transactions'))

# Search operation
@app.route('/search/', methods=['GET', 'POST'])
def search_transactions():
    if request.method == 'POST':
        min_amount = float(request.form['min_amount'])
        max_amount = float(request.form['max_amount'])
        filtered_transactions = []
        
        for transaction in transactions:
            if min_amount <= transaction['amount'] <= max_amount:
                filtered_transactions.append(transaction)

        balance = sum(transaction['amount'] for transaction in filtered_transactions) # Calculate the filtered balance
        return render_template('transactions.html', transactions = filtered_transactions, balance = balance)

    return render_template('search.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
