from flask import Flask, render_template
from flask import request, redirect, url_for
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer,CHAR
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import database_exists

Base = declarative_base()

#====================== Team ======================
class Team(Base):
  __tablename__ = "teams"

  uid = Column("uid", Integer, primary_key=True)
  name = Column("name", String)
  rank = Column("rank", Integer)
  points = Column("points", Integer)
  games_played = Column("games_played", Integer)
  wins = Column("wins", Integer)
  losses = Column("losses", Integer)
  gender = Column("gender", CHAR)

  def __init__(self, uid, name, rank, points, games_played, wins, losses, gender):
    self.uid = uid
    self.name = name
    self.rank = rank
    self.points = points
    self.games_played = games_played
    self.wins = wins
    self.losses = losses
    self.gender = gender

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
  
  def __repr__(self):
    return f"({self.uid}) #{self.rank} {self.name} ({self.points} / {self.games_played}) - ({self.wins} / {self.games_played - (self.wins + self.losses)} / {self.losses}) {self.gender}"

#====================== Player ======================
class Player(Base):
  __tablename__ = "players"

  uid = Column("uid", Integer, primary_key=True)
  firstname = Column("firstname", String)
  lastname = Column("lastname", String)
  team = Column(Integer, ForeignKey("teams.uid"))    # ** Check this later

  # These could be ForeignKeys, but if a player is not playing for any reason this will affect their stats even though they never played
  number = Column("number", Integer)
  points = Column("points", Integer)
  games_played = Column("games_played", Integer)
  wins = Column("wins", Integer)
  losses = Column("losses", Integer)

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
db_url = "sqlite:///mydb.db"
engine = create_engine(db_url, echo=True)

# Create the database or use existing one
if database_exists(db_url):
  print("data base exists - carry on and do stuff")
  Base.metadata.create_all(bind=engine)    # Create a new connection to the database and open a session
  Session = sessionmaker(bind=engine)
  session = Session()
  results = session.query(Team)
  for i in results:
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
  

#====================== Flask ======================
app = Flask(__name__) 

@app.route('/')    # Route to Homepage
def root():
  return render_template('home.html', page_title="Home")

#====================== Teams ======================
@app.route('/teams')    # Route to Team Page
def teams():
  Session = sessionmaker(bind=engine)
  session = Session()
  results=session.query(Team).all() 
  print("\n\nTeams are:\n")
  print(results)
  return render_template("teams.html", page_title="TEAMS", query_results = results)

#====================== Players ======================
@app.route('/players')    # Route to Players Page
def players():
  Session = sessionmaker(bind=engine)
  session = Session()
  results=session.query(Player).all() 
  print("\n\nPlayers are:\n")
  print(results)
  return render_template("players.html", page_title="PLAYERS", query_results = results)

#====================== Add Player ======================
@app.route('/add_player', methods=['POST', 'GET'])    # Route to Add Player Page
def add_player():
  if request.method == "POST":
    # Getting input with name = fname in HTML form
    uid = request.form.get("uid")
    first_name = request.form.get("fname")
    last_name = request.form.get("lname")
    team = request.form.get("team")
    number = request.form.get("number")
    points = request.form.get("points")
    games_played = request.form.get("games")
    wins = request.form.get("wins")
    losses = request.form.get("losses")
       
    # Create a new connection and session
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    # Converts data to int from txt
    uid = int(uid)
    points = int(points)
    games_played = int(games_played)
    wins = int(wins)
    losses = int(losses)
    
    #Create a person object
    p = Player(uid, first_name, last_name, team, number, points, games_played, wins, losses)
    #Add to the database
    session.add(p)
    print("Player added" + str(uid))
    session.commit() 
  return render_template("add_player.html")

#====================== Add Team ======================
@app.route('/add_team', methods=['POST', 'GET'])    # Route to Add Player Page
def add_team():
  if request.method == "POST":
    # Getting input with name = fname in HTML form
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
    uid = int(uid)
    rank = int(rank)
    points = int(points)
    games_played = int(games_played)
    wins = int(wins)
    losses = int(losses)
    gender = (gender)
    
    #Create a team object
    t = Team(uid, name, rank, points, games_played, wins, losses, gender)
    #Add to the database
    session.add(t)
    print("Team added" + str(uid))
    session.commit() 
  return render_template("add_team.html")

#====================== Edit Player ======================
@app.route('/edit_player', methods=['POST', 'GET'])    # Route to edit page
def edit_player():
  if request.method == "POST":
    if request.form['edit_button'] =="search":
      uid = request.form.get("uid")
      print("uid requested is - from edit method - " + uid)
      return redirect(url_for('update_player', ids = uid))
    elif request.form['edit_button'] =="add":
      return redirect(url_for('add_player'))
  else:
    print("did not redirect")
    return render_template("edit.html",page_title='EDIT A PLAYER')

#====================== Edit Team ======================
@app.route('/edit_team', methods=['POST', 'GET'])    # Route to edit page
def edit_team():
  Session = sessionmaker(bind=engine)
  session = Session()
  results=session.query(Team).all() 

  # Debug
  print("\n\nTeams are:\n")
  for i in results:
    print(i.uid, i.name)

  if request.method == "POST":
    print("Post")
    if request.form['edit_button'] == "search":
      uid = request.form.get("team")
      print("\n ID is:", uid, "\n") # Debug
      return redirect(url_for('update_team', ids = uid))
    elif request.form['edit_button'] =="add":
      return redirect(url_for('add_team'))
  
  return render_template("edit.html", page_title="EDIT TEAMS", query_results = results)

#====================== Update Player ======================
@app.route('/update_player/<ids>', methods=['POST', 'GET'])    # Route to Upade Player
def update_player(ids):
  print(ids)
  Base.metadata.create_all(bind=engine)
  Session = sessionmaker(bind=engine)
  session = Session()
  uid = ids
  print("uid requested is ... " + uid)
  uid = int(uid)
  
  player = session.query(Player).filter(Player.uid == uid).first()
  fname = player.get_firstname()
  print(fname) #Check getter method works
  lname = player.get_lastname()
  points = player.get_points()

  if request.method == 'POST': #Check which button is clicked
    
    if request.form['edit_button'] =="Save": #Save pressed, so update the details. request.form['edit_button'] checks the value of the button.
      print("Save clicked - update")
      player.firstname = request.form['fname']# Get the fanme from the form and set it. In SQLalchemy we can directly edit an objects attributes!
      print( "Got the first name")
      player.lastname = request.form['lname']
      print( "Last Name is " + lname)      
      #person.ssn = request.form['int'] ssn is a primary key - do not change
      player.points = int(request.form['points'])
      session.commit()
      return redirect(url_for('players', page_title="PLAYERS"))   
      
    elif request.form['edit_button'] =="Delete":# Delete so delete the player
      print("Delete clicked  -update")
      session.delete(player)
      session.commit()
      print("deleted person with id " + ids)
      return redirect(url_for('players', page_title="PLAYERS"))
      
  print("sending variables from update")
  #Return statement below is run the first time the page is loaded.
  return render_template("update_player.html",page_title='UPDATE A PERSON', ids=uid, Fname = fname, Lname = lname, Points = points)

#====================== Update Team ======================
@app.route('/update_team/<ids>', methods=['POST', 'GET'])    # Route to update Team
def update_team(ids):
  print(ids)
  Base.metadata.create_all(bind=engine)
  Session = sessionmaker(bind=engine)
  session = Session()
  uid = ids
  
  team = session.query(Team).filter(Team.uid == uid).first()
  name = team.name
  print("name requested is ... " + name)
  
  rank = team.rank
  points = team.points
  print(points) # Check method works
  games_played = team.games_played
  wins = team.wins
  losses = team.losses
  gender = team.gender
  

  if request.method == 'POST': #Check which button is clicked
    if request.form['edit_button'] == "Save": #Save pressed, so update the details. request.form['edit_button'] checks the value of the button.
      print("Save clicked - update")
      team.uid = request.form['uid']
      print("UID is" + uid)
      team.name = request.form['name']
      print("Name is" + name)
      team.rank = int(request.form['rank'])
      print("Rank is" + str(rank))
      team.points = int(request.form['points'])
      print("Points is " + str(points))      
      team.games_played = int(request.form['games_played'])
      print("Games played is" + str(games_played))
      team.wins = int(request.form['wins'])
      print("Wins is" + str(wins))
      team.losses = int(request.form['losses'])
      print("Losses is" + str(losses))
      team.gender = request.form['gender']
      print("Gender is" + gender)
      session.commit()
      return redirect(url_for('teams', page_title="TEAMS "))   
      
    elif request.form['edit_button'] =="Delete":# Delete so delete the player
      print("Delete clicked  -update")
      session.delete(team)
      session.commit()
      print("deleted team with name " + name)
      return redirect(url_for('teams', page_title="TEAMS"))
      
  print("sending variables from update")
  #Return statement below is run the first time the page is loaded.
  return render_template("update_team.html",page_title='UPDATE A TEAM', ids=uid, name = name, rank = rank, points = points, games_played = games_played, wins = wins, losses = losses, gender = gender)

if __name__ == "__main__":    # Starts App
    app.run(debug=True, host="0.0.0.0", port=8080)