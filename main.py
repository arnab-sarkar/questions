import webapp2
from controller.home import MainPage
from controller.home import AddQuestion
from controller.home import DisplaySameTagQuestion
from controller.home import ViewQuestion
from controller.home import AddAnswer

app = webapp2.WSGIApplication([
    ('/addAnswer',AddAnswer),
    ('/viewQuestion',ViewQuestion),
    ('/tag',DisplaySameTagQuestion),
    ('/question',AddQuestion),
    ('/', MainPage),
], debug=True)