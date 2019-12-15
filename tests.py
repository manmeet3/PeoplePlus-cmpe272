from flask_testing import TestCase
import os
import unittest
from app.models import Department, Employee, DeptEmp
from flask import abort, url_for
from app import create_app

class TestBase(TestCase):
    def create_app(self):
        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        # app.config.update(
        #     SQLALCHEMY_DATABASE_URI='mysql://dt_admin:dt2016@localhost/dreamteam_test'
        # )
        return app

    def setUp(self):
      pass

    def test_employee_model(self):
        """
        Test number of records in Employee table
        """
        self.assertNotEqual(Employee.query.count(), 0)

    def test_department_model(self):
        """
        Test number of records in Employee table
        """
        self.assertNotEqual(Department.query.count(), 0)

    def test_deptEmp_model(self):
        self.assertNotEqual(Department.query.count(), 0)



    def tearDown(self):
        pass

class TestErrorPages(TestBase):

    def test_403_forbidden(self):
        # create route to abort the request with the 403 Error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        #self.assertTrue("403 Error" in response.data)

    def test_404_not_found(self):
        response = self.client.get('/nothinghere')
        self.assertEqual(response.status_code, 404)
        #self.assertTrue("404 Error" in response.data)

    def test_500_internal_server_error(self):
        # create route to abort the request with the 500 Error
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        #self.assertTrue("500 Error" in response.data)

class TestViews(TestBase):

    def test_homepage_view(self):
        """
        Test that homepage is accessible without login
        """
        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()

