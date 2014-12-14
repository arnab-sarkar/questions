import webapp2
from google.appengine.api import users
from google.appengine.ext.webapp import template
from model.model import Post
from model.model import Tags
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
        question = Post.query(ancestor=None).fetch()
        template_values['question'] = question
        self.response.out.write(template.render(path, template_values))

class DisplaySameTagQuestion(webapp2.RequestHandler):
    def post(self):
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
        template_values = {
            'question': question
        }
        if user:
            template_values['user'] = user
            template_values['userLogout'] = users.create_logout_url('/')
        else:
            template_values['userLogin'] = users.create_login_url('/')
        path = template_path('question.html')        
        self.response.out.write(template.render(path, template_values))