import webapp2
from controller.home import MainPage
from controller.home import AddQuestion
from controller.home import DisplaySameTagQuestion
from controller.home import ViewQuestion
from controller.home import UpdateQuestion
from controller.home import AddAnswer
from controller.home import VotePost

app = webapp2.WSGIApplication([
    ('/addAnswer',AddAnswer),
    ('/updateQuestion',UpdateQuestion),
    ('/viewQuestion',ViewQuestion),
    ('/vote',VotePost),
    ('/tag',DisplaySameTagQuestion),
    ('/question',AddQuestion),
    ('/', MainPage),
], debug=True)