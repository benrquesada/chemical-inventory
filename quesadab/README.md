# About This Application

To build this application you must...
1. Run the setup file with the command
	source setup.sh
2. Populate the database with generic values
	python reset-db.py
3. Add your current machine user id to admin in config/role.yaml 
4. Start Appache server to serve application
	python run.py
5. Open 0.0.0.0:8000 in your browser

# Relevant Documentation

To work on this application, you'll probably want:

* The Flask Documentation

  http://flask.pocoo.org/

* The Jinja Documentation

  http://jinja.pocoo.org/docs/dev/

* The PeeWee Documentation

  http://docs.peewee-orm.com/en/latest/index.html

* The Configure Documentation

  http://configure.readthedocs.io/en/latest/#

That's most of what comes to mind...
