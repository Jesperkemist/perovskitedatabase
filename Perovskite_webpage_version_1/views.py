"""
Routes and views for the flask application.
"""
import os

from datetime import datetime
from flask import flash, redirect, render_template, request, send_file,  url_for
#from Perovskite_webpage_version_1 import app

def init_app(app):

    @app.route('/')
    @app.route('/home')
    def home():
        """Renders the home page."""
        return render_template('home.html')

    @app.route('/Interactive_graphics')
    def Interactive_graphics():
        """Renders the home page."""
        return render_template('Interactive_graphics.html')

    @app.route('/Resources')
    def Resources():
        """Renders the home page."""
        return render_template('Resources.html')

    @app.route('/Download')
    def Download():
        """Renders the home page."""
        return render_template('Download.html')

    @app.route('/Upload')
    def Upload():
        """Renders the home page."""
        return render_template('Upload.html')

    @app.route('/Contributors')
    def Contributors():
        """Renders the home page."""
        return render_template('Contributors.html')

    @app.route('/Funding')
    def Funding():
        """Renders the home page."""
        return render_template('Funding.html')

    @app.route('/How_to_cite')
    def How_to_cite():
        """Renders the home page."""
        return render_template('How_to_cite.html')

    @app.route('/Contact')
    def Contact():
        """Renders the home page."""
        return render_template('Contact.html')

    @app.route('/Papers')
    def Papers():
        """Renders the home page."""
        return render_template('Papers.html')

    @app.route('/Presentations')
    def Presentations():
        """Renders the home page."""
        return render_template('Presentations.html')

    #%% Download files
    @app.route('/return_extractionProtocol')
    def return_extractionProtocol():

        print(f'os.getcwd(): {os.getcwd()}')

        fileName = 'Extraction protocolls version 5_4.xlsx'
        filePath = os.path.join(os.path.abspath(os.getcwd()), 'Perovskite_webpage_version_1', 'static', 'files', fileName)

        try:
            return send_file(filePath, as_attachment = True, attachment_filename=fileName)
        except Exception as e:
            return str(e)

    @app.route('/return_extractionInstructions')
    def return_extractionInstructions():

        print(f'os.getcwd(): {os.getcwd()}')

        fileName = 'The perovskite database instructions for entering data version 5.4.pdf'
        filePath = os.path.join(os.path.abspath(os.getcwd()), 'Perovskite_webpage_version_1', 'static', 'files', fileName)

        try:
            return send_file(filePath, as_attachment = True, attachment_filename=fileName)
        except Exception as e:
            return str(e)

    @app.route('/return_databaseInstructions')
    def return_databaseInstructions():

        print(f'os.getcwd(): {os.getcwd()}')

        fileName = 'The perovskite database description of data content 5.4.pdf'
        filePath = os.path.join(os.path.abspath(os.getcwd()), 'Perovskite_webpage_version_1', 'static', 'files', fileName)

        try:
            return send_file(filePath, as_attachment = True, attachment_filename=fileName)
        except Exception as e:
            return str(e)

    @app.route('/healthz')
    def healthz():
        return {"Status": "OK"}, 200
