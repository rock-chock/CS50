import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

# For DictReader and DictWriter
fieldnames_csv = ["first_name", "last_name", "degree", "topics"]


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    """Render survey form and write user's input to survey.csv file"""

    # Get user's first and last name and degree
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    degree = request.form.get("degree")
    if not request.form.get("first_name") or not request.form.get("last_name") or not request.form.get("degree"):
        return render_template("error.html", message="Please fill in all the elements of a survey")

    # Get topics he is interested in
    checkbox_values_raw = [request.form.get("it"), request.form.get("linguistics"), request.form.get("arts")]
    topics = [i for i in checkbox_values_raw if i]
    if not topics:
        return render_template("error.html", message="Please select topics you are interested in")

    # Write a row to file
    with open('survey.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_csv)
        writer.writerow({"first_name": first_name, "last_name": last_name, "degree": degree, "topics": " ".join(topics)})

    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    """Render survey.csv file"""

    # Read .csv
    with open('survey.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames_csv)
        rows = [row for row in reader]
        rows.pop(0)

    # Display all the submissions in an HTML table (Bootstrap)
    return render_template("sheet.html", rows=rows)
