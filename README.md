This repo contains both the RESTful API and the Frontend mockup exercise.

## Steps to getting the app going

### First, clone the repo

### Then:

`cd caredash`

`python -m venv env`

`. env/bin/activate`

`pip install -r requirements.txt`

### Open a python shell, then:

`from project import db`

`db.create_all()`

### Close the shell, then:

`flask run`

At this point you can navigate to localhost:5000 to view the frontend exercise or running curl commands to hit the API endpoints.

Thanks for this challenge! It was a lot of fun to work through; especially the API component.

If I had more time:
* I would continue to polish the frontend styles ensuring consistency with whitespace and copy widths across more potential device widths
* Add smooth transitions for header dropdowns
* Add hover interactions for links and buttons
* Add floating label interactions for form
* Further split the html into partials
* Break the __init__.py file down into _config, db, models, views, and run files. I would also use the blueprint pattern for the api to help keep the codebase organized
* Add more catch statements to account for incorrect requests
* Figure out how to have the full review object return with the doctor object and vice-versa. I think it would be worthwhile to explore Flask-RESTful and Flask-Migrate