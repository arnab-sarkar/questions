import webapp2
from controller.home import MainPage

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)