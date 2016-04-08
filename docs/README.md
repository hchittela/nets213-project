# CCB - Crowdsourced Comparative Branding

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
