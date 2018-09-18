# [START imports]
import re
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import db

import jinja2
import webapp2

templates_dir =os.path.join(os.path.dirname(__file__), "templates") # """Directory of all templates"""
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(templates_dir),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)
# [END imports]


# [START handler class]
class Handler(webapp2.RequestHandler):
    """The Handler Class"""
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = JINJA_ENVIRONMENT.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

# [START main_page]
class MainPage(Handler):
    """The Home Page Handler."""
    def get(self):
        self.render("home.html")

# [START admission database]
class AdmissionData(db.Model):
    """Database for AdmissionData."""
    applicants_name = db.StringProperty(required = True)
    fathers_email = db.EmailProperty(required = True)
    fathers_phone = db.StringProperty(required = True)
    mothers_email = db.EmailProperty(required = True)
    mothers_phone = db.StringProperty(required = True)
    home_address = db.TextProperty(required = True)
    application_date = db.DateTimeProperty(auto_now_add = True)

# [START admission_page]
class AdmissionPage(Handler):
    """The Admission Page RequestHandler."""
    def get(self):
        self.render("admission.html")

    def post(self):
        applicants_name = self.request.get("applicants_name")
        fathers_phone = self.request.get("fathers_phone")
        fathers_email = self.request.get("fathers_email")
        mothers_phone = self.request.get("mothers_phone")
        mothers_email = self.request.get("mothers_email")
        home_address = self.request.get("home_address")

        applicant = AdmissionData(applicants_name=applicants_name, fathers_email=fathers_email, fathers_phone=fathers_phone, mothers_email=mothers_email, mothers_phone=mothers_phone, home_address=home_address)
        applicant.put()
        self.redirect("/submitted")

# [START admission_submitted]
class AdmissionSubmitted(Handler):
    """for handling admission submittion redirect."""
    def get(self):
        self.render("admission_submitted.html")

# [START career database]
class CareerData(db.Model):
    """Database for Career Data."""
    career_name = db.StringProperty(required = True)
    career_email = db.EmailProperty(required = True)
    career_phone = db.StringProperty(required = True)
    career_address = db.TextProperty(required = True)
    application_date = db.DateTimeProperty(auto_now_add = True)

# [START career]
class Career(Handler):
    """The Admission Page RequestHandler."""
    def get(self):
        self.render("career.html")

    def post(self):
        career_name = self.request.get("career_name")
        career_email = self.request.get("career_email")
        career_phone = self.request.get("career_phone")
        career_address = self.request.get("career_address")

        careerant = CareerData(career_name=career_name, career_email=career_email, career_phone=career_phone,  career_address=career_address)
        careerant.put()
        self.redirect("/submitted")

# [START app]
app = webapp2.WSGIApplication([
    ("/", MainPage),

    ('/career', Career),

    ('/admission', AdmissionPage),

    ("/submitted", AdmissionSubmitted),
])
# [END app]
