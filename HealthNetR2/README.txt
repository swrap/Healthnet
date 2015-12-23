Welcome to Healthnet. This contains all of the files necessary for running the program.

How to Run (on Windows):	
	-Prequirements
		-make sure python 3.4.3 is downloaded and installed
		-make sure django 1.8.3 is downloaded and installed
		-the application should be run off of a local drive NOT OFF THE SERVER
	-Automatic Launch
		-Double click on "Runserver and Launch in Browser.bat" file
		-this should run the server and open a browser windows
		-this should display a login page
	-Manual Launch
		-launch cmd
		-cd into "HealthNetR2" directory
		-type the following command into cmd "python manage.py runserver"
		-open a web browser and type "http://localhost:8000/healthnet/" into the url bar

How to Run Tests (on Windows)
	-Manual Run
		-launch cmd
		-cd into "HealthNetBeta" directory
		-type the following command into cmd "python manage.py test"

Prepopulated Information (all accounts can be accessed by logging in through the index page of healthnet)
	-Administrator Account
		-username = admin
		-password = admin
	-Patient Account (some patients already have appointments scheduled)
		-anthony			
			-username = anthony
			-password = anthony
		-ben
			-username = ben
			-password = ben
		-edward
			-username = edward
			-password = edward
	-Doctor Account
		-jerry
			-username = jerry
			-password = jerry
		-kyle
			-username = kyle
			-password = kyle
	-Nurse Account
		-joy
			-username = joy
			-password = joy

Problem areas or functinal deficiencies
	-Some fields if left blank with the dropdown may throw error
		-reason behind is the checking requires the cleaned_data for that form
		-most of these have been resolved, but some may be lingering
		-how to fix is go back and select a value
	-Everything else should work smoothly

Developer Contact Information
Jesse Saran (main developer)
Louis Trapani (css + html)
Aaron Lui (co developer)
Dylan Bowald (testing)
Ian London (bits and pieces)