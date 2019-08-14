import unittest
import datagen_dao
import requests

class test_dao(unittest.TestCase):
    def test_as_user(self):
        loginJSON = {"username":"user","password":"pass"}
        userObj = datagen_dao.as_user(loginJSON)
        assert userObj.username == "user", "Should return user"

    def test_as_pass(self):
        loginJSON = {"username":"user","password":"pass"}
        userObj = datagen_dao.as_user(loginJSON)
        assert userObj.password == "pass", "Should return pass"

    def test_auth_fail(self):
        loginJSON = {"username":"user","password":"pass"}
        response = requests.post("http://127.0.0.1:5000/login", json=loginJSON)
        assert response.status_code == 401

    def test_auth_good(self):
        loginJSON = {"username":"James","password":"pwd"}
        response = requests.post("http://127.0.0.1:5000/login", json=loginJSON)
        assert response.status_code == 200

    def test_auth_Trader(self):
        loginJSON = {"username":"James","password":"pwd"}
        response = requests.post("http://127.0.0.1:5000/login", json=loginJSON)
        assert response.text == {'type':'Trader'}

    def test_auth_Senior_Trader(self):
        loginJSON = {"username":"Jools","password":"pwd"}
        response = requests.post("http://127.0.0.1:5000/login", json=loginJSON)
        assert response.text == {'type':'Senior Trader'}


if __name__ == "__main__":
    unittest.main()
