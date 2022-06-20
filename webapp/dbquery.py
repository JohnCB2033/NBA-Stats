#Importing requirements, connecting to database, and creating cursor object
import mysql.connector
  
#Connecting to database
dataBase = mysql.connector.connect(
host ="mysql",
user ="mj",
passwd ="23",
  database = "nba"
)
 
# preparing a cursor object
cursorObject = dataBase.cursor()

stat_columns_list = ['Player', 'Position', 'Age', 'Team', 'Games Played', 'Games Started', 'Minutes Played Per Game', 'Field Goals Per Game', 'Field Goal Attempts Per Game', 
'Field Goal Percentage', '3-Point Field Goals Per Game', '3-Point Field Goal Attempts Per Game', '3-Point Field Goal Percentage' , '2-Point Field Goals Per Game', 
'2-Point Field Goal Attempts Per Game', '2-Point Field Goal Percentage', 'Effective Field Goal Percentage', 'Free Throws Per Game', 'Free Throw Attempts Per Game', 
'Free Throw Percentage', 'Offensive Rebounds Per Game', 'Defensive Rebounds Per Game', 'Rebounds Per Game', 'Assists Per Game', 'Steals Per Game', 'Blocks Per Game',
'Turnovers Per Game', 'Personal Fouls Per Game', 'Points Per Game']

stat_columns_dict = {'Player':'Player', 'Pos':'Position', 'Age':'Age', 'Tm':'Team', 'G':'Games Played', 'GS':'Games Started', 'MP':'Minutes Played Per Game',
 'FG':'Field Goals Per Game', 'FGA':'Field Goal Attempts Per Game', 'FG%':'Field Goal Percentage', '3P':'3-Point Field Goals Per Game',
  '3PA':'3-Point Field Goal Attempts Per Game', '3P%':'3-Point Field Goal Percentage', '2P':'2-Point Field Goals Per Game', '2PA':'2-Point Field Goal Attempts Per Game', 
  '2P%':'2-Point Field Goal Percentage', 'eFG%':'Effective Field Goal Percentage', 'FT':'Free Throws Per Game', 'FTA':'Free Throw Attempts Per Game', 
  'FT%':'Free Throw Percentage', 'ORB':'Offensive Rebounds Per Game', 'DRB':'Defensive Rebounds Per Game', 'TRB':'Rebounds Per Game', 'AST':'Assists Per Game',
   'STL':'Steals Per Game', 'BLK':'Blocks Per Game', 'TOV':'Turnovers Per Game', 'PF':'Personal Fouls Per Game', 'PTS':'Points Per Game'}


team_names = {'TOT':'Traded In Season', 'LAL':'Los Angeles Lakers', 'PHO':'Phoenix Suns', 'WSB':'Washington Bullets', 'DAL':'Dallas Mavericks', 'BOS':'Boston Celtics',
'DEN':'Denver Nuggets', 'HOU':'Houston Rockets', 'IND':'Indiana Pacers', 'CLE':'Cleveland Cavaliers', 'NJN':'New Jersey Nets', 'UTA':'Utah Jazz', 'GSW':'Golden State Warriors',
'CHI':'Chicago Bulls', 'PHI':'Philadelphia 76ers', 'ATL':'Atlanta Hawks', 'LAC':'Los Angeles Clippers', 'POR':'Portland Trail Blazers', 'SAS':'San Antonio Spurs',
'MIL':'Milwaukee Bucks', 'DET':'Detroit Pistons', 'NYK':'New York Knicks', 'SAC':'Sacramento Kings', 'SEA':'Seatle Supersonics', 'AND':'Anderson Packers',
'BLB':'Baltimore Bullets', 'CHS':'Chicago Stags', 'DNN':'Denver Nuggets', 'FTW':'Fortwayne Pistons', 'INO':'Indianapolis Olympians', 'MNL':'Minneapolis Lakers',
'PHW':'Philadelphia Warriors', 'ROC':'Rochester Royals', 'SHE':'Sheboygan', 'STB':'St. Louis Bombers', 'SYR':'Syracuse Nationals', 'TRI':'Tri-Cities Blackhawks',
'WAT':'Waterloo Hawks', 'WSC':'Washington Capitols', 'MLH':'Milwaukee Hawks', 'STL':'St. Louis Hawks', 'CIN':'Cincinnati Royals', 'CHP':'Chicago Packers', 'SFW':'San Francisco Warriors'
, 'CHZ':'Chicago Zephyrs', 'BAL':'Baltimore Bullets', 'SDR':'San Diego Rockets', 'BUF':'Buffalo Braves', 'KCO':'Kansas City-Omaha Kings', 'CAP':'Capital Bullets', 'NOJ':'New Orleans Jazz'
, 'KCK':'Kansas City Kings', 'NYN':'New York Nets', 'SDC':'San Diego Clippers', 'CHH':'Charlotte Hornets', 'MIA':'Miami Heat', 'ORL':'Orlando Magic', 'MIN':'Minnesota Timberwolves',
'VAN':'Vancouver Grizzlies', 'TOR':'Toronto Raptors', 'WAS':'Washington Wizards', 'MEM':'Memphis Grizzlies', 'NOH':'New Orleans Hornets', 'CHA':'Charlotte Bobcats',
'NOK':'New Orleans/Oklahoma City Hornets', 'OKC':'Oklahoma City Thunder', 'BRK':'Brooklyn Nets', 'NOP':'New Orleans Pelicans', 'CHO':'Charlotte Hornets'}




def __init__(self, season, want):
    self.season = season
    self.want = want

def run_query(want, season, where, order):
    #Running the query
    query = f"SELECT {want} FROM `{season}`"
    if where != '':
        query += f" WHERE {where}"
    if order != '':
        query += f" ORDER BY {order}"
    cursorObject.execute(query)
    return list(cursorObject.fetchall())

def clean_data (myresult, want):
    myresult = list(myresult)
    if want != '*':
        want = want.split(", ")
    for player in range(0, len(myresult)):
        myresult[player] = list(myresult[player])
        for stat in range(0, len(myresult[player])):
            if want != '*':
                if want[stat] == 'Tm':
                    myresult[player][stat] = team_names[myresult[player][stat]]
            elif len(myresult[player][3]) <= 3:
                myresult[player][3] = team_names[myresult[player][3]]
            myresult[player][stat] = str(myresult[player][stat])
            while myresult[player][stat][(len(myresult[player][stat])-1):] == '0':
                myresult[player][stat] = myresult[player][stat][:-1]
            while myresult[player][stat][(len(myresult[player][stat])-1):] == '`':
                myresult[player][stat] = myresult[player][stat][:-1]
            while myresult[player][stat][0] == '`':
                myresult[player][stat] = myresult[player][stat][1:]
            while myresult[player][stat][(len(myresult[player][stat])-1):] == '.':
                myresult[player][stat] = myresult[player][stat][:-1]
            
            
    return myresult

def column_lengths(myresult, want):
    #setting longest val to the longest value in each column
    longest_vals = []
    #starting with the length of the first player
    for stat in myresult[0]:
        longest_vals.append(len(stat))
    #looping for longest values at each position
    for player in myresult:
        for stat in range(0, len(player)):
            if len(player[stat]) > longest_vals[stat]:
                longest_vals[stat] = len(player[stat])
    #checking against column name lengths
    if want != '*':
        top_row = []
        stat_columns_dict_key = want.split(', ')
        i = 0
        for stat in stat_columns_dict_key:
            if len(stat_columns_dict[stat]) > longest_vals[i]:
                longest_vals[i] = len(stat_columns_dict[stat])
            top_row.append(stat_columns_dict[stat])
            i+=1
        return longest_vals, top_row
    else:
        for stat in range(0, len(stat_columns_list)):
            if len(stat_columns_list[stat]) > longest_vals[stat]:
                longest_vals[stat] = len(stat_columns_list[stat])
        return longest_vals, stat_columns_list

        

def display_info(longest_vals, top_row, players):
    #creating and displaying top row and seperator lines
    top_row_display = ''
    seperator = ''
    for stat in range(0, len(top_row)):
        top_row_display += ' | ' + top_row[stat] + " "*(longest_vals[stat] - len(top_row[stat]))
        seperator += '+' + "-"*(longest_vals[stat]+2)
    top_row_display += " |"
    seperator += "+"
    top_row_display = top_row_display[1:]
    #displaying player info
    t = 0
    result = [seperator]
    for player in players:
        if t%20 == 0:
            result.append(top_row_display)
            result.append(seperator)
        player_display = ''
        i = 0
        for stat in player:
            player_display += ' | ' + stat + " "*(longest_vals[i] - len(stat))
            i +=1
        player_display += " |"
        player_display = player_display[1:]
        result.append(player_display)
        result.append(seperator)
        t+=1
    return result

def master(want, season, where, order):
    a = run_query(want, season, where, order)
    b = clean_data(a, want)
    c = column_lengths(b, want)
    return display_info(c[0], c[1], b)




# startera = input("What stat would you like to look up?\na. Players who average a double double\nb. Players who averaged over 30 points\nc. Players who averaged over 10 assists\nd. Players who averaged over 10 rebounds\n:")
# season_selector = input("What season would you like to see stats for? (1951-2022):")
# if startera == 'a':
#     master(want = 'Player, Pos, Tm, PTS, AST, TRB', season = season_selector, where = 'PTS >= 10 AND TRB >= 10 OR AST >= 10', order = 'PTS')
# if startera == 'b':
#     master(want = 'Player, Pos, Tm, TRB, AST, PTS', season = season_selector, where = 'PTS >= 30', order = 'PTS')
# if startera == 'c':
#     master(want = 'Player, Pos, Tm, TRB, AST, PTS', season = season_selector, where = 'AST >= 10', order = 'AST')
# if startera == 'd':
#     master(want = 'Player, Pos, Tm, TRB, AST, PTS', season = season_selector, where = 'TRB >= 10', order = 'TRB')


# disconnecting from server
