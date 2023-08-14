from flask import Flask, render_template
from flask import request, redirect, url_for
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer,CHAR
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import database_exists

Base = declarative_base()

#========== Team Class ==========
class Team(Base):
  __tablename__ = "teams"

  uid = Column("uid", Integer, primary_key=True)
  name = Column("name", String)
  rank = Column("rank", Integer)
  points = Column("points", Integer)
  games_played = Column("games_played", Integer)
  wins = Column("wins", Integer)
  losses = Column("losses", Integer)

  def __init__(self, uid, name, rank, points, games_played, wins, losses):
    self.uid = uid
    self.name = name
    self.rank = rank
    self.points = points
    self.games_played = games_played
    self.wins = wins
    self.losses = losses

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

  def __repr__(self):
    return f"({self.rank}), {self.name} ({self.wins} / {self.losses}, {self.points}, {self.points // self.games_played})"

class Player(Base):
  __tablename__ = "players"

  uid = Column("uid", Integer, primary_key=True)
  firstname = Column("firstname", String)
  lastname = Column("lastname", String)
  team = Column(Integer, ForeignKey("teams.uid"))    # ** Check this later

  # These could be ForeignKeys, but if a player is not playing for any reason this will affect their stats even though they never played
  rank = Column("rank", Integer)
  points = Column("points", Integer)
  games_played = Column("games_played", Integer)
  wins = Column("wins", Integer)
  losses = Column("losses", Integer)

  def __init__(self, uid, firstname, lastname, team, rank, points, games_played, wins, losses):
    self.uid = uid
    self.firstname = firstname
    self.lastname = lastname
    self.team = team
    self.rank = rank
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

  def __repr__(self):
    return f"({self.uid}, {self.team}), {self.firstname} {self.lastname} ({self.wins} / {self.losses}, {self.points}, {self.points // self.games_played})"
  
#========== Database ==========
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
  t1 = Team(1, "School Boys", 1, 210, 4, 3, 1)
  t2 = Team(2, "Young Ballerz", 2, 180, 4, 2, 2)
  t3 = Team(3, "Fire Hunters", 3, 175, 4, 2, 2)
  t4 = Team(4, "Benmore Rams", 5, 50, 4, 0, 4)
  t5 = Team(5, "Alpine Salmon", 4, 105, 4, 1, 3)

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
  

#========== Flask ==========
app = Flask(__name__) 

@app.route('/')    # Route to Homepage
def root():
  return render_template('home.html', page_title="Home")

@app.route('/teams')    # Route to Team Page
def teams():
  Session = sessionmaker(bind=engine)
  session = Session()
  results=session.query(Team).all() 
  print("\n\nTeams are:\n")
  print(results)
  return render_template("teams.html", page_title="TEAMS", query_results = results)

@app.route('/players')    # Route to Players Page
def players():
  Session = sessionmaker(bind=engine)
  session = Session()
  results=session.query(Player).all() 
  print("\n\nPlayers are:\n")
  print(results)
  return render_template("players.html", page_title="PLAYERS", query_results = results)

#This route is where the SSN of the person to be edited is entered. It uses a redirect with the ssn as a parameter
#to create a custom URL the SSN is passed to the update page. This creates a page /update/<SSN>
#that contains the details of the person to edit
@app.route('/edit_player', methods=['POST', 'GET'])  # note the leading slash, it’s important
def edit_player():
  if request.method == "POST":
    uid = request.form.get("uid")
    print("uid requested is - from edit method - " + uid)
    return redirect(url_for('update', ids = uid))
    
  else:
    print("did not redirect")
    return render_template("edit_player.html",page_title='EDIT A PLAYER')

@app.route('/update/<ids>', methods=['POST', 'GET'])
#Update is used to update a database entry or delete a database entry. A custom page is created on the fly
#for a person when the SSN is passed from edit_person().
#First the person details are got as an object from the DB using SQLalchemy - create a person object.
#Next, (last line of this function) the update page is rendered by passing fname, lname etc to update.html
#If values are edited, they are saved by e.g. person.firstname = request.form['fname'] - which gets
#the edited value from the form and sets a person attribute. The session is commited and a redirect to 'people'
#so that you can see the edit
#If delete is pressed, the person object is deleted using session.delete(person)
def update(ids):
  print(ids)
  Base.metadata.create_all(bind=engine)
  Session = sessionmaker(bind=engine)
  session = Session()
  # getting input with ssn = ssn in HTML form
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
      return redirect(url_for('people', page_title="PEOPLE"))   
      
    elif request.form['edit_button'] =="Delete":# Delete so delete the player
      print("Delete clicked  -update")
      session.delete(player)
      session.commit()
      print("deleted person with id " + ids)
      return redirect(url_for('people', page_title="PEOPLE"))
      
  print("sending variables from update")
  #Return statement below is run the first time the page is loaded.
  return render_template("update.html",page_title='UPDATE A PERSON', ids=uid, Fname = fname, Lname = lname, Points = points)

if __name__ == "__main__":    # Starts App
    app.run(debug=True, host="0.0.0.0", port=8080)