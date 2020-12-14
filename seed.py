from app import app
from models import db, Category, Subcategory, Admin, Trade, Issue, Issue_Parts, Part
from flask_bcrypt import Bcrypt

db.drop_all()
db.create_all()

category = Category(name="Plumbing")
category1 = Category(name="Auto")
category2 = Category(name="Appliances")
category3 = Category(name="Electrical")
category4 = Category(name="Carpentry")
db.session.add_all([category, category1,category2,category3,category4])
db.session.commit()

subcategory = Subcategory(category_id=category.id, name="Toilets")
subcategory1 = Subcategory(category_id=category1.id, name="Engines")
trade = Trade(category_id=category.id, name="Plumber", cost_per_hour=12)
trade1 = Trade(category_id=category1.id, name="Mechanic", cost_per_hour=24)
trade2 = Trade(category_id=category2.id, name="Appliance Expert", cost_per_hour=10)
trade3 = Trade(category_id=category3.id, name="Electrician", cost_per_hour=10)
trade4 = Trade(category_id=category4.id, name="Carpenter", cost_per_hour=10)
part = Part(name="Hammer", link="https://www.walmart.com/ip/Hyper-Tough-16-Ounce-Claw-Hammer-with-Fiberglass-Handle/972830002", 
image_url="https://i5.walmartimages.com/asr/61b5ab99-2d90-45fe-9952-0932abf84c05_1.e755cf112171a90e30833bd8429a2bad.jpeg?odnWidth=100&odnHeight=100&odnBg=ffffff", price=14)
part1 = Part(name="Wrench", link="https://www.walmart.com/ip/8-inch-Adjustable-Wrench-with-Sure-Grip-Handle-UW00015A/17190620", image_url="https://i5.walmartimages.com/asr/959de1ff-d6a9-4876-9256-2b01e2756462_2.9cdc010d9e8ddfc3c1ca7e7a72f7fcb7.jpeg?odnWidth=100&odnHeight=100&odnBg=ffffff", price=4)
db.session.add_all([subcategory, subcategory1, trade, trade1, trade2, trade3, trade4, part, part1])
db.session.commit()

issue = Issue(name="Running Toilet", subcategory_id=subcategory.id,
              video_url="https://www.youtube.com/embed/DoqzGyC92GQ", num_hours=1, difficulty="easy")
db.session.add(issue)
db.session.commit()

issue_part = Issue_Parts(issue_id=issue.id, part_id=part.id, num_needed=2)
issue_part1 = Issue_Parts(issue_id=issue.id, part_id=part1.id, num_needed=2)
db.session.add_all([issue_part, issue_part1])
db.session.commit()

bcrypt = Bcrypt()
password = bcrypt.generate_password_hash("test").decode('UTF-8')
username = "brandon"
new_user = Admin(username=username,password=password)
db.session.add(new_user)
db.session.commit()


