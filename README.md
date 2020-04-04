# FlaskUnityHeroku
Repo for the web app made in flask that takes Unity WebGL build folders' zip files and runs the game


This was deployed on Heroku but it doesn't work cuz Heroku doesn't allow files to be uploaded to their apps so if u bois and grils wanna try it out clone this repo and install the dependencies to run the wsgi.py on localhost.

The Pipfile contains the names of the packages u need to install to run the app (The packages u need to install are flask and flask_bcrypt. gunicorn is just for deploying the app to a Heroku server)

The zip files included in the repo aren't to be extracted by u but to be uploaded on the web app for testing 
