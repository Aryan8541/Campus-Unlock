"""
Campus Unlock — Lead Model
===========================
Represents an inbound lead/inquiry captured from the site (e.g. a
lead-gen form submission). No foreign keys to University/Program yet
— interested_university / interested_program are stored as plain
text for now, per current requirements.
"""

from datetime import datetime

from models import db


class Lead(db.Model):
    __tablename__ = "leads"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(180), nullable=True, index=True)
    mobile = db.Column(db.String(20), nullable=True, index=True)
    city = db.Column(db.String(120), nullable=True)
    state = db.Column(db.String(120), nullable=True)
    interested_university = db.Column(db.String(200), nullable=True)
    interested_program = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text, nullable=True)
    source = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), nullable=False, default="New", index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self):
        return f"<Lead id={self.id} full_name={self.full_name!r} status={self.status!r}>"
