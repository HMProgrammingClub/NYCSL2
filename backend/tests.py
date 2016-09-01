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

EXAMPLE_USER = {"email": "test@gmail.com", "name": "Michael Truell", "school": "Horace Mann", "password": "dummyPassword"}

class LoginTestCase(NYCSLTestCase):
	def testGet(self):
		assert json.loads(self.app.get("/login").data.decode("utf-8")) == {"loggedIn": False}
		exampleUser = copy.deepcopy(EXAMPLE_USER)
		self.db.user.insert_one(exampleUser)

		with self.app.session_transaction() as session:
			session["userID"] = str(exampleUser["_id"])

		response = json.loads(self.app.get("/login").data.decode("utf-8"))
		assert response["loggedIn"] == True
		assert areDicsEqual(response["user"], exampleUser)

	def testPost(self):
		exampleUser = copy.deepcopy(EXAMPLE_USER)
		loginInfo = {"email": exampleUser["email"], "password": exampleUser["password"]}
		exampleUser["password"] = main.hashPassword(exampleUser["password"])

		assert self.app.post("/login", data=json.dumps(loginInfo), content_type="application/json").status_code == 400

		self.db.user.insert_one(exampleUser)
		req = self.app.post("/login", data=json.dumps(loginInfo), content_type="application/json")
		assert req.status_code == 201
		assert areDicsEqual(json.loads(req.data.decode("utf-8")), exampleUser)
		with self.app.session_transaction() as session:
			assert session["userID"] == str(exampleUser["_id"])

		assert self.app.post("/login", data=json.dumps(loginInfo), content_type="application/json").status_code == 409

	def testDelete(self):
		assert self.app.delete("/login").status_code == 404
		with self.app.session_transaction() as session:
			session["userID"] = str("RANDOM_PLACEHOLDER_ID")
		assert json.loads(self.app.delete("/login").data.decode("utf-8")) == {"result": True}

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

		assert self.db.user.find_one(exampleUser) is None

		req = self.app.post("/users", data=json.dumps(exampleUser), content_type="application/json")
		assert req.status_code == 201

		returnedUser = json.loads(req.data.decode("utf-8"))
		assert "_id" in returnedUser
		returnedUser.pop("_id")

		assert "joinDate" in returnedUser
		try:
			datetime.datetime.strptime(returnedUser["joinDate"], '%Y-%m-%d')
		except:
			assert False
		returnedUser.pop("joinDate")

		assert "isVerified" in returnedUser
		returnedUser.pop("isVerified")

		assert returnedUser["password"] != exampleUser["password"]
		returnedUser.pop("password")
		exampleUser.pop("password")

		assert areDicsEqual(exampleUser, returnedUser)
		assert self.db.user.find_one(exampleUser) is not None
	def testPut(self):
		exampleUser = copy.deepcopy(EXAMPLE_USER)
		self.db.user.insert_one(exampleUser)

		exampleUser["name"] = "A way different name"
		exampleUser["_id"] = str(exampleUser["_id"])

		req = self.app.put("/users/"+exampleUser["_id"], data=json.dumps(exampleUser), content_type="application/json")
		returnedUser = json.loads(req.data.decode("utf-8"))

		assert areDicsEqual(returnedUser, exampleUser)

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

def generateExampleEntry(db, exampleProblem=EXAMPLE_PROBLEM, exampleUser=EXAMPLE_USER):
	exampleUser = copy.deepcopy(exampleUser)
	exampleProblem = copy.deepcopy(exampleProblem)

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

	def testGetProblem(self):
		assert b'[]' in self.app.get("/entries").data

		exampleEntry1 = generateExampleEntry(self.db)

		exampleProblem2 = copy.deepcopy(EXAMPLE_PROBLEM)
		exampleProblem2["name"] = "Other Problem"
		exampleEntry2 = generateExampleEntry(self.db, exampleProblem=exampleProblem2)

		self.db.entry.insert_one(exampleEntry1)
		self.db.entry.insert_one(exampleEntry2)

		returnedEntries = json.loads(self.app.get("/entries", query_string={"problemID": exampleEntry1["problemID"]}).data.decode("utf-8"))
		assert areDicsEqual(exampleEntry1, returnedEntries[0])
		assert len(returnedEntries) == 1

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

		req = self.app.get("/search", data=json.dumps({"query": exampleUser['email']}), content_type="application/json")
		returnedResults = json.loads(req.data.decode("utf-8"))
		correctResult = {"title": exampleUser["name"], "category": "user", "url": "/users/"+str(exampleUser["_id"])}
		assert correctResult in returnedResults

if __name__ == '__main__':
	unittest.main()
