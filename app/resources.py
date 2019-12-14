from flask_restful import Resource, reqparse
from app import mongo, mhelp
from app.models.helpers import check_token, check_api_key
from uuid import uuid4
from flask import session, request
import json

def create_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('Api-Key', required=True, location='headers')
    return parser


class Create(Resource):
    def post(self):
        parser = create_parser()
        args = parser.parse_args()
        data = request.get_json()
        if check_api_key(args['Api-Key']):
            pass
        else:
            print('Failed')
            return {"error": "Unauthorized"}, 403
        user = mhelp.get_user({'api_key': args['Api-Key']})
        if user['store_count'] == 3:
            return {"error": "Reached 3 store maximum!"}, 403
        else:
            name = str(uuid4())
            count = user['store_count'] + 1
            mongo.db.stores.insert_one({'name': name, 'owner': user['email'], 'data': data})
            stores = mhelp.get_store_ids({'owner': user['email']})
            mongo.db.free_users.update_one({'email': user['email']}, {'$set': { 'store_count': count, 'stores': stores }})
        return { "message": "Success", "name": name }, 200