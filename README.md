# ifixedit
Official site: ifixedit.heroku.app

Website purpose: Will help users complete projects and repairs without having to pay for expensive specialists. Also, users can find links to purchase the items needed for the repair online.

Capstone Project Idea - Repair Website

API Link: http://api-doc.axesso.de/

Current features:

1. Search function - users may not know the specific category or want to search by sepcific category
2. Repair page
    a. Video walkthrough - i believe it is easier to follow along with a video you can pause and            rewind, than to read a manual
    b. Items Needed - contains image, # needed, price, and link to where part can be purchased. If          you don't already have the parts, you don't want to then go search for them. The repair is            enough work.
    c. Details - hours needed to complete and how much a specialist would have charged, so users can        know they are saving money.
3. Admin section - allows admins to add into database directly from website. For insertion into databases while online. This will be especially useful while following along on videos instead of having to operate in multiple systems.
4. Quick add links - allows admins to add into database by just sending get request. For fastest possible changes.

Upcoming Features:

Alphabetized categories,
Full parts catalog,
Tags to improve search functionality,
Edit and delete functionality for admins,
Top 100 most common diy repairs,
If fix/issue is not an issue user will be redirected to search results,
Finding repair by sound


User Flows:

1. Search - user can type in what they are trying to fix. If a direct match user will be taken to repair page, if not user will see search results for their query.
2. /fix/issue - user can type in repair with dashes, replacing spaces to go directly to page. 
3. Category - found on the banner of every page, user can click a category, then subcategory, then specific repair needed.

Tech Stack:

Python - flask, flask_bcrypt, wtforms, flask_wtf (requirements.txt file included)
Javascript
HTML
CSS
Heroku
Postgres
