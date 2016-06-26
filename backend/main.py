from flask import Flask, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal

from bson.objectid import ObjectId
from tools import jsonify

from pymongo import MongoClient

app = Flask(__name__, static_url_path="")

db = MongoClient().nycsl

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

		db.user.insert_one(user)
		return jsonify(user), 201


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

		args = parser.parse_args()
		for k, v in args.items():
			if v is not None:
				user[k] = v

		db.user.update_one(user)
		return jsonify(user)

	def delete(self, userID):
		result = db.user.delete_one({"_id": ObjectId(userID)})
		if result.deleted_count < 1:
			abort(404)
		return jsonify({"result": True})

api = Api(app)
api.add_resource(UserListAPI, '/users', endpoint='users')
api.add_resource(UserAPI, '/users/<userID>', endpoint='user')

if __name__ == '__main__':
	app.run(debug=True)
