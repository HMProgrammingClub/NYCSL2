import main
import unittest
import copy
import json
from pymongo import MongoClient

def areDicsEqual(dic1, dic2):
	if len(dic1) != len(dic2):
		print(dic1)
		print(dic2)
		return False
	for k in dic1:
		if k not in dic2:
			print(dic1)
			print(dic2)
			return False

		# Incase one was an ObjectID and the other was a string representation of the object id, cast both to string for evaluation
		if str(dic1[k]) != str(dic2[k]):
			print(dic1)
			print(dic2)
			return False
	return True

class NYCSLTestCase(unittest.TestCase):
	def setUp(self):
		main.db = MongoClient().test
		self.db = main.db
		self.app = main.app.test_client()

	def tearDown(self):
		MongoClient().drop_database("test")

DUMMY_USER = {"email": "test@gmail.com", "name": "Michael Truell", "school": "Horace Mann", "password": "dummyPassword"}

class UserTestCase(NYCSLTestCase):
	def testGetAll(self):
		assert b'[]' in self.app.get("/users").data

		exampleUser = copy.deepcopy(DUMMY_USER)
		self.db.user.insert_one(exampleUser)
		newUser = json.loads(self.app.get("/users").data.decode("utf-8"))[0]
		assert areDicsEqual(exampleUser, newUser)
	def testGet(self):
		assert self.app.get("/users/1").status_code == 404

		exampleUser = copy.deepcopy(DUMMY_USER)
		self.db.user.insert_one(exampleUser)
		newUser = json.loads(self.app.get("/users/"+str(exampleUser['_id'])).data.decode("utf-8"))
		assert areDicsEqual(exampleUser, newUser)
	def testPost(self):
		exampleUser = copy.deepcopy(DUMMY_USER)

		assert self.db.user.find_one(exampleUser) is None

		req = self.app.post("/users", data=json.dumps(exampleUser), content_type="application/json")
		assert req.status_code == 201

		returnedUser = json.loads(req.data.decode("utf-8"))
		returnedUser.pop("_id")
		returnedUser.pop("isVerified")

		assert areDicsEqual(exampleUser, returnedUser)
		assert self.db.user.find_one(exampleUser) is not None
	def testPut(self):
		exampleUser = copy.deepcopy(DUMMY_USER)
		self.db.user.insert_one(exampleUser)

		exampleUser["name"] = "A way different name"
		exampleUser["_id"] = str(exampleUser["_id"])

		req = self.app.put("/users/"+exampleUser["_id"], data=json.dumps(exampleUser), content_type="application/json")
		returnedUser = json.loads(req.data.decode("utf-8"))

		assert areDicsEqual(returnedUser, exampleUser)

	def testDelete(self):
		exampleUser = copy.deepcopy(DUMMY_USER)
		self.db.user.insert_one(exampleUser)
		self.app.delete("/users/"+str(exampleUser["_id"]))
		assert self.db.user.find_one(exampleUser) is None

if __name__ == '__main__':
	unittest.main()
