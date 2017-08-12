from flask.ext.wtf import Form
from wtforms import (StringField, BooleanField, SubmitField,
                     PasswordField, SelectField)
from wtforms.validators import DataRequired, EqualTo


class ChangePassForm(Form):

    username = StringField('Username:',
                           validators=[DataRequired()],
                           description="Enter the current priv 15 username")
    user_pass = PasswordField('User Password:',
                              validators=[DataRequired()],
                              description="Enter the current password for this user")

    new_user_pass = PasswordField('NEW User Password:',
                                  validators=[DataRequired(),
                                              EqualTo('cnew_user_pass',
                                                      message='Passwords must match')],
                                  description="Enter the NEW password for this user")
    cnew_user_pass = PasswordField('Confirm NEW User Password:',
                                   validators=[DataRequired()],
                                   description="Enter the NEW password for this user, again")

    enable_pass = PasswordField('Enable Password:',
                                validators=[DataRequired()],
                                description="Enter the current enable password")

    new_enable_pass = PasswordField('NEW Enable Password:',
                                    validators=[DataRequired(),
                                                EqualTo('cnew_enable_pass', message='Passwords must match')],
                                    description="Enter the NEW password for this user")
    cnew_enable_pass = PasswordField('Confirm NEW Enable Password:',
                                     validators=[DataRequired()],
                                     description="Enter the NEW enable password, again")

    confirm = BooleanField("Are you sure? THIS USES devices.txt SO ENSURE THIS IS CORRECT BEFORE SUBMITTING",
                           validators=[DataRequired(message="You must accept")])

    submit = SubmitField('Submit')


class ConfigThrowForm(Form):

    username = StringField('Username:',
                           validators=[DataRequired()],
                           description="Enter the current priv 15 username")
    user_pass = PasswordField('User Password:',
                              validators=[DataRequired()],
                              description="Enter the current password for this user")

    config_mode = SelectField('Configuration Mode:',
                              choices=[('user', 'User (non-enabled commands)'),
                                       ('conf', 'Config (conf t commands)')],
                              description="Select the type of commands in commands.txt")

    enable_pass = PasswordField('Enable Password:',
                                validators=[DataRequired()],
                                description="Enter the current enable password")

    confirm = BooleanField("Are you sure? THIS USES devices.txt AND commands.txt SO ENSURE THESE ARE CORRECT BEFORE SUBMITTING",
                           validators=[DataRequired(message="You must accept")])

    submit = SubmitField('Submit')
