import sqlalchemy as db
import databasetables
import databaseObjects as objs
from sqlalchemy import create_engine, Column, String, Table, Integer, Float, DateTime
from sqlalchemy.orm import Session, sessionmaker, declarative_base
import urllib.parse
import sys, random, os, uuid
import datetime
import queries
import getInputFunctions
from tabulate import tabulate

hashseed = os.getenv('PYTHONHASHSEED')
if not hashseed:
    os.environ['PYTHONHASHSEED'] = '0'
    os.execv(sys.executable, [sys.executable] + sys.argv)

# GLOBALS
escapedPassword = urllib.parse.quote_plus("password")
sqldialect = "mysql+pymysql"
databaseUsername = "admin"
database = "tenniscentral"
host = "tenniscentral.ckusmki3y8up.us-west-1.rds.amazonaws.com"

connectionString = f"{sqldialect}://{databaseUsername}:{escapedPassword}@{host}/{database}"
engine = db.create_engine(connectionString)
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
metadata = db.MetaData()
Base = declarative_base()

def create_account():
    print("Welcome to the account creation page")
    try:
        id = uuid.uuid4()
        email = getInputFunctions.getEmail()
        username = getInputFunctions.getUsername()
        password = hash(getInputFunctions.getPassword())
        firstname = getInputFunctions.getName("first")
        lastname = getInputFunctions.getName("last")
        age = getInputFunctions.getAge()
        gender = getInputFunctions.getGender()
        skillLevel = getInputFunctions.getSkillLevel()

        account = databasetables.Account(accountId=id, email=email, password=password, username=username)
        player = databasetables.Player(playerId=id, firstname=firstname, lastname=lastname, age=age, gender=gender, skillLevel=skillLevel)

        session.add(account)
        session.add(player)
        session.commit()
        account = objs.Account(id, email, password, username)
        player = objs.Player(id, firstname, lastname, age, gender, skillLevel)
        fullUser = objs.FullUser(account, player)
        return fullUser
    except:
        return False

def login():
    print("Welcome to the login page")
    try:
        username = getInputFunctions.getUsername()
        password = hash(getInputFunctions.getPassword())
        query = f"""
            SELECT * 
            FROM accounts
            WHERE Username = "{username}" AND Password = "{password}";
        """

        result = connection.execute(db.text(query))
        rows = result.all()
        if len(rows) == 1:
            data = rows[0]
            account = objs.Account(data[0], data[1], data[2], data[3])
            player = queries.getPlayerFromAccountId(account.accountId)
            fullUser = objs.FullUser(account, player)
            return fullUser
        else:
            return False
    except:
        return False

def query_tournaments_action():
    print("Welcome to the tournament search page")
    tId = getInputFunctions.getTournamentId()
    tName = getInputFunctions.getTournamentName()
    city = getInputFunctions.getCity()
    levelMin = getInputFunctions.getSkillLevelQuery("lower")
    levelMax = getInputFunctions.getSkillLevelQuery("upper")
    sizeMin = getInputFunctions.getSize("lower")
    sizeMax = getInputFunctions.getSize("upper")
    print()

    result = queries.tournamentsQuery(tId, tName, city, levelMin, levelMax, sizeMin, sizeMax)
    if result == False:
        print("Something went wrong with the query please try again")
        return False
    elif result == []:
        print("Search didn't return any results")
        return True
    else:
        result = result[:50]
        print(tabulate(result, headers=["Tournament Id", "Tournament Name", "City", "Required Level", "Size"]))
        return True

def query_sparring_sessions_action():
    print("Welcome to the search sparring sessions page")
    sId = getInputFunctions.getSessionId() #TODO skip others if given sid
    requester = getInputFunctions.getRequester()
    responder = getInputFunctions.getResponder()
    city = getInputFunctions.getCity()
    lowerDate = getInputFunctions.getDateTime("lower")
    upperDate = getInputFunctions.getDateTime("upper")
    levelMin = getInputFunctions.getSkillLevelQuery("lower")
    levelMax = getInputFunctions.getSkillLevelQuery("upper")

    result = queries.sparringSessionsQuery(sId, requester, responder, city, lowerDate, upperDate, levelMin, levelMax)
    if result == False:
        print("Something went wrong with the query please try again")
        return False
    elif result == []:
        print("Search didn't return any results")
        return True
    else:
        queryData = []
        for row in result:
            responder = row[2]
            if responder != None:
                responder = queries.getNameFromPlayerId(responder)
            temp = [row[0], queries.getNameFromPlayerId(row[1]), responder, row[3], row[4], row[5]]
            queryData.append(temp)
        queryData = queryData[:50]
        print(tabulate(queryData, headers=["Session Id", "Requester", "Responder", "City", "Date And Time", "Required Level"]))
        return True

def query_players_action():
    print("Welcome to the search players page")
    playerId = getInputFunctions.getPlayerId()
    firstname = getInputFunctions.getNameQuery("first")
    lastname = getInputFunctions.getNameQuery("last")
    minAge = getInputFunctions.getAgeUpperLower("lower")
    maxAge = getInputFunctions.getAgeUpperLower("upper")
    gender = getInputFunctions.getGenderQuery()
    minSkill = getInputFunctions.getSkillLevelQuery("lower")
    maxSkill = getInputFunctions.getSkillLevelQuery("upper")

    result = queries.playerQuery(playerId, firstname, lastname, minAge, maxAge, gender, minSkill, maxSkill)
    if result == False:
        print("Something went wrong with the search please try again")
        return False
    elif result == []:
        print("Search didn't return any results")
        return True
    else:
        result = result[:50]
        print(tabulate(result, headers=["Player Id", "First Name", "Last Name", "Age", "Gender", "Skill Level"]))
        return True

def change_password_action(fullUser):
    print("Welcome to the password changing page")
    try:
        username = fullUser.Account.username
        password = hash(getInputFunctions.getPassword())
        query = f"""
            SELECT * 
            FROM accounts
            WHERE Username = "{username}" AND Password = "{password}";
        """
        result = connection.execute(db.text(query))
        rows = result.all()
        if len(rows) == 1:
            newPassword = hash(getInputFunctions.getNewPassword())
            result = queries.updatePasswordQuery(fullUser.Account.accountId, newPassword)
            if result:
                print("Password successfully updated!")
                return True
            else:
                print("Something went wrong please try again")
        else:
            print("Incorrect login info please try again")
            return False
    except:
        print("Something went wrong please try again")
        return False

def tournamentSignupAction(user):
    print("Welcome to the tournament signup page")
    tId = getInputFunctions.getTournamentId()
    tourneyRequiredLevel = queries.getTournamentRequiredLevel(tId)
    if tourneyRequiredLevel == False:
        print("Not a valid tournament Id")
        return False
    if queries.getPlayerLevel(user.Player.playerId) < tourneyRequiredLevel:
        print("You aren't high enough skill level for this tournament")
        return False

    result = queries.tournamentSignupQuery(user.Player.playerId, tId)
    if result == False:
        print("Something went wrong with the signup please try again")
        return False
    print("You were successfully signed up!")
    return True

def send_sparring_invitation_action(user):
    print("Welcome to the send sparring session invites page")
    sessionId = uuid.uuid4()
    city = getInputFunctions.getCity()
    time = getInputFunctions.getDateTimeNoBounds()
    requiredLevel = getInputFunctions.getSkillLevelForSparringSessionInvite()
    result = queries.sendSparringSessionInvite(user, sessionId, city, time, requiredLevel)

    if result == False:
        print("Something went wrong please try again")
        return False
    print("Succesfully sent out the session!")
    return True

def respond_to_sparring_session_action(user):
    print("Welcome to the sparring session signup page")
    sessionId = getInputFunctions.getSessionIdSparringResponse()
    sessionData = queries.getSparringSessionData(sessionId)
    if sessionData[2] is not None:
        print("Someone has already signed up for that session")
        return False
    elif user.Player.skillLevel < float(sessionData[5]):
        print("Your skill level is not high enough for this session")
        return False
    elif user.Player.playerId == sessionData[1]:
        print("You can't sign up for your own sparring session")
        return False

    result = queries.signUpForSparringSession(user, sessionId)
    if result == False:
        print("Something went wrong with the signup")
        return False
    print("You succesfully signed up for the session!")
    return True


def main_page(fullUser):
    # 1. change password
    # 2. query tournaments
    # 3. query players
    # 4. query sparring sessions
    # 5. Tournament signup
    # 6. Send sparring session invite
    # 7. Respond to sparring sessions
    while(True):
        print()
        print("Welcome to the main page, enter (Q/q) ar any time to quit.")
        print("Actions you can take: \n1. Change password \n2. Search Tournaments\n3. Search Players" + \
              "\n4. Search sparring sessions\n5. Signup for tournaments\n6. Send out sparring sessions" +\
              "\n7. Sign up for sparring sessions")
        userIn = input("Please enter the number of the action you'd like to take: ")
        if(userIn.lower() == "q"):
            quit()
        elif(userIn.lower() == "l"):
            return

        if userIn == "1":
            print()
            change_password_action(fullUser)
            print()
        elif userIn == "2":
            print()
            query_tournaments_action()
            print()
        elif userIn == "3":
            print()
            query_players_action()
            print()
        elif userIn == "4":
            print()
            query_sparring_sessions_action()
            print()
        elif userIn == "5":
            print()
            tournamentSignupAction(fullUser)
        elif userIn == "6":
            print()
            send_sparring_invitation_action(fullUser)
        elif userIn == "7":
            print()
            respond_to_sparring_session_action(fullUser)
            print()
        else:
            print("Invalid input")

def launch_page():
    done = False
    print("Welcome to Tennis Central!")
    while not done:
        userIn = input("Input 1 to login, 2 to create an account, or (Q/q) to quit the program: ")
        if userIn == "1":
            print()
            return login()
        elif userIn == "2":
            print()
            return create_account()
        elif userIn.lower() == "q":
            quit()
        else:
            print("Not a valid input")

def main_loop():
    while True:
        user = launch_page()
        if user == False:
            print("Something went wrong please try again")
            continue
        print()
        main_page(user)
        print()

if __name__ == "__main__":
    #main_loop()
    query_tournaments_action()
