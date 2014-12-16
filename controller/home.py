import webapp2
from google.appengine.api import users
from google.appengine.ext.webapp import template
#from google.appengine.datastore.datastore_query import Cursor
from model.model import Post
from model.model import Tags
from model.model import Vote
import time
import os
import re

def template_path(template):
    path = os.path.join(os.path.dirname(__file__), '../templates/' + template)
    return path

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        #pageNum = self.request.get("pageNum")
        #curs = None
        #if pageNum == "" :
        #    pageNum = 1
        #else :
        #    curs = Cursor(self.request.get('cursor'))  
        template_values = {}      
        if user:
            template_values['user'] = user
            template_values['userLogout'] = users.create_logout_url('/') 
        else:
            template_values['userLogin'] = users.create_login_url('/')
        path = template_path('home.html')        
        #question, next_curs, more = Post.query(Post.parentId==None).order(-Post.modifiedDate).fetch_page(10, start_cursor=curs)
        question = Post.query(Post.parentId==None).order(-Post.modifiedDate).fetch()
        #template_values['cursor'] = next_curs
        #template_values['more'] = more
        displayQuestions = []   
        for q in question:
            title = q.title
            if len(title) > 500:
                q.title = title[0:499] + "..."
                displayQuestions.append((q, False))
            else:
                body = q.body
                remaining_len = 500 - len(title)
                if body != None and len(body) > remaining_len:
                    q.body = body[0:remaining_len-1] + "..."
                displayQuestions.append((q, True))
            #q.title = re.sub("(https?[^ ]*.jpg)", r"<div class='image'><img src='\1' /></div>", q.title, flags=re.DOTALL)            
        template_values['question'] = displayQuestions
        time.sleep(0.1)
        template_render = template.render(path, template_values)
        template_render = re.sub("(https?[^ ]*.((jpg)|(png)|(gif)))", r"<div><img src='\1' class='image_display' /></div>", template_render, flags=re.DOTALL)
        #print template.render(path, template_values)
        self.response.out.write(template_render)

class DisplaySameTagQuestion(webapp2.RequestHandler):
    def get(self):
        tag = self.request.get("tag")
        user = users.get_current_user()
        tag_object = Tags.query(Tags.name==tag).fetch()
        questionList=[]
        for postId in tag_object[0].posts:
            questionList.append(postId.get())
        pageNum = self.request.get("pageNum")
        if pageNum == "" :
            pageNum = 1
        template_values = {
            'pageNum': pageNum
        }
        if user:
            template_values['user'] = user
            template_values['userLogout'] = users.create_logout_url('/')
        else:
            template_values['userLogin'] = users.create_login_url('/')
        questionList.sort(key = lambda x: x.modifiedDate, reverse=True)
        displayQuestions = []        
        for q in questionList:
            title = q.title
            if len(title) > 500:
                q.title = title[0:499] + "..."
                displayQuestions.append((q, False))
            else:
                body = q.body
                remaining_len = 500 - len(title)
                if body != None and len(body) > remaining_len:
                    q.body = body[0:remaining_len-1] + "..."
                displayQuestions.append((q, True))
        template_values['question'] = displayQuestions
        path = template_path('home.html')
        template_render = template.render(path, template_values)
        template_render = re.sub("(https?[^ ]*.((jpg)|(png)|(gif)))", r"<div><img src='\1' class='image_display' /></div>", template_render, flags=re.DOTALL)
        self.response.out.write(template_render)

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
        self.redirect('/viewQuestion?q='+str(question_post_id.id()))

class UpdateQuestion(webapp2.RequestHandler):
    def post(self):
        qId = self.request.get("qId")
        question_title = self.request.get("question");
        tags = self.request.get("tags")
        tags_array = filter(None,tags.split(","))
        question_db = Post.get_by_id(int(qId))
        question_db.title = question_title
        old_tags = question_db.tags
        question_db.tags = tags_array
        question_post_id = question_db.put()
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
        for old_t in old_tags:
            old_t = old_t.strip()            
            ot = Tags.query(Tags.name==old_t).fetch()
            ot[0].posts.remove(question_post_id)
            if len(ot[0].posts) == 0:
                ot[0].key.delete()
            else:
                ot[0].put()
        time.sleep(0.1)
        self.redirect('/viewQuestion?q='+qId)

class ViewQuestion(webapp2.RequestHandler):
    def get(self):
        qId = self.request.get("q")
        user = users.get_current_user()
        question = Post.get_by_id(int(qId))
        answers = Post.query(Post.parentId==question.key).order(-Post.voteCount).fetch()
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
        template_render = template.render(path, template_values)
        template_render = re.sub("(https?[^ ]*.((jpg)|(png)|(gif)))", r"<div><img src='\1' class='image_display_bigger' /></div>", template_render, flags=re.DOTALL)
        self.response.out.write(template_render)

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
        question.put()
        time.sleep(0.2)
        self.redirect('/viewQuestion?q='+qId)

class PostDescription(webapp2.RequestHandler):
    def post(self):
        q_description = self.request.get("q_description")        
        qId = self.request.get("q")
        question = Post.get_by_id(int(qId))
        question.body = q_description
        question.put()
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
            if post.parentId != None:
                question_db = Post.get_by_id(post.parentId.id())
                question_db.put()
            v.put()
        else:
            if existing_vote[0].vote != bool(vote):
                existing_vote[0].vote = bool(vote)
                if (bool(vote)):
                    post.voteCount = post.voteCount + 2
                else:
                    post.voteCount = post.voteCount - 2
                post.put()
                if post.parentId != None:
                    question_db = Post.get_by_id(post.parentId.id())
                    question_db.put()
                existing_vote[0].put()        
        time.sleep(0.2)
        self.redirect(str(url))

class UpdateAnswer(webapp2.RequestHandler):
    def post(self):
        aId = self.request.get('aId')
        url = self.request.get("url")
        answer = self.request.get('answer').strip()
        answer_post = Post.get_by_id(int(aId))
        answer_post.body = answer;
        answer_post.put()
        if answer_post.parentId != None:
            question_db = Post.get_by_id(answer_post.parentId.id())
            question_db.put()
        time.sleep(0.2)
        self.redirect(str(url))