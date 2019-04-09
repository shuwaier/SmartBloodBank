from flask import Flask
from flask_testing import TestCase
import unittest
from flask import current_app


class TestCase(TestCase):
        
    

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.assertEqual(app.debug, False)
        return app

    def test_main_page(self,create_app):
                self.app =create_app()
                self.app.app_context().push()
                response = self.app.get('/', follow_redirects=True)
                self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()
    
    