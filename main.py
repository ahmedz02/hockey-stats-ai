from bs4 import BeautifulSoup
import requests
import pandas as pd 

url = "https://www.quanthockey.com/nhl/seasons/nhl-players-stats.html"
r = requests.get(url)
print(r)

soup= BeautifulSoup(r.text, 'html.parser')


table = soup.find("table")

tableheader = table.find("tr", class_="orange")

column_titles = [th.text.strip() for th in tableheader.find_all('th')]
column_titles = [title for title in column_titles if title.strip() != '']
print("Column Titles:", column_titles)  # Print column titles to ensure no empty column



df = pd.DataFrame(columns= column_titles)


column_tabledata= table.find_all("tr")[2:]

for row in column_tabledata:
    row_data = row.find_all(['td', 'th'])
    individual_row_data = [data.text.strip() for data in row_data]

    individual_row_data = [item for item in individual_row_data if item]

    if len(individual_row_data) < len(df.columns):
        while len(individual_row_data) < len(df.columns):
            individual_row_data.append(None)  # Fill missing columns

    if len(individual_row_data) > len(df.columns):
        individual_row_data = individual_row_data[:len(df.columns)]  # Trim extra values

    # Append the row to the DataFrame
    df.loc[len(df)] = individual_row_data

print(df.head(50))

df.to_csv("nhl_player_stats.csv", index=False)

