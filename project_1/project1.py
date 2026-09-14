from pathlib import Path # pathlib = file path handle korar tool..  Path(__file__) = current file er path..  with_name("house_rent_project1.csv") = current file er sathe same folder e thaka "house_rent_project1.csv" file ta ke load korbe..

import pandas as pd # excel er moto table handle korar tool..  CSV porar jonno..
from sklearn.linear_model import LinearRegression #amdr AI brain er ekta tool.. Linear Regression model train korar jonno.. o line tene tene prediction shiukhe..

# 1. Data Load.. csv file ta ke table akare load krsi.. df=DataFrame, mane table..
csv_path = Path(__file__).with_name("house_rent_project1.csv")
df = pd.read_csv(csv_path)
print("Data:")
print(df.head()) #df.head() mane table er first 5 row print korbe..

# 2. Data dekhi
print(f"\nTotal bari: {len(df)} ta") # len(df) = total rows in the dataframe
print(f"Average vara: {df['rent'].mean():.0f} tk") # df['rent'].mean() = average value of the 'rent' column

# 3. Model ke shikhai
# X = input (rooms, size), y = output (rent)
X = df[['rooms', 'size_sqft']]
y = df['rent']

model = LinearRegression() #amdr AI brain er ekta tool.. Linear Regression model train korar jonno..
model.fit(X, y) #fit=eta mane shikhano.. model.fit(X, y) mane model ke shikhai input X theke output y shikhe..

print("\nModel training done!")


# 4. Model ke test kori
test_house = pd.DataFrame([[2, 700]], columns=['rooms', 'size_sqft']) # test_house = pd.DataFrame([[2, 700]], columns=['rooms', 'size_sqft']) mane amra ekta test house er data diyechi.. 2 ta room, 700 sqft size.. eta diye model ke test korbo..
predicted_rent = model.predict(test_house) # predicted_rent = model.predict(test_house) mane amdr AI brain ke bolchi, "ei test house er rent koto hobe?".. model.predict(test_house) mane model ke test house er data diye prediction korano..

print(f"\nPredicted rent for 2 rooms, 700 sqft: {predicted_rent[0]:.0f} tk") # predicted_rent[0] mane predicted rent er first value.. .0f mane decimal point chara print korbe..

test_house2 = pd.DataFrame([[3, 1000]], columns=['rooms', 'size_sqft'])
predicted_rent2 = model.predict(test_house2)
print(f"\nPredicted rent for 3 rooms, 1000 sqft: {predicted_rent2[0]:.0f} tk")

test_house3 = pd.DataFrame([[1, 300]], columns=['rooms', 'size_sqft'])
predicted_rent3 = model.predict(test_house3)
print(f"\nPredicted rent for 1 room, 300 sqft: {predicted_rent3[0]:.0f} tk")