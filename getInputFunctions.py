import re
import datetime

def getEmail():
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email = ""
    done = False
    while not done:
        done = True
        email = input("Please enter your email: ")
        if('@' not in email):
            done = False
            print("Not a valid email")
        elif(email == ""):
            done = False
            print("Not a valid email")
        elif(not re.fullmatch(regex, email)):
            done = False
            print("Not a valid email")
    return email

def getUsername():
    username = ""
    done = False
    while not done:
        done = True
        username = input("Please enter your username: ")
        if(username == ""):
            done = False
            print("Not a valid username")
    return username

def getPassword():
    password = ""
    done = False
    while not done:
        done = True
        password = input("Please enter your password: ")
        if(password == ""):
            done = False
            print("Not a valid password")
    return password

def getNewPassword():
    password = ""
    done = False
    while not done:
        done = True
        password = input("Please enter your new password: ")
        if (password == ""):
            done = False
            print("Not a valid password")
    return password

def getName(whichName):
    regex = '[A-Za-z]{2,25}([A-Za-z]{2,25})?'
    name = ""
    done = False
    while not done:
        done = True
        name = input("Please enter your " + whichName + " name: ")
        if(name == ""):
            print("Not a valid " + whichName + " name")
            done = False
        elif not re.fullmatch(regex, name):
            print("Not a valid " + whichName + " name")
            done = False
    return name

def getAge():
    age = None
    done = False
    while not done:
        done = True
        age = input("Please enter your age: ")
        try:
            age = int(age)
            if age < 0:
                done = False
                print("Not a valid age")
            if done:
                return age
        except:
            done = False
            print("Not a valid age")

def getGender():
    while True:
        gender = input("Please input your gender (M/F): ")
        gender = gender.lower()
        if gender == "m":
            return "Male"
        elif gender == "f":
            return "Female"
        print("Not one of the options")

def getSkillLevel():
    while True:
        done = True
        level = input("Please input your skill level (0.0 - 10.0): ")
        try:
            level = float(level)
            if(level < 0.0 or level > 10.0):
                print("Level outside of possible ranges")
                done = False
            if done:
                return level
        except:
            print("Not a valid skill level")

def getSkillLevelForSparringSessionInvite():
    while True:
        done = True
        level = input("Please input a skill level (0.0 - 10.0): ")
        try:
            level = float(level)
            if(level < 0.0 or level > 10.0):
                print("Level outside of possible ranges")
                done = False
            if done:
                return level
        except:
            print("Not a valid skill level")

def getTournamentId():
    while True:
        id = input("Please input a tournament id or leave the entry empty to not search by tournament id: ")
        parts = id.split("-")
        if(len(parts[0]) == 8 and len(parts[1]) == 4 and len(parts[2]) == 4 and len(parts[3]) == 4 and len(parts[4]) == 12 or id == ""):
            return id
        print("Not a valid tournamentId")

def getTournamentName():
    return input("Please input a tournament name or leave the entry empty to not search by tournament name: ")

def getCity():
    return input("Please input a city or leave the entry empty to not search by city: ")

def getSkillLevelQuery(upperLower):
    while True:
        done = True
        level = input("Please input a " + upperLower + " skill level (0.0 - 10.0) or leave it empty to not search by a " + upperLower + "bound: ")
        try:
            if level == "":
                return level
            level = float(level)
            if(level < 0.0 or level > 10.0):
                print("Level outside of possible ranges")
                done = False
            if done:
                return level
        except:
            print("Not a valid skill level")

def getAgeUpperLower(upperLower):
    while True:
        done = True
        age = input("Please input a " + upperLower + " bound for age or leave it empty to not search by a " + upperLower + "bound: ")
        try:
            if age == "":
                return age
            age = int(age)
            if(age < 0):
                print("Age cannot be negative")
                done = False
            if done:
                return age
        except:
            print("Not a valid age")

def getSize(upperLower):
    while True:
        done = True
        size = input("Please input a " + upperLower + " bound for size or leave it empty to not search by a " + upperLower + "bound: ")
        try:
            if size == "":
                return size
            size = int(size)
            if(size < 0):
                print("Size cannot be negative")
                done = False
            if done:
                return size
        except:
            print("Not a valid skill size")

def getSessionId():
    while True:
        id = input("Please input a sessionId or leave it empty to not search by a sessionId: ")
        parts = id.split("-")
        if(len(parts[0]) == 8 and len(parts[1]) == 4 and len(parts[2]) == 4 and len(parts[3]) == 4 and len(parts[4]) == 12 or id == ""):
            return id
        print("Not a valid SessionId")

def getSessionIdSparringResponse():
    while True:
        id = input("Please input a sessionId: ")
        parts = id.split("-")
        if(len(parts[0]) == 8 and len(parts[1]) == 4 and len(parts[2]) == 4 and len(parts[3]) == 4 and len(parts[4]) == 12 or id == ""):
            return id
        print("Not a valid SessionId")

def getRequester():
    while True:
        id = input("Please input a requesterId or leave it empty to not search by a requesterId: ")
        parts = id.split("-")
        if (len(parts[0]) == 8 and len(parts[1]) == 4 and len(parts[2]) == 4 and len(parts[3]) == 4 and len(
                parts[4]) == 12 or id == ""):
            return id
        print("Not a valid RequesterId")

def getResponder():
    while True:
        id = input("Please input a responderId or leave it empty to not search by a responderId: ")
        parts = id.split("-")
        if (len(parts[0]) == 8 and len(parts[1]) == 4 and len(parts[2]) == 4 and len(parts[3]) == 4 and len(
                parts[4]) == 12 or id == ""):
            return id
        print("Not a valid ResponderId")

def getPlayerId():
    while True:
        id = input("Please input a playerId or leave it empty to not search by a playerId: ")
        parts = id.split("-")
        if (len(parts[0]) == 8 and len(parts[1]) == 4 and len(parts[2]) == 4 and len(parts[3]) == 4 and len(
                parts[4]) == 12 or id == ""):
            return id
        print("Not a valid playerId")

def getDateTime(upperLower):
    while True:
        time = input("Please input a " + upperLower + " bound time (MM/DD/YYYY or MM/DD/YYYY 4:50 AM) or leave it empty to not search by a " \
                                       + upperLower + " bound time: ")
        if time == "":
            return time
        try:
            time = datetime.datetime.strptime(time, "%m/%d/%Y")
            return time
        except:
            pass
        try:
            time = datetime.datetime.strptime(time, '%m/%d/%Y %I:%M %p')
        except:
            pass
        print("Not a valid date format")

def getDateTimeNoBounds():
    while True:
        time = input("Please input a time (MM/DD/YYYY or MM/DD/YYYY 4:50 AM) for your sparring session: ")
        try:
            time = datetime.datetime.strptime(time, "%m/%d/%Y")
            return time
        except:
            pass
        try:
            time = datetime.datetime.strptime(time, '%m/%d/%Y %I:%M %p')
            return time
        except:
            pass
        print("Not a valid date format")

def getNameQuery(whichName):
    regex = '[A-Za-z]{2,25}([A-Za-z]{2,25})?'
    name = ""
    done = False
    while not done:
        done = True
        name = input("Please enter your " + whichName + " name: ")
        if name == "":
            return ""
        if not re.fullmatch(regex, name):
            print("Not a valid " + whichName + " name")
            done = False
    return name

def getGenderQuery():
    while True:
        gender = input("Please input your gender (M/F): ")
        gender = gender.lower()
        if gender == "":
            return ""
        elif gender == "m":
            return "Male"
        elif gender == "f":
            return "Female"
        print("Not one of the options")

if __name__ == "__main__":
    print(getDateTime("lower"))