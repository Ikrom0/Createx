from datetime import date, datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    card_img = db.Column(db.String(255), nullable=False)
    image_lg = db.Column(db.String(255), nullable=False)
    image_sm = db.Column(db.String(255), nullable=False)

    goal = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    client = db.Column(db.String(100), nullable=False)
    architect = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Project {self.title}>"


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image_sm = db.Column(db.String(255), nullable=False)
    image_lg = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, default=date.today)
    content = db.Column(db.Text, nullable=False)

    comments = db.relationship(
        "ArticleComment", backref="article", cascade="all, delete-orphan", lazy=True
    )


class ArticleComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, default=date.today)

    article_id = db.Column(db.Integer, db.ForeignKey("article.id"), nullable=False)


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    category = db.Column(db.String(100))
    city = db.Column(db.String(100))
    contact = db.Column(db.String(50))


class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CareerApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    message = db.Column(db.TEXT)
    cv_file = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Admin {self.username}>"