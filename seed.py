from app import app
from models import db, Category, Subcategory, Admin, Trade, Issue, Issue_Parts, Part
from flask_bcrypt import Bcrypt

db.drop_all()
db.create_all()

category = Category(name="Plumbing")
category1 = Category(name="Auto")
db.session.add_all([category, category1])
db.session.commit()

subcategory = Subcategory(category_id=category.id, name="toilets")
subcategory1 = Subcategory(category_id=category.id, name="engines")
trade = Trade(category_id=category.id, name="Plumber", cost_per_hour=12)
trade1 = Trade(category_id=category1.id, name="Mechanic", cost_per_hour=24)
part = Part(name="hammer", link="https://www.walmart.com/ip/Hyper-Tough-16-Ounce-Claw-Hammer-with-Fiberglass-Handle/972830002", 
image_url="https://i5.walmartimages.com/asr/61b5ab99-2d90-45fe-9952-0932abf84c05_1.e755cf112171a90e30833bd8429a2bad.jpeg?odnWidth=100&odnHeight=100&odnBg=ffffff", price=14)
part1 = Part(name="wrench", link="google.com", image_url="google.com", price=4)
db.session.add_all([subcategory, subcategory1, trade, trade1, part, part1])
db.session.commit()

issue = Issue(name="running toilet", subcategory_id=subcategory.id,
              video_url="https://www.youtube.com/embed/DoqzGyC92GQ", num_hours=1, difficulty="easy")
db.session.add(issue)
db.session.commit()

issue_part = Issue_Parts(issue_id=issue.id, part_id=part.id)
issue_part1 = Issue_Parts(issue_id=issue.id, part_id=part1.id)
db.session.add_all([issue_part, issue_part1])
db.session.commit()

bcrypt = Bcrypt()
password = bcrypt.generate_password_hash("test").decode('UTF-8')
username = "brandon"
new_user = Admin(username=username,password=password)
db.session.add(new_user)
db.session.commit()


