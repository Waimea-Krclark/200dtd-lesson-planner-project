#===========================================================
# LESSON PLANNER
# Kieran Clark
#-----------------------------------------------------------
# A weekly lesson planer with resources
#===========================================================

from flask import Flask, render_template, request, flash, redirect
import html

from app.helpers.session import init_session
from app.helpers.db      import connect_db
from app.helpers.errors  import init_error, not_found_error
from app.helpers.logging import init_logging
from app.helpers.dates   import init_datetime, utc_datetime_str, utc_date_str, utc_time_str


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
        # Get all the days from the DB
        sql = "SELECT id, name, code FROM days ORDER BY id DESC"
        params = []
        result = client.execute(sql, params)
        days = result.rows
        # get all lessons
        sql = "SELECT id, name, day_code, time FROM lessons ORDER BY time ASC"
        params = []
        result = client.execute(sql, params)
        lessons = result.rows

        # And show them on the page
        return render_template("pages/home.jinja", days=days, lessons = lessons)

#-----------------------------------------------------------
# Day page route - Show all the lessons with details and options for a day
#-----------------------------------------------------------
@app.get("/day/<string:code>")
def show_all_lessons(code):
    with connect_db() as client:
        # Get all the lessons from the DB
        sql = "SELECT * FROM lessons WHERE day_code=? ORDER BY time ASC"
        params = [code]
        result = client.execute(sql, params)
        lessons = result.rows
        # Get the relevant date and name of the day 
        sql = "SELECT code, name FROM days WHERE code=?"
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
# Add Lesson page route
#-----------------------------------------------------------
@app.get("/addlesson/")
def add_lesson():
    # Reroutes to the page with lesson form
    return render_template("pages/addLesson.jinja")

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
# Route for deleting a lesson, Id given in the route
#-----------------------------------------------------------
@app.get("/delete/<int:id>/<string:day>")
def delete_a_lesson(id, day):
    with connect_db() as client:
        # Delete the Lesson from the DB
        sql = "DELETE FROM lessons WHERE id=?"
        params = [id]
        client.execute(sql, params)

        # Gets resources connected to the lesson
        sql = "SELECT * FROM resources WHERE lesson_id=?" 
        params = [id]
        result = client.execute(sql, params)
        resources = result.rows

        # Checks if any exist, if so resolve resource conflicts
        if(resources):
            return redirect(f"/conflict/{id}")

        #Returns back to the original day page
        flash("Lesson deleted", "success")

        return redirect(f"/day/{day}")

#-----------------------------------------------------------
# Route to resource conflicts (WHEN DELETING A LESSON WITH RESOURCES)
#-----------------------------------------------------------
@app.get("/conflict/<int:lesson_id>")
def reconfigure_resource(lesson_id):
    with connect_db() as client:
        # Get the resources  from the DB
        sql = "SELECT * FROM resources WHERE lesson_id = ?" 
        params = [lesson_id]
        result = client.execute(sql, params)
        resources = result.rows
        # Retrieve other resources to add to selection
        sql = "SELECT id, name, day_code FROM lessons" 
        params = []
        result = client.execute(sql, params)
        lessons = result.rows

        return render_template("pages/resourceConflict.jinja", resources=resources, lessons=lessons, lesson_id=lesson_id)

#-----------------------------------------------------------
# Route For updating conflicts
#-----------------------------------------------------------
@app.post("/updateConflicts/<int:lesson_id>")
def update_conflicts(lesson_id):
    # Get the data from the form
    lesson = request.form.get("lesson")

    with connect_db() as client:
        # Get the new lesson id from the name posted by the form
        sql = "SELECT id FROM lessons WHERE name=?"
        params = [lesson]
        result = client.execute(sql, params)
        lesson = result.__getitem__(0)
        # Set the resources lesson_id to the new one retrieved from the form
        sql = "UPDATE resources SET lesson_id = ? WHERE lesson_id = ?;"
        params = [lesson[0], lesson_id]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"Resource conflict resolved", "success")
        return redirect("/")

#-----------------------------------------------------------
# Route For deleting conflicts
#-----------------------------------------------------------
@app.get("/removeConflicts/<int:lesson_id>")
def delete_conflicts(lesson_id):
    with connect_db() as client:
        # Delete the conflicting resources from the DB
        sql = "DELETE FROM resources WHERE lesson_id=?"
        params = [lesson_id]
        client.execute(sql, params)

        #Returns back to the resources page
        flash("Resource conflict solved", "success")

        return redirect("/")

#-----------------------------------------------------------
# Resource page route - Show all resources
#-----------------------------------------------------------
@app.get("/resources/")
def show_resources():
    with connect_db() as client:
        # Get the resources from the DB
        sql = "SELECT * FROM resources ORDER BY lesson_id asc" 
        params = []
        result = client.execute(sql, params)
        resources = result.rows
        # Get the lessons as well
        sql = "SELECT id, name FROM lessons" 
        params = []
        result = client.execute(sql, params)
        lessons = result.rows

        return render_template("pages/resources.jinja", resources=resources, lessons=lessons)
    
#-----------------------------------------------------------
# Editing Resource Route - gets needed info then reroutes to the update page
#-----------------------------------------------------------
@app.get("/editResource/<int:resource_id>/<int:lesson_id>")
def edit_resource(resource_id, lesson_id):
    with connect_db() as client:
        # Get the resources  from the DB
        sql = "SELECT * FROM resources WHERE id = ?" 
        params = [resource_id]
        result = client.execute(sql, params)
        resource = result.__getitem__(0)
        # Get the lesson that the resource is linked to
        sql = "SELECT * FROM lessons WHERE id = ?" 
        params = [lesson_id]
        result = client.execute(sql, params)
        current_lesson = result.__getitem__(0)
        # Retrieve other resources to add to selection
        sql = "SELECT id, name, day_code FROM lessons" 
        params = []
        result = client.execute(sql, params)
        lessons = result.rows

        return render_template("pages/editResource.jinja", resource=resource, lessons=lessons, resource_id=resource_id, current_lesson=current_lesson)

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
        # get the code of lesson
        sql = "SELECT id FROM lessons WHERE name=?"
        params = [lesson]
        result = client.execute(sql, params)
        lesson = result.__getitem__(0)
        # Add the resource to the DB
        sql = "INSERT INTO resources (name, notes, link, lesson_id) VALUES (?, ?, ?, ?)"
        params = [name, notes, link, lesson[0]]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"resource '{name}' added", "success")
        return redirect("/resources/")

#-----------------------------------------------------------
# Route for editing a resources, using data posted from a form
#-----------------------------------------------------------
@app.post("/updateResource/<int:resource_id>")
def edit_a_resource(resource_id):
    # Get the data from the form
    name  = request.form.get("name")
    lesson = request.form.get("lesson")
    link = request.form.get("link")
    notes = request.form.get("notes")

    # Sanitise the text inputs
    name = html.escape(name)

    with connect_db() as client:
        # get the code of the new lesson
        sql = "SELECT id FROM lessons WHERE name=?"
        params = [lesson]
        result = client.execute(sql, params)
        lesson = result.__getitem__(0)
        # Update the resoure with the new data
        sql = "UPDATE resources SET name = ?, notes = ?, link = ?, lesson_id = ? WHERE id = ?;"
        params = [name, notes, link, lesson[0], resource_id]
        client.execute(sql, params)

        # Return to the resources page
        flash(f"resource '{name}' updated", "success")
        return redirect("/resources/")

#-----------------------------------------------------------
# Route for deleting a resource, Id given in the route
#-----------------------------------------------------------
@app.get("/remove/<int:id>")
def delete_a_resource(id):
    with connect_db() as client:
        # Delete the resource from the DB
        sql = "DELETE FROM resources WHERE id=?"
        params = [id]
        client.execute(sql, params)

        #returns back to the resources page
        flash("Lesson deleted", "success")

        return redirect("/resources/")
