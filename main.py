#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASSWORD_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)

header = """
<!DOCTYPE html>
<html>
    <head>
        <style type="text/css">
            .error {
            color: red;
            }
        </style>
    </head>
        <body>
            <title>Signup</title>
                <h1>Signup</h1>
"""

username = """
    <label>
        Username
        <input type='text' name='username' value=''>
    </label>
"""
password = """
    <label>
        Password
        <input type='password' name='password' value=''>
    </label>
"""
verify = """
    <label>
        Verify Password
        <input type='password' name='verify' value ''>
    </label>
"""
email = """
    <label>
        Email (optional)
        <input type='text' name='email' value=''>
    </label>
"""
submit = """
    <input type='submit' value='Sign Up!'/>
"""
form = """
    <form method='post' action='/signup'>
"""

form_end = """
    </form>
"""

content = (
form + username + "<br>" + password + "<br>" + verify + "<br>" + email + "<br>" + submit + form_end
)

footer = """
    </body>
</html>
"""
def build_page(page):
    page = header + "<br>" + content + "<br>" + footer
    return page

class MainHandler(webapp2.RequestHandler):
    def get(self):
        content = build_page("")
        self.response.write(content)


class SignUp(webapp2.RequestHandler):
    def post(self):
        username = self.request.get('username')
        if valid_username(username) == None:
            error_username = (
            "<p class='error'>" +
            valid_username(username) +
            "</p>")
        else:
            error_username = ""
        #password = self.request.get('password')
        #good_password = valid_password(password)
        #if good_password == None:
        #    self.response.write("Your Password is bad.")
        #verify = self.request.get('verify')
        #if verify != password:
        #    self.response.write("Your passwords don't match!")
        email = self.request.get('email')
        if email == "":
            pass
        else:
            email = valid_email(email)
            if email == None:
                self.response.write("Your email is invalid.")

        #self.redirect('/welcome')


class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.write("Welcome, " + username + "!")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', SignUp),
    ('/welcome', Welcome)
], debug=True)
