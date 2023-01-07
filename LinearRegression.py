# Import necessary libraries
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# Reading the text file into a dataframe
df = pd.read_csv('test.txt', sep="|", encoding='utf-8')

# Removing the null values and replacing all the NaN values with 0
df2 = df.fillna(0)
nVal = df2.isnull().sum()

# the numerical values are stored in X
X = df2[['year', 'listing_mileage']]

# Make of the car is a categorical value hence OneHotEncoder is applied
encoder = OneHotEncoder()
make_encoded = encoder.fit_transform(df2[['make']])

# Concatenate both the numerical and categorical columns
X = pd.concat([X, pd.DataFrame(make_encoded.toarray())], axis=1)

# Price is our target variable
y = df2['listing_price']

# Applying the train test split and dividing the data into training data and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Applying the Linear Regression Model
model = LinearRegression()

# Model fitting on the training data
model.fit(X_train, y_train)


