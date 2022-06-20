#Imports
import requests
from bs4 import BeautifulSoup
import mysql.connector

#Build Database
# importing required libraries

# dataBase = mysql.connector.connect(
# host="db",
# user="jb",
# password="1"
# )

# # preparing a cursor object
# cursorObject = dataBase.cursor()

# # creating database
# cursorObject.execute("CREATE DATABASE nba")


#Connecting to database
dataBase = mysql.connector.connect(
host ="mysql",
user ="mj",
passwd ="23",
  database = "nba"
)

# preparing a cursor object
cursorObject = dataBase.cursor()

#Start at 1950 season end at 2022 season
for season in range(1950, 2023):
    #Scraping for conent
    #Set url using season
    url = f'https://www.basketball-reference.com/leagues/NBA_{season}_per_game.html'
    #Pull and clean data for database creation
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all(class_="full_table")
    head = soup.find(class_="thead")
    column_names_raw = [head.text for item in head][0]
    column_names_clean = column_names_raw.split('\n')[2:-1]
    column_names_SQL = []
    for i in column_names_clean:
        column_names_SQL.append("`")
        column_names_SQL.append(i)
        column_names_SQL.append("`")
        column_names_SQL.append(" DECIMAL(6,3),")
    column_names_SQL[3] = " VARCHAR(50),"
    column_names_SQL[7] = " VARCHAR(20),"
    column_names_SQL[15] = " VARCHAR(20),"
    column_names_SQLf = ''
    for i in column_names_SQL:
        column_names_SQLf += i

    #Building table

    seasonStats = f"CREATE TABLE `{season}` " + "(" + column_names_SQLf[:-1] + ")"

    # table created
    cursorObject.execute(seasonStats)

    #Add Players
    for i in range(len(table)):

        player = []
        sql = []
        x = 0
        f = 0
        for td in table[i].find_all("td"):
            str = "`" + td.text + "`"
            if td.text != '' and td.text != '0.0' and td.text != '0' and td.text != '.000':
                if x < 2:
                    player.append(str)
                else:
                    player.append(td.text)
                sql.append(column_names_clean[x])        
            x+=1
        sql_stmt = ''
        s = ''
        for i in sql:
            sql_stmt +="`" + i + "`" + ", "
            s += "%s, "
        season_str = f"{season}"
        com = "INSERT INTO `" + season_str + "` (" + sql_stmt[:-2] + ") " + "VALUES (" +s[:-2] + ")"
        cursorObject.execute(com, player)
        dataBase.commit()

# disconnecting from server
dataBase.close()