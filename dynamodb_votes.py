import boto3


class DynamoDBVotes:

    def __init__(self):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
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
        counts = {'yes': 0, 'no': 0}

        response_yes = self.table.get_item(Key={'VoteType': 'yes'})
        if 'Item' in response_yes:
            counts['yes'] = response_yes['Item']['Count']

        response_no = self.table.get_item(Key={'VoteType': 'no'})
        if 'Item' in response_no:
            counts['no'] = response_no['Item']['Count']

        return counts
