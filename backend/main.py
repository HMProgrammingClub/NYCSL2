from flask import Flask, abort, session, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask.ext.cors import CORS

from bson.objectid import ObjectId
from tools import jsonify

from pymongo import MongoClient, TEXT

import configparser

import hashlib
from base64 import b64encode

app = Flask(__name__, static_url_path="")

config = configparser.ConfigParser()
config.read("../nycsl.ini")
app.secret_key = config["BACKEND"]["secretKey"]
SALT = config["BACKEND"]["salt"]

SEARCHABLE_COLLECTION_ATTRIBUTES = [{"collectionName": "user", "linkLead": "/users/", "nameField": "name"}, {"collectionName": "problem", "linkLead": "/problems/", "nameField": "name"}]

db = MongoClient().nycsl

def hashPassword(password):
	passbits = password.encode('utf-8')
	saltbits = SALT.encode('utf-8')
	return b64encode(hashlib.pbkdf2_hmac('sha256', passbits, saltbits, 100000)).decode('utf-8')

class LoginAPI(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument("email", type=str, required=True, location="json")
		self.parser.add_argument("password", type=str, required=True, location="json")
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
		self.parser.add_argument("email", type=str, required=True, location="json")
		self.parser.add_argument("password", type=str, required=True, location="json")
		self.parser.add_argument("name", type=str, required=True, location="json")
		self.parser.add_argument("school", type=str, location="json")
		super(UserListAPI, self).__init__()

	def get(self):
		return jsonify([a for a in db.user.find({})])

	def post(self):
		user = self.parser.parse_args()
		user["isVerified"] = False

		user["password"] = hashPassword(user["password"])

		db.user.insert_one(user)

		return jsonify(user, status=201)


class UserAPI(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument("email", type=str, location="json")
		self.parser.add_argument("password", type=str, location="json")
		self.parser.add_argument("name", type=str, location="json")
		self.parser.add_argument("school", type=str, location="json")
		self.parser.add_argument("isVerified", type=str, location="json")
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
		for k, v in args.items():
			if v is not None:
				user[k] = v

		db.user.save(user)
		return jsonify(user)

	def delete(self, userID):
		result = db.user.delete_one({"_id": ObjectId(userID)})
		if result.deleted_count < 1:
			abort(404)
		return jsonify({"result": True})



class ProblemListAPI(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument("abbreviation", type=str, required=True, location="json")
		self.parser.add_argument("isAscending", type=bool, required=True, location="json")
		self.parser.add_argument("name", type=str, required=True, location="json")
		self.parser.add_argument("description", type=str, required=True, location="json")
		super(ProblemListAPI, self).__init__()

	def get(self):
		return jsonify([a for a in db.problem.find({})])

	def post(self):
		problem = self.parser.parse_args()

		db.problem.insert_one(problem)

		return jsonify(problem, status=201)

class ProblemAPI(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument("abbreviation", type=str, location="json")
		self.parser.add_argument("isAscending", type=bool, location="json")
		self.parser.add_argument("name", type=str, location="json")
		self.parser.add_argument("description", type=str, location="json")
		super(ProblemAPI, self).__init__()

	def get(self, problemID):
		try:
			problem = db.problem.find_one({"_id": ObjectId(problemID)})
		except:
			abort(404)
		if problem is None:
			abort(404)
		return jsonify(problem)

	def put(self, problemID):
		try:
			problem = db.problem.find_one({"_id": ObjectId(problemID)})
		except:
			abort(404)
		if problem is None:
			abort(404)

		args = self.parser.parse_args()
		for k, v in args.items():
			if v is not None:
				problem[k] = v

		db.problem.save(problem)
		return jsonify(problem)

	def delete(self, problemID):
		result = db.problem.delete_one({"_id": ObjectId(problemID)})
		if result.deleted_count < 1:
			abort(404)
		return jsonify({"result": True})

class EntryListAPI(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument("problemID", type=str, required=True, location="json")
		self.parser.add_argument("userID", type=str, required=True, location="json")
		self.parser.add_argument("score", type=str, required=True, location="json")
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

		db.entry.insert_one(entry)

		return jsonify(entry, status=201)

class EntryAPI(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument("problemID", type=str, location="json")
		self.parser.add_argument("userID", type=str, location="json")
		self.parser.add_argument("score", type=int, location="json")
		super(EntryAPI, self).__init__()

	def get(self, entryID):
		try:
			entry = db.entry.find_one({"_id": ObjectId(entryID)})
		except:
			abort(404)
		if entry is None:
			abort(404)
		return jsonify(entry)

	def put(self, entryID):
		try:
			entry = db.entry.find_one({"_id": ObjectId(entryID)})
		except:
			abort(404)
		if entry is None:
			abort(404)

		args = self.parser.parse_args()
		for k, v in args.items():
			if v is not None:
				entry[k] = v

		db.entry.save(entry)
		return jsonify(entry)

	def delete(self, entryID):
		result = db.entry.delete_one({"_id": ObjectId(entryID)})
		if result.deleted_count < 1:
			abort(404)
		return jsonify({"result": True})

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
				searchResults.append({"category": collectionAttrs["collectionName"], "name": res[collectionAttrs['nameField']], "link": collectionAttrs['linkLead']+str(res["_id"])})

		return jsonify(searchResults)

api = Api(app)

api.add_resource(LoginAPI, '/login', endpoint='login')

api.add_resource(UserListAPI, '/users', endpoint='users')
api.add_resource(UserAPI, '/users/<userID>', endpoint='user')

api.add_resource(ProblemListAPI, '/problems', endpoint='problems')
api.add_resource(ProblemAPI, '/problems/<problemID>', endpoint='problem')

api.add_resource(EntryListAPI, '/entries', endpoint='entries')
api.add_resource(EntryAPI, '/entries/<entryID>', endpoint='entry')

api.add_resource(SearchAPI, '/search', endpoint='search')

CORS(app)

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)
