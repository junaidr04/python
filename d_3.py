# pandas library import করছি, "pd" হলো pandas-এর short name/alias
import pandas as pd

data = {
    # আমরা একটা Python dictionary তৈরি করছি.. এটাকে আপাতত CSV file-এর মতো ভাবতে পারো
    'hours': [1, 2, 3, 4, 5, 6, 7],
    # "marks" হলো আরেকটা column..প্রতিটি hour-এর corresponding marks
    'marks': [35, 45, 55, 67, 75, 85, 92]
}

# dictionary-এর data দিয়ে একটি Pandas DataFrame তৈরি করছি, DataFrame = Table.. অনেকটা Excel table-এর মতো
df = pd.DataFrame(data)

# প্রথমে একটা heading print করছি
print("Amder Data:")

# পুরো DataFrame print করছি
print(df)