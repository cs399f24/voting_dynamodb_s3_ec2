
from flask import Flask, jsonify, request
import json
from dynamodb_votes import DynamoDBVotes
from flask_cors import CORS


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
    votes = DynamoDBVotes()

    return create_app(votes)


if __name__ == '__main__':
    app = launch_app()
    app.run(port=80, debug=True)
