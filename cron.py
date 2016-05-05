import app

has_credit = False

if has_credit:
	# Create a CF Task for Task 1 if we have more than 10 new uploads
	app.create_crowdflower_task1()

	# If we have new comments from the Task 1, add them to the DB and create a second CrowdFlower QC task on the comments
	if app.get_crowdflower_results_task1():
		app.create_crowdflower_task2()

	# If we have new scores from the Task 2, add them to the DB
	app.get_crowdflower_results_task2()
else:
	print "No credit available in the CrowdFlower account."