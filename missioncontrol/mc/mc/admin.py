from flask_admin import BaseView, expose
from wtforms import TextAreaField, TextField, IntegerField, FloatField, SelectField, PasswordField
from wtforms import validators
from flask_wtf import Form
from flask import request, redirect, url_for, flash, session
from init_db import reset

class Reset(BaseView):
    def is_accessible(self):
        if 'logged_in' in session.keys():
            return True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

    @expose('/', methods=('GET', 'POST'))
    def reset(self):
        if request.method == 'POST':
            if request.form.has_key('reset'):
                flash("reset all data")
                reset()
            if request.form.has_key('shutdown'):
                flash("shutting down")
        return self.render('admin/reset.html')
