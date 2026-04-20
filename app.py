# app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Opportunity, Application
from utils import send_application_notification

app = Flask(__name__)

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///career.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# Helper function for Opportunity API
def opportunity_to_dict(opportunity):
    return {
        "id": opportunity.id,
        "title": opportunity.title,
        "company": opportunity.company,
        "location": opportunity.location,
        "description": opportunity.description
    }


# Helper function for Application API / debugging
def application_to_dict(application):
    return {
        "id": application.id,
        "applicant_name": application.applicant_name,
        "applicant_email": application.applicant_email,
        "motivation": application.motivation,
        "opportunity_id": application.opportunity_id
    }


# ----------------------
# WEB ROUTES
# ----------------------

@app.route("/")
def home():
    """
    Home page:
    show all opportunities.
    """
    opportunities = Opportunity.query.all()
    return render_template("index.html", opportunities=opportunities)


@app.route("/add", methods=["GET", "POST"])
def add_opportunity():
    """
    Add a new opportunity.
    """
    if request.method == "POST":
        title = request.form["title"].strip()
        company = request.form["company"].strip()
        location = request.form["location"].strip()
        description = request.form["description"].strip()

        if not title or not company or not location or not description:
            return "All fields are required!", 400

        new_opportunity = Opportunity(
            title=title,
            company=company,
            location=location,
            description=description
        )

        db.session.add(new_opportunity)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("add_opportunity.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_opportunity(id):
    """
    Edit an existing opportunity.
    """
    opportunity = Opportunity.query.get_or_404(id)

    if request.method == "POST":
        title = request.form["title"].strip()
        company = request.form["company"].strip()
        location = request.form["location"].strip()
        description = request.form["description"].strip()

        if not title or not company or not location or not description:
            return "All fields are required!", 400

        opportunity.title = title
        opportunity.company = company
        opportunity.location = location
        opportunity.description = description

        db.session.commit()

        return redirect(url_for("home"))

    return render_template("edit_opportunity.html", opportunity=opportunity)


@app.route("/delete/<int:id>", methods=["POST"])
def delete_opportunity(id):
    """
    Delete an opportunity.
    Related applications are also deleted because of cascade.
    """
    opportunity = Opportunity.query.get_or_404(id)

    db.session.delete(opportunity)
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/apply/<int:id>", methods=["GET", "POST"])
def apply_opportunity(id):
    """
    Apply to a selected opportunity.
    """
    opportunity = Opportunity.query.get_or_404(id)

    if request.method == "POST":
        applicant_name = request.form["applicant_name"].strip()
        applicant_email = request.form["applicant_email"].strip()
        motivation = request.form["motivation"].strip()

        if not applicant_name or not applicant_email or not motivation:
            return "All fields are required!", 400

        new_application = Application(
            applicant_name=applicant_name,
            applicant_email=applicant_email,
            motivation=motivation,
            opportunity_id=opportunity.id
        )

        db.session.add(new_application)
        db.session.commit()

        # Simulated external action:
        # we will mock/patch this in tests
        send_application_notification(
            applicant_name,
            applicant_email,
            opportunity.title
        )

        return redirect(url_for("home"))

    return render_template("apply_opportunity.html", opportunity=opportunity)


@app.route("/applications")
def view_applications():
    """
    Show all submitted applications.
    """
    applications = Application.query.all()
    return render_template("applications.html", applications=applications)


# ----------------------
# API ROUTES
# ----------------------

@app.route("/api/opportunities", methods=["GET"])
def get_opportunities():
    opportunities = Opportunity.query.all()
    data = [opportunity_to_dict(o) for o in opportunities]
    return jsonify(data), 200


@app.route("/api/opportunities/<int:id>", methods=["GET"])
def get_opportunity(id):
    opportunity = Opportunity.query.get_or_404(id)
    return jsonify(opportunity_to_dict(opportunity)), 200


@app.route("/api/opportunities", methods=["POST"])
def create_opportunity_api():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    required_fields = ["title", "company", "location", "description"]

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Field '{field}' is required"}), 400

    new_opportunity = Opportunity(
        title=data["title"],
        company=data["company"],
        location=data["location"],
        description=data["description"]
    )

    db.session.add(new_opportunity)
    db.session.commit()

    return jsonify(opportunity_to_dict(new_opportunity)), 201


@app.route("/api/opportunities/<int:id>", methods=["PUT"])
def update_opportunity_api(id):
    opportunity = Opportunity.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    if "title" in data:
        opportunity.title = data["title"]

    if "company" in data:
        opportunity.company = data["company"]

    if "location" in data:
        opportunity.location = data["location"]

    if "description" in data:
        opportunity.description = data["description"]

    db.session.commit()

    return jsonify(opportunity_to_dict(opportunity)), 200


@app.route("/api/opportunities/<int:id>", methods=["DELETE"])
def delete_opportunity_api(id):
    opportunity = Opportunity.query.get_or_404(id)

    db.session.delete(opportunity)
    db.session.commit()

    return jsonify({"message": "Opportunity deleted successfully"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)