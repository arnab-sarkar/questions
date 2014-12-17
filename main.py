import webapp2
from controller.home import MainPage
from controller.home import AddQuestion
from controller.home import DisplaySameTagQuestion
from controller.home import ViewQuestion
from controller.home import UpdateQuestion
from controller.home import UpdateAnswer
from controller.home import AddAnswer
from controller.home import VotePost
from controller.home import PostDescription
from controller.home import UploadImage
from controller.home import UploadImagePage
from controller.home import ImageServeHandler
from controller.home import Search

app = webapp2.WSGIApplication([
    ('/addAnswer',AddAnswer),
    ('/imagePage',UploadImagePage),
    ('/updateQuestion',UpdateQuestion),
    ('/postDescription',PostDescription),
    ('/updateAnswer',UpdateAnswer),
    ('/upload',UploadImage),
    ('/viewQuestion',ViewQuestion),
    ('/vote',VotePost),
    ('/tag',DisplaySameTagQuestion),
    ('/question',AddQuestion),
    ('/serveImage/([^/]+)?', ImageServeHandler),
    ('/search',Search),
    ('/', MainPage),
], debug=True)