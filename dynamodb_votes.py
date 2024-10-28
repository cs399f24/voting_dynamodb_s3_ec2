import boto3


class DynamoDBVotes:

    def __init__(self, redis):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('VoteCounts')

    def is_valid_vote(self, vote):
        return vote in ['yes', 'no']

    def register_vote(self, vote):
        if self.is_valid_vote(vote):

            self.table.update_item(
                Key={'VoteType': vote},
                UpdateExpression="SET #C = if_not_exists(#C, :start) + :inc",
                ExpressionAttributeNames={'#C': 'Count'},
                ExpressionAttributeValues={':inc': 1, ':start': 0}
            )

    def get_votes(self):
        response = self.table.batch_get_item(
            RequestItems={
                'VoteCounts': {
                    'Keys': [{'VoteType': 'yes'}, {'VoteType': 'no'}]
                }
            }
        )

        counts = {'yes': 0, 'no': 0}
        for item in response['Responses']['VoteCounts']:
            counts[item['VoteType']] = item['Count']

        return counts
