import main
import unittest
import copy
import json
import flask
from pymongo import MongoClient
import datetime

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

EXAMPLE_USER = {"_id": "1", "name": "Michael Truell"}
EXAMPLE_SCHOOL = {"_id": "asdlfkj", "name": "Horace Mann School"}

class UserTestCase(NYCSLTestCase):
	def testGetAll(self):
		assert b'[]' in self.app.get("/users").data

		exampleUser = copy.deepcopy(EXAMPLE_USER)
		self.db.user.insert_one(exampleUser)
		newUser = json.loads(self.app.get("/users").data.decode("utf-8"))[0]
		assert areDicsEqual(exampleUser, newUser)

	def testGet(self):
		assert self.app.get("/users/1").status_code == 404

		exampleUser = copy.deepcopy(EXAMPLE_USER)
		self.db.user.insert_one(exampleUser)
		newUser = json.loads(self.app.get("/users/"+str(exampleUser['_id'])).data.decode("utf-8"))
		assert areDicsEqual(exampleUser, newUser)

	def testPost(self):
		exampleUser = copy.deepcopy(EXAMPLE_USER)
		exampleSchool = copy.deepcopy(EXAMPLE_SCHOOL)

		assert self.db.user.find_one(exampleUser) is None

		# Try posting without having logged in via github
		args = {"schoolID": exampleSchool["_id"], "userID": exampleUser["_id"]}
		req = self.app.post("/users", data=json.dumps(args), content_type="application/json")
		assert req.status_code == 400

		# Fake github login
		self.db.tempUser.insert_one(exampleUser)
		self.db.school.insert_one(exampleSchool)

		req = self.app.post("/users", data=json.dumps(args), content_type="application/json")
		assert req.status_code == 201

		returnedUser = json.loads(req.data.decode("utf-8"))

		assert returnedUser["schoolID"] == exampleSchool["_id"]
		returnedUser.pop("schoolID")

		assert areDicsEqual(exampleUser, returnedUser)
		assert self.db.user.find_one(exampleUser) is not None

def generateExampleEvent(db):
	exampleUser = copy.deepcopy(EXAMPLE_USER)
	db.user.insert_one(exampleUser)

	return {"userID": str(exampleUser["_id"]), "title": "New submission", "description": "Pushed a submission with a score of 14"}

class EventTestCase(NYCSLTestCase):
	def testGetAll(self):
		assert b'[]' in self.app.get("/events").data

		exampleEvent = generateExampleEvent(self.db)
		self.db.event.insert_one(exampleEvent)
		newEvent = json.loads(self.app.get("/events").data.decode("utf-8"))[0]
		assert areDicsEqual(exampleEvent, newEvent)
	def testGet(self):
		assert self.app.get("/events/1").status_code == 404

		exampleEvent = generateExampleEvent(self.db)
		self.db.event.insert_one(exampleEvent)
		newEvent = json.loads(self.app.get("/events/"+str(exampleEvent['_id'])).data.decode("utf-8"))
		assert areDicsEqual(exampleEvent, newEvent)
	def testPost(self):
		exampleEvent = generateExampleEvent(self.db)

		assert self.db.event.find_one(exampleEvent) is None

		req = self.app.post("/events", data=json.dumps(exampleEvent), content_type="application/json")
		assert req.status_code == 201

		returnedEvent = json.loads(req.data.decode("utf-8"))
		assert "_id" in returnedEvent
		returnedEvent.pop("_id")

		assert areDicsEqual(exampleEvent, returnedEvent)
		assert self.db.event.find_one(exampleEvent) is not None

EXAMPLE_PROBLEM = {"isAscending": True, "name": "Tetris", "description": "Write a bot to play the classic game Tetris"}

class ProblemTestCase(NYCSLTestCase):
	def testGetAll(self):
		assert b'[]' in self.app.get("/problems").data

		exampleProblem = copy.deepcopy(EXAMPLE_PROBLEM)
		self.db.problem.insert_one(exampleProblem)
		newProblem = json.loads(self.app.get("/problems").data.decode("utf-8"))[0]
		assert areDicsEqual(exampleProblem, newProblem)
	def testGet(self):
		assert self.app.get("/problems/1").status_code == 404

		exampleProblem = copy.deepcopy(EXAMPLE_PROBLEM)
		self.db.problem.insert_one(exampleProblem)
		newProblem = json.loads(self.app.get("/problems/"+str(exampleProblem['_id'])).data.decode("utf-8"))
		assert areDicsEqual(exampleProblem, newProblem)

INVALID_EXAMPLE_ENTRY = {"problemID": "incorrectproblemid", "userID": "incorrectuserid", "score": 12}

def generateExampleEntry(db):
	exampleUser = copy.deepcopy(EXAMPLE_USER)
	exampleProblem = copy.deepcopy(EXAMPLE_PROBLEM)

	db.user.insert_one(exampleUser)
	db.problem.insert_one(exampleProblem)

	return {"problemID": str(exampleProblem["_id"]), "userID": str(exampleUser["_id"]), "score": "12"}

class EntryTestCase(NYCSLTestCase):
	def testGetAll(self):
		assert b'[]' in self.app.get("/entries").data

		exampleEntry = generateExampleEntry(self.db)
		self.db.entry.insert_one(exampleEntry)
		newEntry = json.loads(self.app.get("/entries").data.decode("utf-8"))[0]
		assert areDicsEqual(exampleEntry, newEntry)

	def testGet(self):
		assert self.app.get("/entries/1").status_code == 404

		exampleEntry = generateExampleEntry(self.db)
		self.db.entry.insert_one(exampleEntry)
		newEntry = json.loads(self.app.get("/entries/"+str(exampleEntry['_id'])).data.decode("utf-8"))
		assert areDicsEqual(exampleEntry, newEntry)

EXAMPLE_BLOG = {"title": "Example Blog Post", "body": "Some random <b>html</b>"}

class BlogTestCase(NYCSLTestCase):
	def testGetAll(self):
		assert b'[]' in self.app.get("/blogs").data

		exampleBlog = copy.deepcopy(EXAMPLE_BLOG)
		self.db.blog.insert_one(exampleBlog)
		newBlog = json.loads(self.app.get("/blogs").data.decode("utf-8"))[0]
		assert areDicsEqual(exampleBlog, newBlog)
	def testGet(self):
		assert self.app.get("/blogs/1").status_code == 404

		exampleBlog = copy.deepcopy(EXAMPLE_BLOG)
		self.db.blog.insert_one(exampleBlog)
		newBlog = json.loads(self.app.get("/blogs/"+str(exampleBlog['_id'])).data.decode("utf-8"))
		assert areDicsEqual(exampleBlog, newBlog)

class SearchTestCase(NYCSLTestCase):
	def testGet(self):
		assert b'[]' in self.app.get("/search", data=json.dumps({"query": "thisshouldbeinnothing"}), content_type="application/json").data

		exampleUser = copy.deepcopy(EXAMPLE_USER)
		self.db.user.insert_one(exampleUser)

		req = self.app.get("/search", data=json.dumps({"query": exampleUser['name']}), content_type="application/json")
		returnedResults = json.loads(req.data.decode("utf-8"))
		correctResult = {"title": exampleUser["name"], "category": "user", "url": "/users/"+str(exampleUser["_id"])}
		assert correctResult in returnedResults

if __name__ == '__main__':
	unittest.main()
