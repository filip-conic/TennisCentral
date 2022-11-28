import sqlalchemy as db
import databasetables
import databaseObjects as objs
from sqlalchemy import create_engine, Column, String, Table, Integer, Float, DateTime
from sqlalchemy.orm import Session, sessionmaker, declarative_base
import urllib.parse
import sys, random, os, uuid
import datetime
import getInputFunctions

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

def getNameFromPlayerId(id):
    try:
        query = f"""
            SELECT * FROM players
            WHERE PlayerId = "{id}"
        """
        result = connection.execute(db.text(query)).all()
        return result[0][1] + " " + result[0][2]
    except Exception as e:
        print(e)
        return False

def tournamentsQuery(tId, name, city, minSkill, maxSkill, minSize, maxSize):
    emptyQuery = False
    if(tId == "" and name == "" and city == ""  and minSkill == "" and maxSkill == "" and minSize == "" and maxSize == ""):
        emptyQuery = True

    try:
        baseQuery = 'SELECT * FROM tournaments'
        if emptyQuery:
            result = connection.execute(db.text(baseQuery))
            return result.all()

        query = baseQuery + " WHERE"
        parameters = [tId, name, city, minSkill, maxSkill, minSize, maxSize]
        idToParam = {0:" TournamentId = ", 1:" TournamentName = ", 2:" City = ", 3:" RequiredLevel > ", 4:" RequiredLevel < ", 5:" Size > ", 6:" Size < "}
        firstParam = True
        for i in range(7):
            if(parameters[i] != ""):
                if not firstParam:
                    query = query + " AND"
                curParam = parameters[i]
                if i < 3:
                    curParam = "\"" + str(curParam) + "\""
                query = query + idToParam[i] + str(curParam)
                firstParam = False
        query = query + ";"

        result = connection.execute(db.text(query))
        rows = result.all()
        return rows

    except Exception as e:
        print(e)
        return False

def sparringSessionsQuery(sId, requester, responder, city, lowerDate, upperDate, lowerSkill, upperSkill):
    baseQuery = "SELECT * FROM sparringSessions"
    if(sId == "" and requester == "" and responder == "" and city == "" and lowerDate == "" and upperDate == "" and lowerSkill == "" and upperSkill == ""):
        result = connection.execute(db.text(baseQuery))
        return result.all()

    try:
        query = baseQuery + " WHERE"
        parameters = [sId, requester, responder, city, lowerDate, upperDate, lowerSkill, upperSkill]
        idxToParam = {0:" SessionId = ", 1:" Requester = ", 2:" Responder = ", 3:" City = ", 4:" DateAndTime > ", 5:" DateAndTime < ", 6:" RequiredLevel > ", 7:" RequiredLevel < "}
        firstParam = True
        for i in range(8):
            if(parameters[i] != ""):
                if not firstParam:
                    query = query + " AND"
                curParam = parameters[i]
                if i < 6:
                    curParam = "\"" + str(curParam) + "\""
                query = query + idxToParam[i] + str(curParam)
                firstParam = False
        query = query + ";"
        result = connection.execute(db.text(query))
        return result.all()

    except Exception as e:
        print(e)
        return False

def playerQuery(pId, firstname, lastname, minAge, maxAge, gender, minSkill, maxSkill):
    baseQuery = "SELECT * FROM players"
    if(pId == "" and firstname == "" and lastname == "" and minAge == "" and maxAge == "" and gender == "" and minSkill == "" and maxSkill == ""):
        result = connection.execute(db.text(baseQuery))
        return result.all()

    try:
        query = baseQuery + " WHERE"
        params = [pId, firstname, lastname, minAge, maxAge, gender, minSkill, maxSkill]
        idxToParam = {0:" PlayerId = ", 1:" FirstName = ", 2:" LastName = ", 3:" Age > ", 4:" Age < ", 5:" Gender = ", 6:" SkillLevel > ", 7:" SkillLevel < "}
        firstParam = True
        for i in range(8):
            if(params[i] != ""):
                if not firstParam:
                    query = query + " AND"
                curParam = params[i]
                if i < 4 or i == 5:
                    curParam = "\"" + str(curParam) + "\""
                query = query + idxToParam[i] + str(curParam)
                firstParam = False
        query = query + ";"
        print(query)
        result = connection.execute(db.text(query))
        return result.all()

    except Exception as e:
        print(e)
        return False

def getPlayerFromAccountId(accountId):
    try:
        query = f"""
            SELECT * 
            FROM players
            WHERE PlayerId = "{accountId}" 
        """
        result = connection.execute(db.text(query))
        rows = result.all()
        if len(rows) == 1:
            data = rows[0]
            player = objs.Player(data[0], data[1], data[2], data[3], data[4], float(data[5]))
            return player
    except Exception as e:
        print(e)
        return False

def updatePasswordQuery(accountId, newPassword):
    try:
        query = f"""
            UPDATE accounts
            SET password = \"{newPassword}\"
            WHERE AccountId = \"{accountId}\"
        """
        result = connection.execute(db.text(query))
        connection.commit()
        session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def getTournamentRequiredLevel(tId):
    try:
        query = f"""
            SELECT * FROM tournaments WHERE TournamentId = "{tId}";
        """
        result = connection.execute(db.text(query))
        row = result.all()[0]
        return float(row[3])
    except Exception as e:
        print(e)
        return False

def getPlayerLevel(pId):
    try:
        query = f"""
            SELECT * FROM players WHERE PlayerId = "{pId}";
        """
        result = connection.execute(db.text(query))
        row = result.all()[0]
        return float(row[5])
    except Exception as e:
        print(e)
        return False

def getSparringSessionData(sId):
    try:
        query = f"""
            SELECT * FROM sparringSessions WHERE SessionId = "{sId}";
        """
        result = connection.execute(db.text(query))
        row = result.all()[0]
        return row
    except Exception as e:
        print(e)
        return False

def tournamentSignupQuery(pId, tId):
    try:
        query = f"""
            INSERT INTO tournamentPlayers (TourneyPlayerId, TourneyId)
            VALUES
                ("{pId}", "{tId}")
        """
        result = connection.execute(db.text(query))
        connection.commit()
        session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def sendSparringSessionInvite(user, sessionId, city, time, requiredLevel):
    try:
        query = f"""
            INSERT INTO sparringSessions (SessionId, Requester, Responder, City, DateAndTime, RequiredLevel)
            VALUES
                ("{sessionId}", "{user.Player.playerId}", null, "{city}", "{time}", "{requiredLevel}");
        """
        result = connection.execute(db.text(query))
        connection.commit()
        session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def signUpForSparringSession(user, sessionId):
    try:
        query = f"""
            UPDATE sparringSessions
            SET Responder = \"{user.Player.playerId}\"
            WHERE SessionId = \"{sessionId}\"
        """
        result = connection.execute(db.text(query))
        connection.commit()
        session.commit()
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    #(pId, firstname, lastname, minAge, maxAge, gender, minSkill, maxSkill)
    #print(playerQuery("", "", "", "54", "", "Male", "2.3", "7.2"))
    #print(hash("test"))
    #print(updatePasswordQuery("00206913-3cef-4aa3-966f-889e3c8895f3", "4418353137104490830"))
    print(getSparringSessionData("1e2eb5a0-1450-49de-a98e-cae969330408"))

