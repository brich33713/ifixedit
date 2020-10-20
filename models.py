from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)


class Subcategory(db.Model):
    __tablename__ = "subcategories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.Text, nullable=False, unique=True)

    category = db.relationship("Category", backref="sub")


class Trade(db.Model):
    __tablename__ = "trades"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    category_id = db.Column(db.ForeignKey('categories.id'), nullable=False)
    cost_per_hour = db.Column(db.Integer, nullable=False)

    category = db.relationship('Category', backref="trade")


class Issue(db.Model):
    __tablename__ = "issues"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    subcategory_id = db.Column(db.ForeignKey('subcategories.id'), nullable=False)
    video_url = db.Column(db.Text, nullable=False)
    num_hours = db.Column(db.Integer)
    difficulty = db.Column(db.Text)

    subcategory = db.relationship('Subcategory', backref="issues")

    def savings(self):
        return self.num_hours * self.subcategory.category.trade[0].cost_per_hour


class Part(db.Model):
    __tablename__ = "parts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    link = db.Column(db.Text)
    image_url = db.Column(db.Text)
    price = db.Column(db.Integer)


class Issue_Parts(db.Model):
    """various parts needed for issues. One issue can have multiple parts"""
    __tablename__ = "issues_parts"
    issue_id = db.Column(db.ForeignKey('issues.id'),
                         primary_key=True, nullable=False)
    part_id = db.Column(db.ForeignKey('parts.id'),
                        primary_key=True, nullable=False)
    num_needed = db.Column(db.Integer)

    """access Issue table to get issue info 
    (name, category, video_url, num_hours, difficulty"""
    issue = db.relationship("Issue", backref="issue_parts")
    """access Part table to get part info
    (name, link, image_url, price)"""
    part = db.relationship("Part", backref="issue_parts")

class Admin(db.Model):
    """Admin user"""
    __tablename__ = "admins"
    username = db.Column(db.Text,primary_key=True,nullable=False)
    password = db.Column(db.Text,nullable=False)
