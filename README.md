# SolutionChallenge2021-LearningTeaching
Github repository for the code of our submission

This is a Flask application developed for the Google solution challenge 2021 (submission March 31). 
We use Firebase as a database.

To run the code, please follow the instructions below:

- Clone our project: to do this, open a Git CMD console and navigate to the desired location "cd path_to_location". Then clone our project with the command "git clone url_of_project" (the url of the project is available on the repository page (green button "Code"). 
- From a classic command console or via your favorite python IDE (Pycharm for example), place yourself inside the created folder named SolutionChallenge2021-LearningTeaching. 
- Start your virtual environment (to create a new one, under Anaconda for example, use the command "conda create -n myenv python=3.7 anaconda" and launch it with "conda activate myenv"
- Install the dependencies of our project in this environment : "pip install -r requirements.txt"
- Enter the following command in the same console: "set FLASK_APP=app.py" 
- Run the code with the command "flask run". 
- An url is displayed in console, click on it to get to our web application