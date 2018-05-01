from application import app
from flask import render_template

@app.errorhandler(401)
def unauthorized(e):
    return render_template("errors/401.html"), 401