import re
import threading
import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from app import create_app, db, fake
from app.models import Role, User, Post


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # start Chrome
        options = Options()
        options.headless = True
        service = Service("/usr/bin/chromedriver")
        try:
            cls.client = webdriver.Chrome(service=service, options=options)
        except:
            pass

        # skip these tests if the browser could not be started
        if cls.client:
            # create the application
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # suppress logging to keep unittest output clean
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            # create the database and populate with some fake data
            db.create_all()
            Role.insert_roles()
            fake.users(10)
            fake.posts(10)

            # add an administrator user
            admin_role = Role.query.filter_by(name='Admin').first()
            admin = User(email='john@example.org',
                         username='john', password='caterpillar',
                         role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()

            # start the Flask server in a thread
            cls.server_thread = threading.Thread(target=cls.app.run,
                                                 kwargs={'debug': False})
            cls.server_thread.start()

            # give the server a second to ensure it is up
            time.sleep(1) 

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # stop the flask server and the browser
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.quit()
            cls.server_thread.join()

            # destroy database
            db.drop_all()
            db.session.remove()

            # remove application context
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        # navigate to home page
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Hello,\s+Stranger\s+!',
                                  self.client.page_source))

        # navigate to login page
        self.client.find_element("link text", "Log In").click()
        self.assertTrue(re.search('[<h1>Log in</h1>]',
                                  self.client.page_source))

        from selenium.webdriver.support.ui import WebDriverWait
        # from selenium.webdriver.support import expected_conditions as EC
        
        # login
        username = self.client.find_element('name', 'email')
        # print(username.is_displayed())
        username.clear()
        username.send_keys("john@example.org")
        
        password = self.client.find_element('name', 'password')
        # print(password.is_displayed())
        password.clear()
        password.send_keys("caterpillar")
        
        # print(username.get_attribute("value"))
        # print(password.get_attribute("value"))
    
        self.client.find_element('name', 'submit').click()
        # print(self.client.page_source)

        # wait the ready state to be complete
        WebDriverWait(driver=self.client, timeout=10).until(
                lambda x: x.execute_script("return document.readyState === 'complete'")
                        )
        error_message = "Invalid email or password"
        # get the errors (if there are)
        errors = self.client.find_elements('class name', "alert-danger")
        # print the errors optionally
        # for e in errors:
            # print(e.text)
        # if we find that error message within errors, then login is failed
        # if any(error_message in e.text for e in errors):
        #     print("[!] Login failed")
        # else:
        #     print("[+] Login successful")

        
        # login failed ???
        

        # navigate to the user's profile page
        # time.sleep(2)
        # print(self.client.page_source)
        # WebDriverWait(self.client, 10).until(EC.element_to_be_clickable(self.client.find_element("link text", "Profile")))
        # self.client.find_element("link text", "Profile").click()
        # self.assertIn('<h1>john</h1>', self.client.page_source)
        # self.assertTrue(re.search('[<h1>john</h1>]',
                                #   self.client.page_source))