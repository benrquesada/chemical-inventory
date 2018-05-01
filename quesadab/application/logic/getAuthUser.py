'''Any function that is related to user information or authentification should
be located here.'''
from application.__init__ import *
from application.models.usersModel import *
from flask import abort

class AuthorizedUser:
    def __init__(self):
        self.username = authUser(request.environ)

    def getUsername(self):
        """returns the username"""
        return self.username

    def getUser(self):
        """returns the user object corresponding to the logged on user"""
        user = Users.select().where(Users.username == self.username)
        if user.exists():
            return user[0]
        else:
            return abort(401)

    def userLevel(self):
        """Gets the system specific user level based on username"""
        user = self.getUser()
        try:
            if user.auth_level is not None and user.approve == True:
                return user.auth_level
            else:
                return -1
        except:
            return -1
