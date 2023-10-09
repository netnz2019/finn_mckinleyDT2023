from flask import Flask, render_template
from flask import request, redirect, url_for
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer,CHAR
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import database_exists
# Importing Libraries

Base = declarative_base()

#====================== Team Class ======================
class Team(Base):
  __tablename__ = "teams" # Creates SQL Table

  # Create Table Columns
  uid = Column("uid", Integer, primary_key=True)
  name = Column("name", String)
  rank = Column("rank", Integer)
  points = Column("points", Integer)
  games_played = Column("games_played", Integer)
  wins = Column("wins", Integer)
  losses = Column("losses", Integer)
  gender = Column("gender", CHAR)

  # Creates object based on the tables data (Setter Method)
  def __init__(self, uid, name, rank, points, games_played, wins, losses, gender):
    self.uid = uid
    self.name = name
    self.rank = rank
    self.points = points
    self.games_played = games_played
    self.wins = wins
    self.losses = losses
    self.gender = gender

  # Returns data from object (Getter Methods)
  def get_uid(self):
    return self.uid

  def get_name(self):
    return self.name

  def get_rank(self):
    return self.rank

  def get_points(self):
    return self.points

  def get_games_played(self):
    return self.games_played

  def get_wins(self):
    return self.wins

  def get_losses(self):
    return self.losses

  def get_gender(self):
    return self.gender

  # Returns self data (Getter Method)
  def __repr__(self):
    return f"({self.uid}) #{self.rank} {self.name} ({self.points} / {self.games_played}) - ({self.wins} / {self.games_played - (self.wins + self.losses)} / {self.losses}) {self.gender}"

#====================== Player ======================
class Player(Base):
  __tablename__ = "players" # Creates SQL Table

  # Create Table Columns
  uid = Column("uid", Integer, primary_key=True)
  firstname = Column("firstname", String)
  lastname = Column("lastname", String)
  team = Column(Integer, ForeignKey("teams.uid"))
  number = Column("number", Integer)
  points = Column("points", Integer)
  games_played = Column("games_played", Integer)
  wins = Column("wins", Integer)
  losses = Column("losses", Integer)

  # Creates object based on the tables data (Setter Method)
  def __init__(self, uid, firstname, lastname, team, number, points, games_played, wins, losses):
    self.uid = uid
    self.firstname = firstname
    self.lastname = lastname
    self.team = team
    self.number = number
    self.points = points
    self.games_played = games_played
    self.wins = wins
    self.losses = losses

  # Returns data from object (Getter Methods)
  def get_uid(self):
    return self.uid

  def get_firstname(self):
    return self.firstname
    
  def get_lastname(self):
    return self.lastname

  def get_team(self):
    return self.team

  def get_number(self):
    return self.number

  def get_points(self):
    return self.points

  def get_games_played(self):
    return self.games_played

  def get_wins(self):
    return self.wins

  def get_losses(self):
    return self.losses

  def __repr__(self):
    return f"({self.uid}, {self.team})   #{self.number} - {self.firstname} {self.lastname} ({self.wins} / {self.losses}) ({self.points} / {self.games_played})"
  
#====================== Database ======================
# Creates Database
db_url = "sqlite:///mydb.db"
engine = create_engine(db_url, echo=True)

# Checks if database already exists
if database_exists(db_url):
  print("data base exists - carry on and do stuff")
  Base.metadata.create_all(bind=engine)    # Create a new connection to the database and open a session
  Session = sessionmaker(bind=engine)
  session = Session()
  results = session.query(Team)
  for i in results: # Debugging
    print(i)
else:    # Database does not exist
  print("database does not exist - so create it and add some data")
  Base.metadata.create_all(bind=engine)

  Session = sessionmaker(bind=engine)
  session = Session()
  
  # Adds Teams
  t1 = Team(1, "School Boys", 1, 210, 4, 3, 1, "M")
  t2 = Team(2, "Young Ballerz", 2, 180, 4, 2, 2, "M")
  t3 = Team(3, "Fire Hunters", 3, 175, 4, 2, 2, "M")
  t4 = Team(4, "Benmore Rams", 5, 50, 4, 0, 4, "M")
  t5 = Team(5, "Alpine Salmon", 4, 105, 4, 1, 3, "M")

  session.add(t1)
  session.add(t2)
  session.add(t3)
  session.add(t4)
  session.add(t5)
  session.commit() # Commits Changes

  # Adds Players
  p1 = Player(1, "Ralph", "Henderson", 1, 2, 50, 4, 3, 1)
  p2 = Player(2, "Rudolf", "Campomanes", 2, 1, 103, 4, 2, 2)
  p3 = Player(203, "Dave", "White", 1, 3, 60, 4, 3, 1)
  
  session.add(p1)
  session.add(p2)
  session.add(p3)
  session.commit() # Commits Changes
  
  print("SUCCESS database created and data added")
  
#====================== Testing ======================
def testexists(uid, player=0, team=0):
  print("Testing if exists") # Debug
  if player == 1 and team == 0: # Checks for players
    print("Checking Player") # Debug
    try:
      player = session.query(Player).filter(Player.uid == uid).first() # Searchs db for player
      print("Player Exists: ", player.firstname, player.lastname) # Debug
      return True 
    except:
      print("Player does not exist") # Debug
      return "Error: Player does not exist"
      
  elif  player == 0 and team == 1: # Checks for teams
    print("Checking Team")
    try:
      team = session.query(Team).filter(Team.uid == uid).first() # Searchs db for team
      print("Team Exists: ", team.name, team.uid) # Debug
      return True
    except:
      print("Team does not exist") # Debug
      return "Error: Team does not exist"
  else: # if unexpected input code will return error
    return "Error: Unexpected input in program" # Catches if I did something wrong

def testcreation(uid, player=0, team=0, teamuid=0, games_played=0, wins=0, losses=0):
  print("Testing Creation")
  if player == 1 and team == 0:
    try: # Checks for players
      player = session.query(Player).filter(Player.uid == uid).first()
      print("Player already exists", player.firstname) # Debug
      return "Error: Player already exists"
    except:
      print("Player doesn't exist") # Debug
      
      try: # Checks if player's team exists
        team = session.query(Team).filter(Team.uid == teamuid).first()
        print("Player's team exists", team.name) # Debug

        if games_played < losses + wins: # Checks if match stats makes sense
          print("Unexpected wins / lossess / games played")
          return "Error: Unexpected wins - lossess - games played"
        else: 
          print("All tests completed") # Debug
          return True
          
      except: # Team doesnt exist
        print("Player's team doesn't exist") # Debug
        return "Error: Player's team doesn't exist"
      
  elif player == 0 and team == 1:
    try: # Checks for teams
      team = session.query(Team).filter(Team.uid == uid).first()
      print("Team already exists", team.name) # Debug
      return "Error: Team already exists"
    except:
      print("Team doesn't exist") # Debug

      if games_played < losses + wins:
        print("Unexpected wins / lossess / games played")
        return "Error: Unexpected wins / lossess / games played"
      else: 
        print("All tests completed") # Debug
        return True
      
  else: # Returns error in input (likely not users fault)
    return "Error: unexpected input"

def testTeamUpdate(new_uid, uid, gender, games_played, losses, wins):
  """ Tests if the updates are valid """
  if gender.upper() != "F" and gender.upper() != "M":
    return "Error: Gender must be F/M"
  else:
    if int(new_uid) != int(uid):
      try:
        team = session.query(Team).filter(Team.uid == new_uid).first()
        if team != None:
          print("Team UID Unchanged:", team) # Debug
          return "Error: Team UID is already in use"
      except:
        print("") # Debug
    if games_played < losses + wins: # Checks if match stats makes sense
      print("Unexpected wins / lossess / games played")
      return "Error: Unexpected wins / lossess / games played"
    else: 
      print("No Errors found in testTeamUpdate") # Debug
      return True

def testPlayerUpdate(new_uid, uid, team, games_played, losses, wins):
  """ Tests player update changes """
  if int(new_uid) != int(uid):
    print(new_uid, uid)
    try:
      player = session.query(Player).filter(Player.uid == new_uid).first()
      if player != None:
        print("Player UID Unavailable:", player) # Debug
        return "Error: Player UID is already in use"
    except:
      print("") # Debug
  if games_played < losses + wins: # Checks if match stats makes sense
    print("Unexpected wins / lossess / games played")
    return "Error: Unexpected wins / lossess / games played"
  try:
    testingteam = session.query(Team).filter(Team.uid == int(team)).first()
    print("Players team exists", testingteam)
    print("No Errors found in testTeamUpdate") # Debug
    return True
  except:
    return "Error: Player's team does not exist"

def teststupidinput(input):
  """ Tests for ridiculous inputs """
  if not input:
    return "Error: Value is empty"
  try:
    x = input + 1
    if input < 0:
      return "Error: Value cannot be negative"
    if input > 2000:
      return "Error: Value is too large"
      print(x)
  except TypeError:
    print("No Errors found") # Debug
    return True
  else:
    print("No Errors found") # Debug
    return True
    
#====================== Flask ======================
app = Flask(__name__) # Loads Flask app

@app.route('/')    # Route to Homepage
def root():
  # Connects to database
  Session = sessionmaker(bind=engine)
  session = Session()

  # Gets teams
  maleteams = session.query(Team).filter(Team.gender == "M")
  femaleteams = session.query(Team).filter(Team.gender == "F")

  # Gets players
  maleplayers = session.query(Player).all()
  # Need to add female player filtering

  return render_template('home.html', page_title="Home", maleteams = maleteams, femaleteams = femaleteams,  maleplayers = maleplayers)

#====================== Teams ======================
@app.route('/teams')    # Route to Team Page
def teams():
  # Connects to database
  Session = sessionmaker(bind=engine)
  session = Session()
  results=session.query(Team).all() 

  # Debug
  print("\n\nTeams are:\n")
  print(results)
  return render_template("teams.html", page_title="TEAMS", query_results = results) # Returns team data

#====================== Players ======================
@app.route('/players')    # Route to Players Page
def players():
  # Connects to database
  Session = sessionmaker(bind=engine)
  session = Session()
  results=session.query(Player).all()

  # Debug
  print("\n\nPlayers are:\n")
  print(results)
  return render_template("players.html", page_title="PLAYERS", query_results = results) # Returns player data

#====================== Add Player ======================
@app.route('/add_player', methods=['POST', 'GET'])    # Route to Add Player Page
def add_player():
  if request.method == "POST":
    # Gets form inputs
    uid = request.form.get("uid")
    first_name = request.form.get("fname")
    last_name = request.form.get("lname")
    team = request.form.get("team")
    number = request.form.get("number")
    points = request.form.get("points")
    games_played = request.form.get("games")
    wins = request.form.get("wins")
    losses = request.form.get("losses")

    print("\nUID type is:", type(uid)) # Debug
    print("UID Value is:", uid)
    
    # Create a new connection and session
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Converts data to int from txt
    try:
      uid = int(uid)
      points = int(points)
      games_played = int(games_played)
      wins = int(wins)
      losses = int(losses)
    except:
      print("Error: Cannot convert value to integer")
      return redirect(url_for("error_page", error = "Error: Expected number input"))

    # Tests for ridiculous inputs first
    testplayer = [uid, first_name, last_name, team, number, points, games_played, wins, losses]
        
    for i in testplayer:
      if teststupidinput(i) != True:
        return redirect(url_for("error_page", error = teststupidinput(i)))
    print("No errors found in teststupidinput") # Debug

    # Tests for more complex issues
    if testcreation(uid, 1, 0, team, games_played, wins, losses) == True:
      # Create a player object
      p = Player(uid, first_name, last_name, team, number, points, games_played, wins, losses)
      # Adds to the database
      session.add(p)
      print("Player added" + str(uid)) # Debug
      session.commit() 
    else: # Error occured
      result = testcreation(uid, 1, 0, team, games_played, wins, losses)
      print(result)
      return redirect(url_for("error_page", error = result))
  return render_template("add_player.html")

#====================== Add Team ======================
@app.route('/add_team', methods=['POST', 'GET'])    # Route to Add Team Page
def add_team():
  if request.method == "POST":
    # Gets form inputs
    uid = request.form.get("uid")
    name = request.form.get("name")
    rank = request.form.get("rank")
    points = request.form.get("points")
    games_played = request.form.get("games_played")
    wins = request.form.get("wins")
    losses = request.form.get("losses")
    gender = request.form.get("gender")
    
    # Create a new connection and session
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Converts data to int from txt
    try:
      uid = int(uid)
      rank = int(rank)
      points = int(points)
      games_played = int(games_played)
      wins = int(wins)
      losses = int(losses)
      gender = (gender)
    except:
      print("Error: Cannot convert value to integer")
      return redirect(url_for("error_page", error = "Error: Expected number input"))

    testteam = [uid, name, rank, points, games_played, wins, losses, gender]
    for i in testteam:
      if teststupidinput(i) != True:
        return redirect(url_for("error_page", error = teststupidinput(i)))
    print("No errors found in teststupidinput") # Debug
    
    # Create a team object
    if testcreation(uid, 0, 1, uid, games_played, wins, losses): # Tests inputs
      t = Team(uid, name, rank, points, games_played, wins, losses, gender)
      # Add to the database
      session.add(t)
      print("Team added" + str(uid)) # Debug
      session.commit()
  return render_template("add_team.html")
  
#====================== Edit Player ======================
@app.route('/edit_player', methods=['POST', 'GET'])    # Route to edit page
def edit_player():
  # Get Players
  Session = sessionmaker(bind=engine)
  session = Session()
  playerlist = session.query(Player).all() 

  print("\n\nPlayers are:\n") # Debug
  for i in playerlist:
    print(i.uid, i.firstname, i.lastname)

  # Get Teams
  teamlist=session.query(Team).all() 

  print("\n\nTeams are:\n") # Debug
  for i in teamlist:
    print(i.uid, i.name)

  # Checks form for inputs
  if request.method == "POST":
    if request.form['edit_button'] =="search":
      uid = request.form.get("player") # Gets player from dropdown menu
      print("uid requested is - from edit method - " + str(uid)) # Debug

      # Error testing
      if testexists(uid, 1, 0) == True:
        return redirect(url_for('update_player', ids = uid)) # Updates player with selected UID
      else:
        return redirect(url_for('error_page', error = testexists(uid, 1, 0)))
      
    elif request.form['edit_button'] =="add":
      return redirect(url_for('add_player'))
  else:
    print("Did not redirect") # Debug
    return render_template("edit.html", page_title='EDIT', playerlist = playerlist, query_results = teamlist) # Renders edit page with dropdown menu's

#====================== Edit Team ======================
@app.route('/edit_team', methods=['POST', 'GET'])    # Route to edit page
def edit_team():
  # Connects to database
  Session = sessionmaker(bind=engine)
  session = Session()
  teamlist=session.query(Team).all() 

  # Debug
  print("\n\nTeams are:\n")
  for i in teamlist:
    print(i.uid, i.name)

  if request.method == "POST":
    if request.form['edit_button'] == "search":
      uid = request.form.get("team") # Gets team from dropdown menu
      print("\n ID is:", uid, "\n") # Debug

      # Error Testing
      if testexists(uid, 0, 1) == True:      
        return redirect(url_for('update_team', ids = uid)) # Updates selected team
      else:
        return redirect(url_for('error_page', error = testexists(uid, 0, 1))) # Goes to error page
        
    elif request.form['edit_button'] =="add":
      return redirect(url_for('add_team')) # Redirects to add team page
  else:
    return render_template("edit.html", page_title="EDIT TEAMS", query_results = teamlist) # Render edit page with dropdown menu's

#====================== Update Player ======================
@app.route('/update_player/<ids>', methods=['POST', 'GET'])    # Route to Upade Player
def update_player(ids):
  print("Selected Player to update is:", ids) # Debug

  # Connects to database
  Base.metadata.create_all(bind=engine)
  Session = sessionmaker(bind=engine)
  session = Session()

  # Collects selected UID
  uid = int(ids)
  print("uid requested is ... " + str(uid)) # Debug

  # Gets player from database from UID
  player = session.query(Player).filter(Player.uid == uid).first()

  # Gets properties of player
  fname = player.get_firstname()
  print(fname) # Debug
  lname = player.get_lastname()
  team = player.get_team()
  number = player.get_number() 
  points = player.get_points()
  games_played = player.get_games_played()
  losses = player.get_losses()
  wins = player.get_wins()
  
  if request.method == 'POST': # Check which button is clicked
    if request.form['edit_button'] =="Save": # Save pressed, so update the details. request.form['edit_button'] checks the value of the button.
      print("Save clicked - update") # Debug
      
      # Get data from the form
      new_uid = int(request.form['uid'])
      new_firstname = request.form['fname']
      new_lastname = request.form['lname']
      new_team = int(request.form['team'])
      new_number = int(request.form['number'])
      new_points = int(request.form['points'])
      new_games_played = int(request.form['games_played'])
      new_losses = int(request.form['losses'])
      new_wins = int(request.form['wins'])

      # Test the data
      testPlayer = [new_firstname, new_lastname, new_team, new_number, new_points, new_games_played, new_losses, new_wins]
      for i in testPlayer:
        if teststupidinput(i) != True:
          return redirect(url_for("error_page", error = teststupidinput(i)))
      print("No errors found in teststupidinput") # Debug

      if testPlayerUpdate(new_uid, uid, new_team, new_games_played, new_losses, new_wins) == True:
        # Update the player details
        player.uid = new_uid
        player.firstname = new_firstname
        player.lastname = new_lastname
        player.team = new_team
        player.number = new_number
        player.points = new_points
        player.games_played = new_games_played
        player.losses = new_losses
        player.wins = new_wins
        session.commit() # Save changes
        return redirect(url_for('players', page_title="PLAYERS")) # Redirects to players page so user can see changes
      else:
        return redirect(url_for("error_page", error = testPlayerUpdate(new_uid, uid, new_team, new_games_played, new_losses, new_wins))) 
      
    elif request.form['edit_button'] =="Delete": # Delete the player
      print("Delete clicked  -update") # Debug

      # Deletes player from database
      session.delete(player)
      session.commit() # Saves changes
      print("deleted person with id " + ids) # Debug
      return redirect(url_for('players', page_title="PLAYERS")) # Redirects to players page so user can see changes
      
  print("sending variables from update") # Debug
  
  return render_template("update_player.html",page_title='UPDATE A PERSON', ids=uid, Fname = fname, Lname = lname, Team = team, Number = number, Points = points, Games_played = games_played, Losses = losses, Wins = wins) # Sets up form on initial loading
  
#====================== Update Team ======================
@app.route('/update_team/<ids>', methods=['POST', 'GET'])    # Route to update Team
def update_team(ids):
  print(ids) # Debug

  # Connects to database
  Base.metadata.create_all(bind=engine)
  Session = sessionmaker(bind=engine)
  session = Session()
  
  uid = int(ids) # Collects selected UID
  team = session.query(Team).filter(Team.uid == uid).first() # Finds team connected to UID
  
  # Gets properties of selected team
  name = team.name 
  print("name requested is ... " + name) # Debug
  rank = team.rank
  points = team.points
  games_played = team.games_played
  wins = team.wins
  losses = team.losses
  gender = team.gender
  

  if request.method == 'POST': # Check which button is clicked
    if request.form['edit_button'] == "Save": # Update the details
      print("Save clicked - update") # Debug

      # Finds changes
      new_uid = request.form['uid']
      print("UID is" + str(new_uid))
      new_name = request.form['name']
      print("Name is" + new_name)
      new_rank = int(request.form['rank'])
      print("Rank is" + str(new_rank))
      new_points = int(request.form['points'])
      print("Points is " + str(new_points))      
      new_games_played = int(request.form['games_played'])
      print("Games played is" + str(new_games_played))
      new_wins = int(request.form['wins'])
      print("Wins is" + str(new_wins))
      new_losses = int(request.form['losses'])
      print("Losses is" + str(new_losses))
      new_gender = request.form['gender']
      print("Gender is" + new_gender)

      # Tests changes
      testteam = [new_uid, new_name, new_rank, new_points, new_games_played, new_wins, new_losses, new_gender]
      for i in testteam:
        if teststupidinput(i) != True:
          return redirect(url_for("error_page", error = teststupidinput(i)))
      print("No errors found in teststupidinput") # Debug

      if testTeamUpdate(new_uid, uid, new_gender, new_games_played, new_losses, new_wins) == True:
        # Makes changes
        team.uid = new_uid
        team.name = new_name
        team.rank = new_rank
        team.points = new_points
        team.games_played = new_games_played
        team.wins = new_wins
        team.losses = new_losses
        team.gender = new_gender[0].upper()
        session.commit() # Saves changes
        return redirect(url_for('teams', page_title="TEAMS ")) # Redirects to teams page so user can see changes
      else:
        return redirect(url_for("error_page", error = testTeamUpdate(new_uid, uid, new_gender, new_games_played, new_losses, new_wins)))
      
    elif request.form['edit_button'] =="Delete":# Delete the player
      print("Delete clicked  -update") # Debug
      # Delete team
      session.delete(team) 
      session.commit()
      print("deleted team with name " + name) # Debug
      return redirect(url_for('teams', page_title="TEAMS")) # Redirects to teams page so user can see changes
      
  print("sending variables from update") # Debug
  
  return render_template("update_team.html",page_title='UPDATE A TEAM', ids=uid, name = name, rank = rank, points = points, games_played = games_played, wins = wins, losses = losses, gender = gender) # Renders on initial loading

#====================== Error Page ======================
@app.route('/error_page/<error>', methods=['POST', 'GET'])
def error_page(error="IDK what just happened"):
  error = [error]
  print("Error is:", error)
  return render_template("error.html", page_title="Error", errors = error)

if __name__ == "__main__":    # Starts App
    app.run(debug=True, host="0.0.0.0", port=5000)

