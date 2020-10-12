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
    return render_template("base.html")

@app.route("/search",methods=["GET"])
def search():
    issue = request.args["fix"].capitalize()
    issues = [issue.name for issue in Issue.query.all()]
    if issue in issues:
        issue = issue.replace(" ","-")
        return redirect(f"/fix/{issue}")
    words_to_omit = ["a","an","to","of","the"]
    query = issue.split()
    query = [word for word in query if word not in words_to_omit]
    possible_answers = []
    possible_issue_holder = []
    vowels = ["a","e","i","o","u"]
    for word in query:
        possible_issues = Issue.query.filter(Issue.name.like(f'%{word}%')).all()
        for possibility in possible_issues:
            if possibility.name not in possible_answers:
                possible_answers.append(possibility.name)
                possible_issue_holder.append(possibility) 
    if(len(possible_answers) == 0):
        return render_template("search-results.html",results="Search returned no results",issue=issue)
    return render_template("search-results.html",results=possible_issue_holder,vowels=vowels,issue=issue)

@app.route("/fix/<issue>")
def display_repair_page(issue):
    issue = issue.replace("-"," ")
    issue = issue.title()
    if issue[0] in ["A","E","I","O","U"]:
        vowel = True
    else:
        vowel = False
    return render_template("display-repair.html",issue=Issue.query.filter(Issue.name == issue).first(),vowel=vowel)

@app.route("/category/<category>")
def display_category(category):
    category = category.capitalize()
    category = Category.query.filter(Category.name == category).first()
    return render_template("display-category.html",subcategories=category.sub,category=category)

@app.route("/subcategory/<subcategory>")
def display_subcategory(subcategory):
    subcategory = subcategory.capitalize()
    subcategory = Subcategory.query.filter(Subcategory.name == subcategory).first()
    return render_template("display-subcategory.html",issues=subcategory.issues,subcategory=subcategory)

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
    if "Admin" in session:
        i = 0
        not_added = []
        results = request.form
        existing_categories = Category.query.all()
        results = [results[result].capitalize() for result in results if result not in existing_categories]
        for result in results:
                new_category = Category(name=result)
                db.session.add(new_category)
                db.session.commit()
                i += 1
        flash(f"Added {i} categories to database")
        return redirect("/")
    flash("Not authorized to access this page")
    return redirect("/")

@app.route("/add-issuepart",methods=["POST"])
def add_issuepart_by_form():
    if "Admin" in session:
        results = request.form
        part = Part.query.filter(Part.name == results["part"].capitalize()).first()
        issue = Issue.query.filter(Issue.name == results["issue"].title()).first()
        existing_repair_parts = [(part.issue_id, part.part_id)
                             for part in Issue_Parts.query.all()]
        if (issue.id, part.id) not in existing_repair_parts:
            new_repair_part = Issue_Parts(issue_id=issue.id,part_id=part.id)
            db.session.add(new_repair_part)
            db.session.commit()
            flash(f"{part.name} added to {issue.name}")
        return redirect("/")
    flash("Not authorized to access this page")
    return redirect("/")
    
@app.route("/add-subcategory",methods=["POST"])
def add_subcategory_by_form():
    if "Admin" in session: 
        i = 0
        not_added = []
        results = request.form
        category = Category.query.filter(Category.name == results["category"]).first()
        existing_subcategories = Subcategory.query.all()
        results = [results[result].capitalize() for result in results if result != "category" and result not in existing_subcategories]
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
    flash("Not authorized to access this page")
    return redirect("/")

@app.route("/add-trade",methods=["POST"])
def add_trade_by_form():
    i = 0
    not_added = []
    results = request.json
    category = Category.query.filter(Category.name == results["category"]).first()
    new_trade = Trade(category_id=category.id,name=results["name"].capitalize(),cost_per_hour=results["cost"])
    db.session.add(new_trade)
    db.session.commit()
    return results

@app.route("/add-part",methods=["POST"])
def add_part_by_form():
    data = request.json
    part = Part(name=data["name"].capitalize(),link=data["link"],image_url=data["image_url"],price=data["price"])
    db.session.add(part)
    db.session.commit()
    return data

@app.route("/add-issue",methods=["POST"])
def add_issue_by_form():
    data = request.json
    video_url = (data["video_url"]).replace("watch?v=","embed/")
    subcategory = Subcategory.query.filter(Subcategory.name == data["subcategory"]).first()
    new_issue = Issue(name = data["name"].title(),video_url=video_url,
    subcategory_id=subcategory.id,num_hours=data["num_hours"],difficulty=data["difficulty"])
    db.session.add(new_issue)
    db.session.commit()
    return data
####################################################################################################
"""Routes for admin to quickly add to database without form submission"""


@app.route("/quick-add-category/<category>")
def add_category(category):
    if "Admin" in session:
        new_category = Category(name=category.capitalize())
        existing_categories = [category.name.capitalize() for category in Category.query.all()]
        if category in existing_categories:
            flash(f"{category} already exists in Category table")
            return redirect("/admin")
        db.session.add(new_category)
        db.session.commit()
        flash(f"{category} added to Category table")
        return redirect("/admin")
    flash("Not authorized to access this page")
    return redirect("/")


@app.route("/quick-add-subcategory/<int:category_id>/<subcategory>")
def add_subcategory_by_id(category_id, subcategory):
    if "Admin" in session:
        new_subcategory = Subcategory(
        category_id=category_id, name=subcategory.capitalize())
        existing_subcategories = [
        category.name.capitalize() for subcategory in Subcategory.query.all()]
        if subcategory in existing_subcategories:
            flash(f"{new_subcategory.name} already exists in Subcategory tablenew_")
            return redirect("/admin-access")
        db.session.add(new_subcategory)
        db.session.commit()
        flash(f"{new_subcategory.name} added to Subcategory tablenew_")
        return redirect("/admin")
    flash("Not authorized to access this page")
    return redirect("/")


@app.route("/quick-add-subcategory/<category>/<subcategory>")
def add_subcategory_by_category(category, subcategory):
    if "Admin" in session:
        category = category.capitalize()
        category = Category.query.filter(Category.name == category).first_or_404()
        new_subcategory = Subcategory(
        category_id=category.id, name=subcategory.capitalize())
        existing_subcategories = [
        subcategory.name.capitalize() for subcategory in Subcategory.query.all()]
        if subcategory in existing_subcategories:
            flash(f"{new_subcategory.name} already exists in Subcategory table for {category.name}")
            return redirect("/admin")
        db.session.add(new_subcategory)
        db.session.commit()
        flash(f"{new_subcategory.name} added to Subcategory table for {category.name}")
        return redirect("/admin")
    flash("Not authorized to access this page")
    return redirect("/")


@app.route("/quick-add-trade/<int:category_id>/<trade_name>/<int:cost>")
def add_trade_by_id(category_id, trade_name, cost):
    if "Admin" in session:
        new_trade = Trade(category_id=category_id,
                      name=trade_name.capitalize(), cost_per_hour=cost)
        existing_trades = [trade.name.capitalize() for trade in Trade.query.all()]
        if trade in existing_trades:
            flash(f"{trade} already exists in Trade table")
            return redirect("/admin")
        db.session.add(new_trade)
        db.session.commit()
        flash(f"{trade} added to Trade table")
        return redirect("/admin")
    flash("Not authorized to access this page")
    return redirect("/")


@app.route("/quick-add-trade/category/<trade_name>/<int:cost>")
def add_trade_by_category(category, trade_name, cost):
    if "Admin" in session:
        category = Category.filter(Category.name == category).first_or_404()
        new_trade = Trade(category_id=category.id,
                      name=trade_name.capitalize(), cost_per_hour=cost)
        existing_trades = [trade.name.capitalize() for trade in Trade.query.all()]
        if trade in existing_trades:
            flash(f"{trade} already exists in Trade table")
            return redirect("/admin")
        db.session.add(new_trade)
        db.session.commit()
        flash(f"{trade} added to Trade table")
        return redirect("/admin")
    flash("Not authorized to access this page")
    return redirect("/")


@app.route("/quick-add-repair-part/<int:issue_id>/<int:part_id>")
def add_repair_part(issue_id, part_id):
    if "Admin" in session:
        new_repair_part = Issue_Parts(issue_id=issue_id, part_id=part_id)
        issue = Issue.query.get(issue_id)
        part = Part.query.get(part_id)
        existing_repair_parts = [(part.issue_id, part.part_id)
                             for part in Issue_Parts.query.all()]
        if (issue_id, part_id) in existing_repair_parts:
            flash(
            f"{issue.name} with {part.name} already exists in Issue_Parts table")
            return redirect("/admin")
        db.session.add(new_repair_part)
        db.session.commit()
        flash(f"{issue.name} with {part.name} added to Issue_Parts table")
        return redirect("/admin")
    flash("Not authorized to access this page")
    return redirect("/")


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