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
        print(days)
        # And show them on the page
        return render_template("pages/home.jinja", days=days, lessons = lessons)


#-----------------------------------------------------------
# About page route
#-----------------------------------------------------------
@app.get("/about/")
def about():
    return render_template("pages/about.jinja")


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
@app.get("/thing/<int:id>")
def show_one_thing(id):
    with connect_db() as client:
        # Get the thing details from the DB
        sql = "SELECT id, name, price FROM things WHERE id=?"
        params = [id]
        result = client.execute(sql, params)

        # Did we get a result?
        if result.rows:
            # yes, so show it on the page
            thing = result.rows[0]
            return render_template("pages/thing.jinja", thing=thing)

        else:
            # No, so show error
            return not_found_error()


#-----------------------------------------------------------
# Route for adding a lessons, using data posted from a form
#-----------------------------------------------------------
@app.post("/add")
def add_a_lesson():
    # Get the data from the form
    name  = request.form.get("name")
    price = request.form.get("price")

    # Sanitise the text inputs
    name = html.escape(name)

    with connect_db() as client:
        # Add the lesson to the DB
        sql = "INSERT INTO lessons (name, price) VALUES (?, ?)"
        params = [name, price]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"lesson '{name}' added", "success")
        return redirect("/")


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

        # Go back to the home page
        flash("Lesson deleted", "success")
        # no work !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return redirect("/day/{day}")


