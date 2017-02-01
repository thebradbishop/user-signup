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

error_username = ""

error_password = ""

error_verify = ""

error_email = ""

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
form + username + "<br>" + password + "<br>" + verify + "<br>" + email + "<br><br>" + submit + form_end
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
        input_username = self.request.get('username')
        if valid_username(input_username) == None:
            error_username ="""
            <text class='error'>
            The username entered is not valid!
            </text>
            """
        else:
            error_username = ""
        username = """
            <label>
                Username
                <input type='text' name='username' value='{0}'>
            </label>{1}
        """.format(input_username, error_username)

        input_password = self.request.get('password')
        if valid_password(input_password) == None:
            error_password = """
            <text class='error'>
            The password entered is not valid!
            </text>
            """
        else:
            error_password = ""
        password = """
            <label>
                Password
                <input type='password' name='password' value=''>
            </label>{0}
        """.format(error_password)

        verify = self.request.get('verify')
        error_verify = ""
        if verify != input_password:
            error_verify = """
            <text class='error'>
            Your passwords don't match!
            </text>
            """
        verify = """
            <label>
                Verify Password
                <input type='password' name='verify' value ''>
            </label>{0}
        """.format(error_verify)

        input_email = self.request.get('email')
        error_email = ""
        save_email = """
        <label>
        Email (optional)
        <input type='text' name='email' value='{0}'>
        </label>{1}
        """.format(input_email, error_email)
        if input_email == "":
            pass
        else:
            input_email = valid_email(input_email)
            if input_email == None:
                error_email = """
                <text class='error'>
                Your email is invalid!
                </text>
                """
                save_email = """
                <label>
                Email (optional)
                <input type='text' name='email' value='{0}'>
                </label>{1}
                """.format(input_email, error_email)

        if error_username == '':
            if error_verify == '':
                if error_email == '':
                    self.redirect("/welcome?username=" + input_username)

        content = (
        form + username + "<br>" + password + "<br>" + verify + "<br>" + save_email + "<br><br>" + submit + form_end
        )
        page = header + "<br>" + content + "<br>" + footer
        self.response.write(page)



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
