from flask import Flask, render_template, make_response, request, redirect, url_for
from flask_bootstrap import Bootstrap
from app import app
from .forms import ChangePassForm, ConfigThrowForm
from .miko import dochangepass, doconfthrow

Bootstrap(app)


@app.route('/')
def home():
    return render_template('index.html',
                           title='Home',
                           strapline='Choose a tool to begin...')


@app.route('/new')
def tbc():

    #Placeholder page

    return render_template('index.html',
                           title='Coming Soon',
                           strapline='Coming Soon...')


@app.route('/changepass', methods=['GET', 'POST'])
def changepass():
    form = ChangePassForm()
    form_desc = "This changes the user password (of the user entered) and enable password on all devices (in devices.txt)"

    if form.validate_on_submit():
        #accepted = request.form.get('confirm') # accepted = "y" if ticked, None if unticked
        user = request.form['username']
        oldPass = request.form['user_pass']
        newPass = request.form['new_user_pass']
        oldENPass = request.form['enable_pass']
        newENPass = request.form['new_enable_pass']

        dochangepass(user, oldPass, newPass, oldENPass, newENPass)

        return render_template('index.html',
                                   title='Home',
                                   strapline='The form submitted OK with user: ' + user)

    return render_template('formpage.html',
                           title='ChangePass',
                           strapline='Password Changer App',
                           form=form,
                           form_desc=form_desc,
                           len=5, devfile="FAKE ENTRIES")


@app.route('/config', methods=['GET', 'POST'])
def config():
    form = ConfigThrowForm(csrf_enabled=False)
    form_desc = "This pushes out commands (from commands.txt) to devices (in devices.txt)"

    if form.validate_on_submit():
        user = request.form['username']
        user_pass = request.form['user_pass']
        enPass = request.form['enable_pass']
        confmode = request.form['config_mode']

        doconfthrow(user, user_pass, enPass, confmode)

        return render_template('index.html',
                                   title='Home',
                                   strapline='The form submitted OK with user: ' + user + ' & Config mode: ' + confmode)

    return render_template('formpage.html',
                           title='ConfigThrow',
                           strapline='Configuration Thrower App',
                           form=form,
                           form_desc=form_desc)

"""
@app.route('/changepass2', methods=['GET', 'POST'], defaults={'app': "changepass"})
@app.route('/config2', methods=['GET', 'POST'], defaults={'app': "config"})
def formpage(app):
    if app == "changepass":
        form = ChangePassForm()
        form_desc = "This changes the user password (of the user entered) and enable password on all devices (in devices.txt)"
        title = 'ChangePass'
        strapline = 'Password Changer App'
    elif app == "config":
        form = ConfigThrowForm()
        form_desc = "This pushes out commands (from commands.txt) to devices (in devices.txt)"
        title = 'ConfigThrow'
        strapline = 'Configuration Thrower App'

    if form.validate_on_submit():
        namey = request.form['username']
        
        if app == "config":
            mode = request.form['config_mode']
            return render_template('index.html',
                                       title='Home',
                                       strapline='The form submitted OK with user: ' + namey + ' & Config mode: ' + mode)

        return render_template('index.html',
                                   title='Home',
                                   strapline='The form submitted OK with user: ' + namey)

    return render_template('formpage.html',
                           title=title,
                           strapline=strapline,
                           form=form,
                           form_desc=form_desc)
"""

@app.route('/devices', methods=['GET', 'POST'], defaults={'dname': "devices"})
@app.route('/commands', methods=['GET', 'POST'], defaults={'dname': "commands"})
def editfiles(dname):
    import os
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))  # refers to application_top
    confile_path = os.path.join(APP_ROOT, dname + '.txt')

    def file_len(file):
        with file:
            for i, l in enumerate(file):
                pass
        return i + 1

    def try_file(file):
        try:
            open(file)
        except:
            return False
        return True

    if try_file(confile_path):
        length = file_len(open(confile_path)) + 5
        confile = open(confile_path).read()
    else:
        length = 2
        confile = "Error reading file:\nNo file '" + dname + ".txt" + "' found!"

    # Used by button presses (Download/Save):
    if request.method == 'POST':
        if request.form['do'] == "download":
            response = make_response(confile)
            # Downloads the txt file to the client from the browser:
            response.headers["Content-Disposition"] =\
                "attachment; filename=%s.txt" % dname
            return response
        elif request.form['do'] == "save":
            # Gets text from the HTML textarea named 'config':
            data = request.form.get('config')

            # Writes the text to the config file and reloads page with updated file:
            file = open(confile_path, 'w', newline="\n")
            file.write(data)
            file.close()
        return render_template('editfiles.html', confile=data, len=length, dname=dname, title=dname)

    return render_template('editfiles.html', confile=confile, len=length, dname=dname, title=dname)


# Error page routes
@app.errorhandler(404)  # page not found (incorrect URL)
@app.errorhandler(405)  # method not allowed (no PUT etc.)
@app.errorhandler(500)  # internal server error (code/server error)
def http_error(e):
    return render_template('error.html',
                           title=e,
                           err_message=e), e.code
