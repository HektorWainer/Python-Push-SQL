### This first part is just getting some random data froman API call
import requests
import pandas as pd

# API-endpoint
url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query?"

# Defining a params dict for the parameters to be sent to the API
params = {"fields" : "record_date,cusip,security_type,security_term,auction_date",
          "filter" : "record_date:gte:2022-01-01,record_date:lte:2022-12-31,security_type:in:(Bill,Note)",
          "format" : "csv",
          "page[size]": 1000 }

# Sending get request and saving the response as response object
r = requests.get(url = url, params = params)

# extracting data
data = r.content

# Saving the API data in a CSV
csv_file = open('data.csv', 'wb')
csv_file.write(data)
csv_file.close()

# Saving CSV data into df
df = pd.read_csv('data.csv')
df


### This part is the bit that pushes the data to the database table
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text

# Connect to the database - in this example I use sqllite to host a SQL instance in python as i dont have a database to connect to currently
engine = create_engine('sqlite://', echo=False)

# Write the DataFrame to the database in one go, can ammend the if_exists to append data to and add further checks to this script but for now just keeping it basic
with engine.begin() as connection:
  df.to_sql(name='Test', con=connection, if_exists='replace', index=False)

with engine.connect() as conn:
   SQL = conn.execute(text("SELECT * FROM Test")) # Get all of the data from the SQL table that i created in the cell above
   SQL_table = pd.DataFrame(SQL.fetchall())  # Create a DataFrame from the table in SQL
   SQL_table.columns = SQL.keys()  # Assign column names
   display(SQL_table) # Display table
