# models.py

from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy object
db = SQLAlchemy()


class Opportunity(db.Model):
    """
    Table for career opportunities.
    """
    __tablename__ = "opportunities"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Relationship:
    # one opportunity can have many applications
    applications = db.relationship(
        "Application",
        backref="opportunity",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Opportunity {self.title}>"


class Application(db.Model):
    """
    Table for user applications to opportunities.
    """
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    # Applicant information
    applicant_name = db.Column(db.String(100), nullable=False)
    applicant_email = db.Column(db.String(120), nullable=False)
    motivation = db.Column(db.Text, nullable=False)

    # Foreign key:
    # connects each application to one opportunity
    opportunity_id = db.Column(
        db.Integer,
        db.ForeignKey("opportunities.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Application {self.applicant_name}>"