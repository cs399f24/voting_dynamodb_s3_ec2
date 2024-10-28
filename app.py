
from flask import Flask, jsonify, request
import json
from dynamodb_votes import DynamoDBVotes
from flask_cors import CORS
import redis
import dotenv
import os


def create_app(votes):

    app = Flask(__name__)
    CORS(app)

    @app.route('/results')
    def results():
        return jsonify(votes.get_votes())

    @app.route('/vote', methods=['POST'])
    def vote():
        data = json.loads(request.data)

        if 'vote' not in data:
            return 'Invalid body', 400

        the_vote = data['vote']

        if not votes.is_valid_vote(the_vote):
            return 'Invalid vote', 400

        votes.register_vote(the_vote)

        return jsonify(votes.get_votes())

    return app


def launch_app():
    dotenv.load_dotenv()
    redis_server = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))
    votes = DynamoDBVotes(redis_server)

    return create_app(votes)


if __name__ == '__main__':
    app = launch_app()
    app.run(port=80, debug=True)
