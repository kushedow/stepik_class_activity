# Run with Python 3

import datetime
from stepik_activity import StepikActivity
from flask import Flask, render_template, request, session, redirect


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"


@app.route('/')
def render_index():

    if session.get("config_id") is None:
        return redirect("/settings/")

    class_id = request.args.get("class_id", "")

    stepic_activity = StepikActivity(session["config_id"], session["config_secret"])
    students_activity = stepic_activity.get_activity_by_class(class_id)

    return render_template("index.html", class_id=class_id, students_activity=students_activity, datetime=datetime)


@app.route('/settings/')
def render_settings():

    session["config_id"] = request.args.get("config_id", session.get("config_id", ""))
    session["config_secret"] = request.args.get("config_secret", session.get("config_secret", ""))
    return render_template("settings.html", config_id=session["config_id"], config_secret=session["config_secret"])


app.run(debug=True)

