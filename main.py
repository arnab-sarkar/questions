import webapp2
from controller.home import MainPage
from controller.home import AddQuestion
from controller.home import DisplaySameTagQuestion
from controller.home import ViewQuestion

app = webapp2.WSGIApplication([
    ('/viewQuestion',ViewQuestion),
    ('/tag',DisplaySameTagQuestion),
    ('/question',AddQuestion),
    ('/', MainPage),
], debug=True)