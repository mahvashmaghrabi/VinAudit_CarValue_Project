# Importing the necessary flask libraries
from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL

import LinearRegression
import numpy as np

app = Flask(__name__)

# Connecting the flask application to CarValue database
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mahvash14'
app.config['MYSQL_DATABASE_DB'] = 'CarValue'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()


#  First endpoint to the search page
@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        car_make = request.form['car_make']
        car_model = request.form['car_model']
        car_year = request.form['car_year']
        car_mileage = request.form['car_mileage']

        # Error handling and Validation
        if car_make == "" or car_model == "" or car_year == "":
            error_msg = "Please enter a valid car make/model and year value"
            return render_template('search.html', data="", avg="", error_msg=error_msg)
        if car_year == 0 or int(car_year) > 2023:
            error_msg = "Please enter a valid car year value"
            return render_template('search.html', data="", avg="", error_msg=error_msg)
        if car_mileage != "" and int(car_mileage) < 0:
            error_msg = "Please enter a valid car mileage value"
            return render_template('search.html', data="", avg="", error_msg=error_msg)

        # SQL query that gives the results according to the user input
        sql = "SELECT year, make, model, trim, listing_price, listing_mileage, dealer_city, dealer_state " \
              " FROM Car " \
              "INNER JOIN Id ON Car.vin = Id.vin " \
              "INNER JOIN Listing ON Id.listingID = Listing.listingID " \
              "INNER JOIN Dealer ON Id.dID = Dealer.dID " \
              "where year={} AND make='{}' AND model='{}';".format(car_year, car_make, car_model)

        # SQL query when the user enters the mileage which is an optional field
        if car_mileage != "" and int(car_mileage) > 0:
            sql = "SELECT year, make, model, trim, listing_price, listing_mileage, dealer_city, dealer_state " \
                  " FROM Car " \
                  "INNER JOIN Id ON Car.vin = Id.vin " \
                  "INNER JOIN Listing ON Id.listingID = Listing.listingID " \
                  "INNER JOIN Dealer ON Id.dID = Dealer.dID " \
                  "where year={} AND make='{}' AND model='{}' AND listing_mileage<{};" \
                .format(car_year, car_make, car_model, car_mileage)

        cursor.execute(sql)
        results = cursor.fetchall()

        search_price_total = 0

# Average and Estimated Prices
        for row in results:
            search_price_total = search_price_total + row[4]
        print(search_price_total)
        search_avg_price = search_price_total / len(results)
        print(search_avg_price)

        if car_mileage != "" and int(car_mileage) > 0:

            encodedMake = LinearRegression.encoder.transform([[car_make]]).toarray()
            input_data = np.concatenate([[[car_year, car_mileage]], encodedMake], axis=1)
            prediction = LinearRegression.model.predict(np.concatenate([input_data], axis=1))[0]
            print(f'Predicted price: {prediction:.2f}')

        else:
            prediction = "To get the estimated price give the mileage"

        return render_template('search.html', data=results, avg=search_avg_price, prediction=prediction)
    return render_template('search.html')


# Run and debug the flask application
if __name__ == '__main__':
    app.debug = True
    app.run()