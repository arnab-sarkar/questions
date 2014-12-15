from google.appengine.ext import ndb

class Post(ndb.Model):
	userId = ndb.UserProperty()
	createdDate = ndb.DateTimeProperty( auto_now_add = True )
	modifiedDate = ndb.DateTimeProperty( auto_now = True )
	title = ndb.StringProperty()
	body = ndb.TextProperty()
	tags = ndb.StringProperty( repeated = True )
	parentId = ndb.KeyProperty()
	voteCount = ndb.IntegerProperty()

class Vote(ndb.Model):
	userId = ndb.UserProperty()
	postId = ndb.KeyProperty()
	vote = ndb.BooleanProperty()

class Tags(ndb.Model):
	name = ndb.StringProperty()
	posts = ndb.KeyProperty( repeated = True )

