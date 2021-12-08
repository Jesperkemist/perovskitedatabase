The Perovskite Database Project

In the top directory there are two master files

1. bokehServerRun.py
  That one starts a Bokeh server runing the interactive apps defines in the dashboards directory

  To use this script, you must create a file called `.env` in your root directory that will contain the database connection details (this file is git ignored), copy the following lines into this file, and replace the place holders with the connection details of the database:

  ```bash
  DB_HOST=<host ip>
  DB_DATABASE=<database name>
  DB_USERNAME=<user name>
  DB_PASSWORD=<password>
  ```

2. runserver.py
  Runs a Flask application that runs the webpage defined in the Perovskite_webpage_version_1 directory 

