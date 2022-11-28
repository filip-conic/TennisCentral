class FullUser:
    def __init__(self, account, player):
        self.Account = account
        self.Player = player

    def __str__(self):
        return "AccountId: " + str(self.Account.accountId)

class Account:
    def __init__(self, accountId, email, password, username):
        self.accountId = accountId
        self.email = email
        self.password = password
        self.username = username

    def __str__(self):
        return "AccountId: " + self.accountId + ", email: " + self.email + ", password: " + self.password + ", username: " + self.username

class Player:
    def __init__(self, playerId, firstname, lastname, age, gender, skillLevel):
        self.playerId = playerId
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.gender = gender
        self.skillLevel = skillLevel

    def __str__(self):
        return "PlayerId: " + self.playerId + ", firstname: " + self.firstname + ", lastname: " + self.lastname \
               + ", age: " + str(self.age) + ", gender: " + self.gender + ", SkillLevel: " + str(self.skillLevel)
