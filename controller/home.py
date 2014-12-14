import webapp2
from google.appengine.api import users
from google.appengine.ext.webapp import template
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
        time.sleep(1)
        question = Post.query(ancestor=None).fetch()
        template_values['question'] = question
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
        post.put()
        self.redirect('/')