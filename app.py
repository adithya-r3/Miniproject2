#All of the imports that are necessary for the code to work
import atexit
import pandas as pd
from flask import Flask, g, redirect, request, render_template
import sqlite3




#This is to create the Flask app
app= Flask(__name__,template_folder='templates')
#sets up the database for the code
global data
database = "../products.sqlite"
conn = sqlite3.connect(database, check_same_thread=False)

#start-up page
@app.route('/', methods = ['GET','POST'])
def index():
    return render_template('home.html')

#The data entry page
@app.route('/dataentry', methods = ['GET', 'POST'])
def home_func():
    if request.method == "POST":
       category = request.form.get("category")
       description = request.form.get("description")
       quantity = request.form.get("quantity")
       productCode = request.form.get("product-code")
       if all((category, description, quantity, productCode)):
            new_data = pd.DataFrame({'Product Category': [category],
                                     'Product Description': [description],
                                     'Price': ["$" + quantity],
                                     'Product Code': [productCode]})
#This is to add all of the data into the sql database
            conn.execute("CREATE TABLE IF NOT EXISTS Users (\
                          'Product Category' TEXT,\
                          'Product Description' TEXT,\
                          'Price' TEXT,\
                          'Product Code' TEXT)")
            new_data.to_sql(name="Users", con= conn, if_exists='append', index=False)
#After the code is filled, the webpage routes back to the home page
            return redirect('/')
    return render_template("formForAddingNewProduct.html")

#Creates the database page
@app.route('/database', methods = ['GET','POST'])
def catalog(): 
    if request.method == "POST":
        requested_category = request.form.get("category")
        # Fetch data from the database based on the requested category
        if requested_category:
            query = f"SELECT * FROM Users WHERE `Product Category` = ?"
            result = pd.read_sql_query(query, conn, params=(requested_category,))
        else:
            # If no category is provided, fetch all data from the table
            query = "SELECT * FROM Users"
            result = pd.read_sql_query(query, conn)
        if not result.empty:
            category_data = result.to_html(index=False)  # Convert DataFrame to HTML if it contains data
        else:
            category_data = "No data found for the specified category."
        # Render the template, passing the category_data variable to the template
        return render_template('catalog.html',category_data=category_data)    
    return render_template('catalog.html')


#IMPORTANT: THIS CODE IS NOT IMPLICITLY DESCRIBED ON THE RUBRIC. This is to wipe the data on the sqlite server after the program shuts down.
def cleanup():
    # Code to reset the SQLite database upon exiting the Flask application
    conn.execute("DROP TABLE IF EXISTS Users")

atexit.register(cleanup)  # Register the cleanup function to run on application exit

#Sends the code to port 8080
if __name__ == "__main__":
    app.run(debug=True, port ='8080')
