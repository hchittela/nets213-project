# CCB - Crowdsourced Comparative Branding
http://nets213ccb.herokuapp.com

##Overview
We've utilized Flask with a MySQL database to make this project a reality. Web hosting is done via Heroku. Creating an entire website obviously means there are a lot of different parts; in this README we will go over the main code for this project. 

##Files
**app.py**:
This file has most of the backend logic for our app. Starting from the top and working our way down the file: We utilized the SQLAlchemy framework within Flask to handle the database transactions. We then define and create the database models to match up exactly with the database tables we have created in MySQL. The _Challenges_ table represents an upload by a designer - or a 'challenge' between two designs to see which is better. The _User_ table is what our login/signup system is built on, and holds name, email, and password information (hashed, of course). After a few helper functions, around mid-way through the file and down are our app routes. These define what pages load when specific URL endpoints are hit. They also further hold all our logic for form validation (e.g. making sure users don't leave a field empty). 

**config.py**:
This file is smaller - it essentially sets a few essential features and connects us to our database. 

**templates folder**:
This folder contains all of our HTML code. We utilized python's templating: our main templates are nav_layout.html and bg_layout.html. bg_layout is the main page - it contains the template with the navigation bar of "Upload", "Responses", and "Log out" at the top. nav_layout is the template for the login and signup pages. As you can see, we used bootstrap as our main source of styling for this project. index.html is the first page you hit when you go to the URL above, and is the login page. The rest of the pages extend their respective template and are named according to their function. 

**static folder**: This folder contains all of our CSS and images. As mentioned, we mainly used bootstrap for our styling, but also used a little custom CSS. 

**src folder**: This folder contains all the python code that's used for CrowdFlower. job_create_upload extracts a CSV from our database, uploads it to CrowdFlower, and creates the job automatically based on how many responses the designer wanted. qc1input_to_qc1output takes the output from this initial job (the job in which workers vote and comment on a design), and filters out all of the people who answered the GOLD question incorrectly. The GOLD question is an obvious answer that we have put in to act as a quality control measure. qc1input_to_qc2input takes the output from the initial job and turns it into input for the second CrowdFlower task, which we have designed as a secondary quality control measure. This task takes all of the comments for a design and aggregates them into a new task, in which workers rate each comment on its usefulness relative to the design on a scale of 1-5. We then provide the top rated comments to the designer. Finally, aggregation takes the output from both tasks and puts them into a readable CSV file. We then provide this data back to the designer (under the "Responses" page in the navigation bar). 

##Old README
##Customer Submission (4)
**Idea**: Customers who wish to use our app will submit to us two separate versions of a design that they want feedback on. This can be screenshots of an app, color variations of a logo, different menu layouts for a website, etc. They will also specify at this time how many reviews they want on their mockups (100, 250, or 500).

**Milestones**: We will need to build a web app where customers can upload images and specify the number of reviews they want. Each customer will have a user account so that they can log back in and view the progress of their submission and the final results.


##CrowdFlower Task Creation (3)
**Idea**: We will create a CF task containing submissions from multiple customers. The data we receive from the customer submission on our web app will need to be formatted into an appropriate csv with urls to the customer’s mockups hosted by us. An important note is that since we cannot specify the number of workers to complete a given ‘row’ individually per row, we will be creating separate tasks for each tier (100 reviews, 250 reviews, and 500 reviews).

**Milestones**: Ensuring proper formatting of the csv with image uploads. Finding an efficient method of creating tasks and determining how often new tasks should be created since we can’t dynamically add rows to a task’s csv.

##Quality Control (3)
**Idea**: Three main features of the module. 

1) We will be mixing in random gold standard tasks into our csv that we create. For these, one mockup will be clearly better than the other so that it is obvious when a worker is clicking randomly and chooses the poorer mockup in our gold standard.
2) Workers will be required to submit a comment detailing why they chose one mockup over the other. This will serve as a quality control measure since it will at the very least make workers stop and think. 
3) To determine whether the comments are useful, and to provide the most useful comments back to the designer, we will create a new task which has images with the previously submitted comments. Workers will be required to rate how relevant and helpful each comment is on a scale of 1-5, and 0 if it is gibberish or makes no sense. 

**Milestones**: Creating gold standard tasks. Writing script to identify if a comment is garbage or comprehensible.

##Aggregation (4)
**Idea**: Worker submissions will be tallied to obtain a count of which mockup is favored for a given designer’s task. We will also run analysis to identify how much ‘better’ one mockup is compared to the other. Finally, we will analyze the comments to provide a word cloud to the customer that shows which words were most common in the comments. Hopefully this will hint at what factors were important to workers in making a decision.

**Milestones**: Script to identify most common words that are not generic English words like “this”, “a”, “it”, etc. Script to obtain analysis of quantitative measures of mockup favorability.

##Final Customer Result (2)
**Idea**: Customers will log into their account on our website to see the final aggregate results. This will include the data/counts mentioned above and the word cloud.

**Milestones**: We will need to be able to provide information to the customer on our website based on the csv data we download from our CF task. This will be a challenge in formatting and parsing.
