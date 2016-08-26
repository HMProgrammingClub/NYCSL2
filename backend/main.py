from flask import Flask, abort, session, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask.ext.cors import CORS
from werkzeug import FileStorage

from bson.objectid import ObjectId
from tools import jsonify

from pymongo import MongoClient, TEXT

import configparser

import hashlib
from base64 import b64encode

import subprocess
import shlex

import datetime

app = Flask(__name__, static_url_path="")

config = configparser.ConfigParser()
config.read("../nycsl.ini")
app.secret_key = config["BACKEND"]["secretKey"]
SALT = config["BACKEND"]["salt"]

SEARCHABLE_COLLECTION_ATTRIBUTES = [{"collectionName": "user", "linkLead": "/users/", "nameField": "name"}, {"collectionName": "problem", "linkLead": "/problems/", "nameField": "name"}, {"collectionName": "blog", "linkLead": "/blogs/", "nameField": "title"}]
PROBLEMS_DIR = "../problems/"
GRADING_SCRIPT = "grade.py"
CURRENT_SEASON = 0

db = MongoClient().nycsl

def hashPassword(password):
	passbits = password.encode('utf-8')
	saltbits = SALT.encode('utf-8')
	return b64encode(hashlib.pbkdf2_hmac('sha256', passbits, saltbits, 100000)).decode('utf-8')

class LoginAPI(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument("email", type=str, required=True, location="args")
		self.parser.add_argument("password", type=str, required=True, location="args")
		super(LoginAPI, self).__init__()

	def get(self):
		if "userID" not in session:
			return jsonify({"loggedIn": False})

		user = db.user.find_one({"_id": ObjectId(session["userID"])})
		if user is None:
			session.pop("userID")
			return jsonify({"loggedIn": False})
		return jsonify({ "loggedIn": True, "user": user })

	def post(self):
		if "userID" in session:
			abort(409)

		args = self.parser.parse_args()
		user = db.user.find_one({"email": args["email"], "password": hashPassword(args["password"])})
		if user is None:
			abort(400)

		session['userID'] = str(user["_id"])
		return jsonify(user, status=201)

	def delete(self):
		if "userID" not in session:
			abort(404)

		session.pop("userID")
		return jsonify({"result": True})

class UserListAPI(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument("email", type=str, required=True, location="args")
		self.parser.add_argument("password", type=str, required=True, location="args")
		self.parser.add_argument("name", type=str, required=True, location="args")
		self.parser.add_argument("school", type=str, location="args")
		super(UserListAPI, self).__init__()

	def get(self):
		return jsonify([a for a in db.user.find({})])

	def post(self):
		user = self.parser.parse_args()
		user["isVerified"] = False
		user["joinDate"] = datetime.datetime.today().strftime('%Y-%m-%d')
		user["password"] = hashPassword(user["password"])

		db.user.insert_one(user)

		return jsonify(user, status=201)


class UserAPI(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument("email", type=str, location="args")
		self.parser.add_argument("password", type=str, location="args")
		self.parser.add_argument("name", type=str, location="args")
		self.parser.add_argument("school", type=str, location="args")
		self.parser.add_argument("isVerified", type=str, location="args")
		super(UserAPI, self).__init__()

	def get(self, userID):
		try:
			user = db.user.find_one({"_id": ObjectId(userID)})
		except:
			abort(404)
		if user is None:
			abort(404)
		return jsonify(user)

	def put(self, userID):
		try:
			user = db.user.find_one({"_id": ObjectId(userID)})
		except:
			abort(404)
		if user is None:
			abort(404)

		args = self.parser.parse_args()
		try:
			db.user.find_one({"_id": ObjectId(userID), "password": hashPassword(args["password"])})
		except:
			abort(400)

		for k, v in args.items():
			if v is not None:
				user[k] = v

		db.user.save(user)
		return jsonify(user)

class EventListAPI(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument("userID", type=str, required=True, location="args")
		self.parser.add_argument("title", type=str, required=True, location="args")
		self.parser.add_argument("description", type=str, required=True, location="args")
		super(EventListAPI, self).__init__()

	def get(self):
		return jsonify([a for a in db.event.find({})])

	def post(self):
		event = self.parser.parse_args()

		try:
			db.user.find_one({"_id": ObjectId(event['userID'])})
		except:
			abort(400)

		db.event.insert_one(event)

		return jsonify(event, status=201)


class EventAPI(Resource):
	def get(self, eventID):
		try:
			event = db.event.find_one({"_id": ObjectId(eventID)})
		except:
			abort(404)
		if event is None:
			abort(404)
		return jsonify(event)


class ProblemListAPI(Resource):
	def get(self):
		return jsonify([a for a in db.problem.find({}).sort('_id', -1)])

class ProblemAPI(Resource):
	def get(self, problemID):
		try:
			problem = db.problem.find_one({"_id": ObjectId(problemID)})
		except:
			abort(404)
		if problem is None:
			abort(404)
		return jsonify(problem)

class EntryListAPI(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument("problemID", type=str, required=True, location="args")
		self.parser.add_argument("userID", type=str, required=True, location="args")
		self.parser.add_argument("file", type=FileStorage, required=True, location="files")
		super(EntryListAPI, self).__init__()

	def get(self):
		return jsonify([a for a in db.entry.find({})])

	def post(self):
		entry = self.parser.parse_args()

		try:
			if db.problem.find_one({"_id": ObjectId(entry['problemID'])}) == None:
				abort(400)
			if db.user.find_one({"_id": ObjectId(entry['userID'])}) == None:
				abort(400)
		except:
			abort(400)

		problemName =  db.problem.find_one({"_id": ObjectId(entry['problemID'])})['name']
		gradingFilePath = os.path.join(os.path.join(PROBLEMS_DIR, problemName.lower()), GRADING_SCRIPT)
		command = "python3 "+gradingFilePath+" \""+entry["file"].stream+"\""
		gradingOutput = subprocess.Popen(shlex.split(command.replace('\\','/')), stdout=subprocess.PIPE).communicate()[0]
		structuredGradingOutput = json.loads(gradingOutput)

		status_code = None
		if "score" in structuredGradingOutput:
			entry["score"] = structuredGradingOutput["score"]
			entry.pop("file")
			db.entry.insert_one(entry)
			status_code = 201
		else:
			status_code = 400

		return jsonify(structuredGradingOutput, status=status_code)

class EntryAPI(Resource):
	def get(self, entryID):
		try:
			entry = db.entry.find_one({"_id": ObjectId(entryID)})
		except:
			abort(404)
		if entry is None:
			abort(404)
		return jsonify(entry)

class BlogListAPI(Resource):
	def get(self):
		return jsonify([a for a in db.blog.find({}).sort('_id', -1)])

class BlogAPI(Resource):
	def get(self, blogID):
		try:
			blog = db.blog.find_one({"_id": ObjectId(blogID)})
		except:
			abort(404)
		if blog is None:
			abort(404)
		return jsonify(blog)

class SearchAPI(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument("query", type=str, required=True, location="args")
		self.parser.add_argument("maxResults", type=int, default=10, location="args")
		super(SearchAPI, self).__init__()

	def get(self):
		args = self.parser.parse_args()
		query = args["query"]
		maxResults = args["maxResults"]

		searchResults = []
		isDone = False
		for collectionAttrs in SEARCHABLE_COLLECTION_ATTRIBUTES:
			if isDone: break

			collection = db[collectionAttrs["collectionName"]]
			collection.create_index([("$**", TEXT)])
			results = collection.find({"$text": {"$search": query}})
			for res in results:
				if len(searchResults) >= maxResults:
					isDone = True
					break
				searchResults.append({"category": collectionAttrs["collectionName"], "title": res[collectionAttrs['nameField']], "url": collectionAttrs['linkLead']+str(res["_id"])})

		returnedResults = { "results" : {}}
		for i in searchResults:
			if i['category'] in returnedResults['results'].keys():
				returnedResults['results'][i['category']]['results'].append(i)
			else:
				returnedResults['results'].update({i['category']: {'results': [i], 'name': i['category']}})


		return jsonify(returnedResults)

api = Api(app)

api.add_resource(LoginAPI, '/login', endpoint='login')

api.add_resource(UserListAPI, '/users', endpoint='users')
api.add_resource(UserAPI, '/users/<userID>', endpoint='user')

api.add_resource(EventListAPI, '/events', endpoint='events')
api.add_resource(EventAPI, '/events/<eventID>', endpoint='event')

api.add_resource(ProblemListAPI, '/problems', endpoint='problems')
api.add_resource(ProblemAPI, '/problems/<problemID>', endpoint='problem')

api.add_resource(EntryListAPI, '/entries', endpoint='entries')
api.add_resource(EntryAPI, '/entries/<entryID>', endpoint='entry')

api.add_resource(BlogListAPI, '/blogs', endpoint='blogs')
api.add_resource(BlogAPI, '/blogs/<blogID>', endpoint='blog')

api.add_resource(SearchAPI, '/search', endpoint='search')

CORS(app)

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)
