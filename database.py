# Importing necessary libraries
import mysql.connector
import pandas as pd

# Connecting MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    port=3306,
    password="mahvash14",
    database="CarValue"
)
# Creating a cursor object
cursor = mydb.cursor()

# Creating a new database schema
cursor.execute("CREATE DATABASE CarValue")

# Creating Car table in the CarValue database.
cursor.execute('''CREATE TABLE IF NOT EXISTS Car(
   vin VARCHAR(100) PRIMARY KEY NOT NULL,
   year INTEGER,
   make TEXT,
   model TEXT,
   trim TEXT
)''')

# Creating CarDescription table in the CarValue database.
cursor.execute('''CREATE TABLE IF NOT EXISTS CarDescription(
   carID VARCHAR(200) PRIMARY KEY NOT NULL,
   style TEXT,
   driven_wheels TEXT,
   engine TEXT,
   fuel_type TEXT,
   exterior_color TEXT,
   interior_color TEXT
)''')

# Creating Dealer table in the CarValue database.
cursor.execute('''CREATE TABLE IF NOT EXISTS Dealer(
   dID VARCHAR(100) PRIMARY KEY NOT NULL,
   dealer_name TEXT ,
   dealer_street TEXT,
   dealer_city TEXT,
   dealer_state TEXT,
   dealer_zip TEXT
)''')

# Creating Listing table in the CarValue database.
cursor.execute('''CREATE TABLE IF NOT EXISTS Listing(
   listingID VARCHAR(100) PRIMARY KEY NOT NULL,
   listing_price INTEGER,
   listing_mileage INTEGER,
   listing_status TEXT,
   used BOOLEAN,
   certified BOOLEAN,
   seller_website TEXT,
   first_seen_date DATE,
   last_seen_date DATE,
   dealer_vdp_last_seen_date DATE
)''')

# Creating Id table in the CarValue database.
cursor.execute('''CREATE TABLE IF NOT EXISTS Id(
   vin VARCHAR(100),
   carID VARCHAR(200),
   dID VARCHAR(100),
   listingID VARCHAR(100),
   FOREIGN KEY (vin) REFERENCES Car(vin),
   FOREIGN KEY (dID) REFERENCES Dealer(dID),
   FOREIGN KEY (listingID) REFERENCES Listing(listingID)
)''')

# Importing the text file
data = pd.read_csv("NEWTEST-inventory-listing-2022-08-17.txt", sep="|", encoding='utf-8')

# Creating a dataframe of the entire datafile and cleaning the null values
df = pd.DataFrame(data).fillna('')

# Creating dataframes for each entity
# The Car dataframe
Car_df = pd.DataFrame().assign(vin=df['vin'], year=df['year'], make=df['make'], model=df['model'],
                               trim=df['trim'])

# Creating unique IDs for the primary keys defined in the tables
# Unique id for the listing table is formed using the domain name of the seller_website
df['listingID'] = df['seller_website'].str.replace("https://", '').str.replace(".com", '').str.replace("www.", '') \
    .replace(" ", "UnknownListingID")

# Unique id for the dealer table is formed using the dealer_name and the dealer_zip
df['dID'] = (df['dealer_name'] + "_" + df['dealer_zip'].astype(str)).replace("_", "UnknownDealerID").str.replace(' ',
                                                                                                                 '')
# Unique id for the CarDescription table is formed using all the fields of the CarDescription table
df['carID'] = (df['style'] + "_" + df['driven_wheels'] + "_" + df['engine'] + "_" + df['fuel_type']
               + "_" + df['exterior_color'] + "_" + df['interior_color']).replace("_____", "UnknownCarID")

# CarDescription dataframe
CarDescription_df = pd.DataFrame().assign(carID=df['carID'], style=df['style'],
                                          driven_wheels=df['driven_wheels'],
                                          engine=df['engine'].fillna(''), fuel_type=df['fuel_type'],
                                          exterior_color=df['exterior_color'], interior_color=df['interior_color'])

# Dealer dataframe
Dealer_df = pd.DataFrame().assign(dID=df['dID'], dealer_name=df['dealer_name'], dealer_street=df['dealer_street'],
                                  dealer_city=df['dealer_city'], dealer_state=df['dealer_state'],
                                  dealer_zip=df['dealer_zip'])
# Listing dataframe
Listing_df = pd.DataFrame().assign(listingID=df['listingID'], listing_price=df['listing_price'],
                                   listing_mileage=df['listing_mileage'], listing_status=df['listing_status'],
                                   used=df['used'], certified=df['certified'], seller_website=df['seller_website'],
                                   first_seen_date=df['first_seen_date'], last_seen_date=df['last_seen_date'],
                                   dealer_vdp_last_seen_date=df['dealer_vdp_last_seen_date'])
# Id dataframe
Id_df = pd.DataFrame().assign(vin=df['vin'], carID=df['carID'], dID=df['dID'], listingID=df['listingID'])

# Dropping the duplicate values in all dataframes
Car_df.drop_duplicates(keep="first", inplace=True)
CarDescription_df.drop_duplicates(keep="first", inplace=True)
Dealer_df.drop_duplicates(keep="first", inplace=True)
Listing_df.drop_duplicates(keep="first", inplace=True)
Id_df.drop_duplicates(keep="first", inplace=True)

# Printing and checkin all the dataframes created
print(CarDescription_df.count())
print(Car_df)
print(CarDescription_df)
print(Dealer_df)
print(Listing_df)
print(Id_df)

# Importing dataframes to databases and committing
# Car_df to Car table
for row in Car_df.itertuples():
    cursor.execute("INSERT IGNORE INTO Car (vin, year, make, model, trim) values (%s, %s, %s, %s, %s)",
                   [row.vin,
                    row.year,
                    row.make,
                    row.model,
                    row.trim]
                   )
mydb.commit()

# CarDescription_df to CarDescription table
for row in CarDescription_df.itertuples():
    cursor.execute(
        "INSERT IGNORE INTO CarDescription (carID, style, driven_wheels, engine, fuel_type, exterior_color,interior_color) values (%s, %s, %s, %s, %s, %s, %s)",
        [row.carID,
         row.style,
         row.driven_wheels,
         row.engine,
         row.fuel_type,
         row.exterior_color,
         row.interior_color]
    )
mydb.commit()

# Dealer_df to Dealer table
for row in Dealer_df.itertuples():
    cursor.execute(
        "INSERT IGNORE INTO Dealer (dID,dealer_name, dealer_street, dealer_city, dealer_state, dealer_zip) values (%s, %s, %s, %s, %s, %s)",
        [row.dID,
         row.dealer_name,
         row.dealer_street,
         row.dealer_city,
         row.dealer_state,
         row.dealer_zip]
    )
mydb.commit()

# Listing_df to Listing table
for row in Listing_df.itertuples():
    cursor.execute(
        "INSERT IGNORE INTO Listing (listingID, listing_price, listing_mileage, listing_status, used, certified, seller_website, first_seen_date, last_seen_date, dealer_vdp_last_seen_date) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        [row.listingID,
         row.listing_price,
         row.listing_mileage,
         row.listing_status,
         row.used,
         row.certified,
         row.seller_website,
         row.first_seen_date,
         row.last_seen_date,
         row.dealer_vdp_last_seen_date]
    )
mydb.commit()

# Id_df to Id table
for row in Id_df.itertuples():
    cursor.execute("INSERT IGNORE INTO Id (vin, carID, dID,listingID) values (%s, %s, %s, %s)",
                   [row.vin,
                    row.carID,
                    row.dID,
                    row.listingID]
                   )

mydb.commit()

# Performing select queries to check all the database tables
query1 = "SELECT * from Car"
query2 = "SELECT * from CarDescription"
query3 = "SELECT * from Dealer"
query4 = "SELECT * from Listing"
query5 = "SELECT * from Id"

# Reading the SQL queries
q1 = pd.read_sql(query1, mydb)
q2 = pd.read_sql(query2, mydb)
q3 = pd.read_sql(query3, mydb)
q4 = pd.read_sql(query4, mydb)
q5 = pd.read_sql(query5, mydb)

# Printing and checking the database tables
print(q1)
print(q2)
print(q3)
print(q4)
print(q5)
