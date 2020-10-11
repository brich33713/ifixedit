from flask import Flask, jsonify, request, redirect, render_template, flash, session
from models import db, connect_db, Category, Subcategory, Admin, Trade, Issue, Issue_Parts, Part
from flask_debugtoolbar import DebugToolbarExtension
from forms import Admin_Login_Form
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config["SECRET_KEY"] = "repair_project"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///repair_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# debug = DebugToolbarExtension(app)
connect_db(app)
bcrypt = Bcrypt()


@app.route("/")
def homepage():
    categories = Category.query.all()
    parts = Part.query.all()
    issues = Issue.query.all()
    subcategories = Subcategory.query.all()
    return render_template("creation.html", categories=categories,subcategories=subcategories,parts=parts,issues=issues)

@app.route("/search")
def search():
    return render_template("base.html")

@app.route("/fix/<issue>")
def display_repair_page(issue):
    issue = issue.replace("-"," ")
    if issue[0] in ["a","e","i","o","u"]:
        vowel = True
    else:
        vowel = False
    return render_template("display.html",issue=Issue.query.filter(Issue.name == issue).first(),vowel=vowel)

"""Logins in admin for editing database"""


@app.route("/admin",methods=["GET","POST"])
def login_admin():
    categories = Category.query.all()
    # return render_template("base.html", category=categories)
    if "Admin" in session:
        categories = Category.query.all()
        parts = Part.query.all()
        issues = Issue.query.all()
        subcategories = Subcategory.query.all()
        return render_template("creation.html", categories=categories,subcategories=subcategories,parts=parts,issues=issues)

    form = Admin_Login_Form()
    if form.validate_on_submit():
        admin = Admin.query.filter(Admin.username == form.username.data).first()
        success = bcrypt.check_password_hash(admin.password, form.password.data)
        if admin and success:
            session["Admin"] = form.username.data
            categories = Category.query.all()
            parts = Part.query.all()
            issues = Issue.query.all()
            subcategories = Subcategory.query.all()
            return render_template("creation.html", categories=categories,subcategories=subcategories,parts=parts,issues=issues)
        else:
            form.username.errors = "Incorrect credentials"
            return render_template("admin.html",form=form)
    return render_template("admin.html",form=form) 

####################################################################################################
"""For admin to add to database using forms"""
@app.route("/add-category",methods=["POST"])
def add_category_by_form():
    i = 0
    not_added = []
    results = request.form
    existing_categories = Category.query.all()
    results = [results[result] for result in results if result not in existing_categories]
    for result in results:
            new_category = Category(name=result)
            db.session.add(new_category)
            db.session.commit()
            i += 1
    flash(f"Added {i} categories to database")
    return redirect("/")

@app.route("/add-issuepart",methods=["POST"])
def add_issuepart_by_form():
    results = request.form
    part = Part.query.filter(Part.name == results["part"]).first()
    issue = Issue.query.filter(Issue.name == results["issue"]).first()
    existing_repair_parts = [(part.issue_id, part.part_id)
                             for part in Issue_Parts.query.all()]
    if (issue.id, part.id) not in existing_repair_parts:
        new_repair_part = Issue_Parts(issue_id=issue.id,part_id=part.id)
        db.session.add(new_repair_part)
        db.session.commit()
        flash(f"{part.name} added to {issue.name}")
    return redirect("/")
    
@app.route("/add-subcategory",methods=["POST"])
def add_subcategory_by_form():
    i = 0
    not_added = []
    results = request.form
    category = Category.query.filter(Category.name == results["category"]).first()
    existing_subcategories = Subcategory.query.all()
    results = [results[result] for result in results if result != "category" and result not in existing_subcategories]
    for result in results:
        if result not in existing_subcategories and result != '':
            new_subcategory = Subcategory(category_id=category.id,name=result)
            db.session.add(new_subcategory)
            db.session.commit()
            i += 1
        else:
            not_added.append(result)
    flash(f"{i} subcategories added")
    return redirect("/")

@app.route("/add-trade",methods=["POST"])
def add_trade_by_form():
    i = 0
    not_added = []
    results = request.json
    category = Category.query.filter(Category.name == results["category"]).first()
    new_trade = Trade(category_id=category.id,name=results["name"],cost_per_hour=results["cost"])
    db.session.add(new_trade)
    db.session.commit()
    return results

@app.route("/add-part",methods=["POST"])
def add_part_by_form():
    data = request.json
    part = Part(name=data["name"],link=data["link"],image_url=data["image_url"],price=data["price"])
    db.session.add(part)
    db.session.commit()
    return data

@app.route("/add-issue",methods=["POST"])
def add_issue_by_form():
    data = request.json
    video_url = (data["video_url"]).replace("watch?v=","embed/")
    # # video_url = video_url.replace("watch?v","embed/")
    subcategory = Subcategory.query.filter(Subcategory.name == data["subcategory"]).first()
    new_issue = Issue(name = data["name"],video_url=video_url,
    subcategory_id=subcategory.id,num_hours=data["num_hours"],difficulty=data["difficulty"])
    db.session.add(new_issue)
    db.session.commit()
    return data
####################################################################################################
"""Routes for admin to quickly add to database without form submission"""


@app.route("/quick-add-category/<category>")
def add_category(category):
    new_category = Category(name=category.capitalize())
    existing_categories = [category.name for category in Category.query.all()]
    if category in existing_categories:
        flash(f"{category} already exists in Category table")
        return redirect("/admin-access")
    db.session.add(new_category)
    db.session.commit()
    flash(f"{category} added to Category table")
    return redirect("/admin-access")


@app.route("/quick-add-subcategory/<int:category_id>/<subcategory>")
def add_subcategory_by_id(category_id, subcategory):
    new_subcategory = Subcategory(
        category_id=category_id, name=subcategory.capitalize())
    existing_subcategories = [
        category.name for subcategory in Subcategory.query.all()]
    if subcategory in existing_subcategories:
        flash(f"{new_subcategory.name} already exists in Subcategory tablenew_")
        return redirect("/admin-access")
    db.session.add(new_subcategory)
    db.session.commit()
    flash(f"{new_subcategory.name} added to Subcategory tablenew_")
    return redirect("/admin-access")


@app.route("/quick-add-subcategory/<category>/<subcategory>")
def add_subcategory_by_category(category, subcategory):
    category = Category.query.filter(Category.name == category).first_or_404()
    new_subcategory = Subcategory(
        category_id=category.id, name=subcategory.capitalize())
    existing_subcategories = [
        subcategory.name for subcategory in Subcategory.query.all()]
    if subcategory in existing_subcategories:
        flash(f"{new_subcategory.name} already exists in Subcategory table for {category.name}")
        return redirect("/admin-access")
    db.session.add(new_subcategory)
    db.session.commit()
    flash(f"{new_subcategory.name} added to Subcategory table for {category.name}")
    return redirect("/admin-access")


@app.route("/quick-add-trade/<int:category_id>/<trade_name>/<int:cost>")
def add_trade_by_id(category_id, trade_name, cost):
    new_trade = Trade(category_id=category_id,
                      name=trade_name, cost_per_hour=cost)
    existing_trades = [trade.name for trade in Trade.query.all()]
    if trade in existing_trades:
        flash(f"{trade} already exists in Trade table")
        return redirect("/admin-access")
    db.session.add(new_trade)
    db.session.commit()
    flash(f"{trade} added to Trade table")
    return redirect("/admin-access")


@app.route("/quick-add-trade/category/<trade_name>/<int:cost>")
def add_trade_by_category(category, trade_name, cost):
    category = Category.filter(Category.name == category).first_or_404()
    new_trade = Trade(category_id=category.id,
                      name=trade_name, cost_per_hour=cost)
    existing_trades = [trade.name for trade in Trade.query.all()]
    if trade in existing_trades:
        flash(f"{trade} already exists in Trade table")
        return redirect("/admin-access")
    db.session.add(new_trade)
    db.session.commit()
    flash(f"{trade} added to Trade table")
    return redirect("/admin-access")


@app.route("/quick-add-repair-part/<int:issue_id>/<int:part_id>")
def add_repair_part(issue_id, part_id):
    new_repair_part = Issue_Parts(issue_id=issue_id, part_id=part_id)
    issue = Issue.query.get(issue_id)
    part = Part.query.get(part_id)
    existing_repair_parts = [(part.issue_id, part.part_id)
                             for part in Issue_Parts.query.all()]
    if (issue_id, part_id) in existing_repair_parts:
        flash(
            f"{issue.name} with {part.name} already exists in Issue_Parts table")
        return redirect("/admin-access")
    db.session.add(new_repair_part)
    db.session.commit()
    flash(f"{issue.name} with {part.name} added to Issue_Parts table")
    return redirect("/admin-access")


# API
@app.route("/api/issues")
def get_issues():
    issues = [issue.name for issue in Issue.query.all()]
    return jsonify(issues = issues)

@app.route("/api/issue-parts")
def get_all_issue_parts():
    parts = Part.query.all()
    parts = [part.name for part in parts]
    issues = Issue.query.all()
    issues = [issue.name for issue in issues]
    return jsonify(response = {"parts": parts,
                "issues": issues})

