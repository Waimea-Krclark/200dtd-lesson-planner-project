#===========================================================
# YOUR PROJECT TITLE HERE
# YOUR NAME HERE
#-----------------------------------------------------------
# BRIEF DESCRIPTION OF YOUR PROJECT HERE
#===========================================================

from flask import Flask, render_template, request, flash, redirect
import html

from app.helpers.session import init_session
from app.helpers.db      import connect_db
from app.helpers.errors  import init_error, not_found_error
from app.helpers.logging import init_logging
from app.helpers.time    import init_datetime, utc_timestamp, utc_timestamp_now


# Create the app
app = Flask(__name__)

# Configure app
init_session(app)   # Setup a session for messages, etc.
init_logging(app)   # Log requests
init_error(app)     # Handle errors and exceptions
init_datetime(app)  # Handle UTC dates in timestamps


#-----------------------------------------------------------
# Home page route
#-----------------------------------------------------------
@app.get("/")
def index():
    with connect_db() as client:
        # Get all the things from the DB
        sql = "SELECT id, name, code FROM days ORDER BY id DESC"
        params = []
        result = client.execute(sql, params)
        days = result.rows
        sql = "SELECT id, name, day_code, time FROM lessons ORDER BY time ASC"
        params = []
        result = client.execute(sql, params)
        lessons = result.rows

        # And show them on the page
        return render_template("pages/home.jinja", days=days, lessons = lessons)


#-----------------------------------------------------------
# About page route
#-----------------------------------------------------------
@app.get("/addlesson/")
def about():
    return render_template("pages/addLesson.jinja")


#-----------------------------------------------------------
# Day page route - Show all the lessons with details and options for a day
#-----------------------------------------------------------
@app.get("/day/<string:code>")
def show_all_things(code):
    with connect_db() as client:
        # Get all the lessons from the DB
        sql = "SELECT * FROM lessons WHERE day_code=? ORDER BY time ASC"
        params = [code]
        result = client.execute(sql, params)
        lessons = result.rows
        # Get the relevant date and name of the day 
        sql = "SELECT code, name, date FROM days WHERE code=?"
        params = [code]
        result = client.execute(sql, params)
        day = result.__getitem__(0)
        # Get all resources
        sql = "SELECT id, name, lesson_id, link FROM resources ORDER BY name ASC"
        params = []
        result = client.execute(sql, params)
        resources = result.rows

        # And show them on the page
        return render_template("pages/day.jinja", lessons=lessons, day=day, resources=resources)


#-----------------------------------------------------------
# Thing page route - Show details of a single thing
#-----------------------------------------------------------
@app.get("/resources/")
def show_resources():
    with connect_db() as client:
        # Get the resources  from the DB
        sql = "SELECT * FROM resources" 
        params = []
        result = client.execute(sql, params)
        resources = result.rows

        sql = "SELECT id, name FROM lessons" 
        params = []
        result = client.execute(sql, params)
        lessons = result.rows

        return render_template("pages/resources.jinja", resources=resources, lessons=lessons)

#-----------------------------------------------------------
# Route for adding a lessons, using data posted from a form
#-----------------------------------------------------------
@app.post("/addLesson")
def add_a_lesson():
    # Get the data from the form
    name  = request.form.get("name")
    time = request.form.get("time")
    day = request.form.get("day")
    description = request.form.get("description")

    # Sanitise the text inputs
    name = html.escape(name)

    with connect_db() as client:
        # get the code of the selected day
        sql = "SELECT code FROM days WHERE name=?"
        params = [day]
        result = client.execute(sql, params)
        day = result.__getitem__(0)
        # Add the lesson to the DB
        sql = "INSERT INTO lessons (name, description, time, day_code) VALUES (?, ?, ?, ?)"
        params = [name, description, time, day[0]]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"lesson '{name}' added", "success")
        return redirect("/")

#-----------------------------------------------------------
# Route for adding a resources, using data posted from a form
#-----------------------------------------------------------
@app.post("/addResource")
def add_a_resource():
    # Get the data from the form
    name  = request.form.get("name")
    lesson = request.form.get("lesson")
    link = request.form.get("link")
    notes = request.form.get("notes")

    # Sanitise the text inputs
    name = html.escape(name)

    with connect_db() as client:
        # get the code of the selected day
        sql = "SELECT id FROM lessons WHERE name=?"
        params = [lesson]
        result = client.execute(sql, params)
        lesson = result.__getitem__(0)
        # Add the lesson to the DB
        sql = "INSERT INTO resources (name, notes, link, lesson_id) VALUES (?, ?, ?, ?)"
        params = [name, notes, link, lesson[0]]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"resource '{name}' added", "success")
        return redirect("/resources/")

#-----------------------------------------------------------
# Route for deleting a lesson, Id given in the route
#-----------------------------------------------------------
@app.get("/delete/<int:id><string:day>")
def delete_a_lesson(id, day):
    with connect_db() as client:
        # Delete the Lesson from the DB
        sql = "DELETE FROM lessons WHERE id=?"
        params = [id]
        client.execute(sql, params)

        #returns back to the original day page
        flash("Lesson deleted", "success")

        return redirect(f"/day/{day}")


