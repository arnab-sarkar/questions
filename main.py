import webapp2
from controller.home import MainPage
from controller.home import AddQuestion
from controller.home import DisplaySameTagQuestion

app = webapp2.WSGIApplication([
    ('/tag',DisplaySameTagQuestion),
    ('/question',AddQuestion),
    ('/', MainPage),
], debug=True)