import webapp2
from controller.home import MainPage
from controller.home import AddQuestion

app = webapp2.WSGIApplication([
    ('/question',AddQuestion),
    ('/', MainPage),
], debug=True)