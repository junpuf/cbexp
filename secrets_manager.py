import boto3


class SecretsManager(object):
    """
    Methods to handle interacting with aws codebuild
    """

    def __init__(self):
        self.client = boto3.client("secretsmanager")

    def get_secret_value(self, secret_id):
        """
        get secret value
        Args:
            secret_id
        Return:
            str
        """
        try:
            response = self.client.get_secret_value(SecretId=secret_id)
        except:
            raise
        return response["SecretString"]