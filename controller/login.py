import webapp2

from google.appengine.api import users


class MainPage(webapp2.RequestHandler):

    def get(self):
        # [START get_current_user]
        # Checks for active Google account session
        user = users.get_current_user()
        # [END get_current_user]

        # [START if_user]
        if user:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('Hello there, ' + user.nickname())
        # [END if_user]
        # [START if_not_user]
        else:
            self.redirect(users.create_login_url(self.request.uri))
        # [END if_not_user]