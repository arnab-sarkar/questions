import webapp2
from google.appengine.api import users
from google.appengine.ext.webapp import template
from model.model import Post
from model.model import Tags
from model.model import Vote
import time
import os

def template_path(template):
    path = os.path.join(os.path.dirname(__file__), '../templates/' + template)
    return path

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template_values = {
            'title': 'Questions'
        }
        if user:
            template_values['user'] = user
            template_values['userLogout'] = users.create_logout_url('/') 
        else:
            template_values['userLogin'] = users.create_login_url('/')
        path = template_path('home.html')
        time.sleep(0.1)
        question = Post.query(Post.parentId==None).fetch()
        template_values['question'] = question
        self.response.out.write(template.render(path, template_values))

class DisplaySameTagQuestion(webapp2.RequestHandler):
    def get(self):
        tag = self.request.get("tag")
        user = users.get_current_user()
        tag_object = Tags.query(Tags.name==tag).fetch()
        questionList=[]
        for postId in tag_object[0].posts:
            questionList.append(postId.get())
        template_values = {
            'title': 'Questions'
        }
        if user:
            template_values['user'] = user
            template_values['userLogout'] = users.create_logout_url('/')
        else:
            template_values['userLogin'] = users.create_login_url('/')
        template_values['question']=questionList
        path = template_path('home.html')
        self.response.out.write(template.render(path, template_values))

class AddQuestion(webapp2.RequestHandler):
    def post(self):
        question = self.request.get("question")
        tags = self.request.get("tags")
        tags_array = filter(None,tags.split(","))
        post = Post()        
        post.userId = users.get_current_user()
        post.title = question
        post.tags = tags_array
        post.parentId = None
        post.voteCount = 0
        question_post_id = post.put()
        for t in tags_array:
            tag = Tags.query(Tags.name==t).fetch()
            if (len(tag) == 0):
                tag = Tags()
                tag.name = t
                tag.posts = [question_post_id]
                tag.put()
            else:
                tag[0].posts.append(question_post_id)
                tag[0].put()        
        self.redirect('/')

class ViewQuestion(webapp2.RequestHandler):
    def get(self):
        qId = self.request.get("q")
        user = users.get_current_user()
        question = Post.get_by_id(int(qId))
        answers = Post.query(Post.parentId==question.key).fetch()
        template_values = {
            'question': question,
            'answers': answers
        }
        if user:
            template_values['user'] = user
            template_values['userLogout'] = users.create_logout_url('/')
        else:
            template_values['userLogin'] = users.create_login_url('/')
        path = template_path('question.html')        
        self.response.out.write(template.render(path, template_values))

class AddAnswer(webapp2.RequestHandler):
    def post(self):
        answer = self.request.get("a")        
        qId = self.request.get("q")
        question = Post.get_by_id(int(qId))
        post = Post()        
        post.userId = users.get_current_user()
        post.body = answer        
        post.parentId = question.key
        post.voteCount = 0
        post.put()
        time.sleep(0.1)
        self.redirect('/viewQuestion?q='+qId)

class VotePost(webapp2.RequestHandler):
    def post(self):
        postId = self.request.get("id")
        vote = self.request.get("vote")
        url = self.request.get("url")
        user = users.get_current_user()
        post = Post.get_by_id(int(postId))
        existing_vote = Vote.query(Vote.userId==user,Vote.postId==post.key).fetch()
        if (len(existing_vote) == 0):
            v = Vote()
            v.userId = user
            v.postId = post.key
            v.vote = bool(vote)
            if (bool(vote)):
                post.voteCount = post.voteCount + 1
            else:
                post.voteCount = post.voteCount - 1
            post.put()
            v.put()
        else:
            if existing_vote[0].vote != bool(vote):
                existing_vote[0].vote = bool(vote)
                if (bool(vote)):
                    post.voteCount = post.voteCount + 2
                else:
                    post.voteCount = post.voteCount - 2
                post.put()
                existing_vote[0].put()        
        time.sleep(0.1)
        self.redirect(str(url))