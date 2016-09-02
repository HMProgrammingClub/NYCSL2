from flask import Flask, abort, session, make_response, redirect
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask.ext.cors import CORS
from werkzeug import FileStorage

from bson.objectid import ObjectId
from tools import jsonify

from pymongo import MongoClient, TEXT

import configparser

import subprocess
import shlex

import datetime

import requests

app = Flask(__name__, static_url_path="")

config = configparser.ConfigParser()
config.read("../nycsl.ini")

app.secret_key = config["BACKEND"]["secretKey"]
SALT = config["BACKEND"]["salt"]
GITHUB_CLIENT_ID= config["BACKEND"]["githubClientID"]
GITHUB_CLIENT_SECRET = config["BACKEND"]["githubClientSecret"]
WEBSITE_DOMAIN = config["BACKEND"]["websiteDomain"]

SEARCHABLE_COLLECTION_ATTRIBUTES = [{"collectionName": "user", "linkLead": "/users/", "nameField": "name"}, {"collectionName": "problem", "linkLead": "/problems/", "nameField": "name"}, {"collectionName": "blog", "linkLead": "/blogs/", "nameField": "title"}]
PROBLEMS_DIR = "../problems/"
GRADING_SCRIPT = "grade.py"
CURRENT_SEASON = 0

db = MongoClient().nycsl

class LoginAPI(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument("code", type=str, required=True, location="json")
		code = parser.parse_args()["code"]

		response = json.loads(requests.post("https://github.com/login/oauth/access_token", json={"code": code, "client_id": GITHUB_CLIENT_ID, "client_secret": GITHUB_CLIENT_SECRET}).text)

		accessToken = response["access_token"]
		githubUser = json.loads(requests.get("https://api.github.com/user", data={"access_token": accessToken}).text)

		dbUser = db.user.find_one({"_id": githubUser['id']})
		if dbUser is None:
			newUser = {"_id": githubUser["id"], "name": githubUser['username'], "joinDate": datetime.datetime.today().strftime('%Y-%m-%d')}
			db.tempUser.insert_one(newUser)

			return redirect(WEBSITE_DOMAIN+"/signup.html#"+newUser["_id"])
		else:
			session['userID'] = dbUser["_id"]
			return jsonify({ "loggedIn": True, "user": user })

class SessionAPI(Resource):
	def get(self):
		if "userID" not in session:
			return jsonify({"loggedIn": False})

		user = db.user.find_one({"_id": session["userID"]})
		if user is None:
			session.pop("userID")
			return jsonify({"loggedIn": False})
		return jsonify({ "loggedIn": True, "user": user })

	def delete(self):
		if "userID" not in session:
			abort(404)

		session.pop("userID")
		return jsonify({"result": True})

class UserListAPI(Resource):
	def get(self):
		return jsonify([a for a in db.user.find({})])

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("schoolID", type=str, required=True, location="json")
		parser.add_argument("userID", type=str, required=True, location="json")

		args = parser.parse_args()

		user = db.tempUser.find_one({"_id": args["userID"]})
		if user is None: abort(400)

		school = db.school.find_one({"_id": args["schoolID"]})
		if school is None: abort(400)

		user["schoolID"] = args["schoolID"]

		db.user.insert_one(user)
		session['userID'] = user["_id"]

		return jsonify(user, status=201)

class UserAPI(Resource):
	def get(self, userID):
		try:
			user = db.user.find_one({"_id": userID})
		except:
			abort(404)
		if user is None:
			abort(404)
		return jsonify(user)


class EventListAPI(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument("userID", type=str, required=True, location="json")
		self.parser.add_argument("title", type=str, required=True, location="json")
		self.parser.add_argument("description", type=str, required=True, location="json")
		super(EventListAPI, self).__init__()

	def get(self):
		return jsonify([a for a in db.event.find({})])

	def post(self):
		event = self.parser.parse_args()

		try:
			db.user.find_one({"_id": event['userID']})
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
		self.parser.add_argument("problemID", type=str, required=True, location="json")
		self.parser.add_argument("userID", type=str, required=True, location="json")
		self.parser.add_argument("file", type=FileStorage, required=True, location="files")
		super(EntryListAPI, self).__init__()

	def get(self):
		return jsonify([a for a in db.entry.find({})])

	def post(self):
		entry = self.parser.parse_args()

		try:
			if db.problem.find_one({"_id": ObjectId(entry['problemID'])}) == None:
				abort(400)
			if db.user.find_one({"_id": entry['userID']}) == None:
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
		self.parser.add_argument("query", type=str, required=True, location="json")
		self.parser.add_argument("maxResults", type=int, default=10, location="json")
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

		return jsonify(searchResults)

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
