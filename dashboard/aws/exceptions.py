class DynamoTableIndexError(Exception):
    def __init__(self, msg=None) -> None:
        self.msg = (
            'Dynamo Error occurred while '
            'waiting for secondary indexes to load'
        )
        self.msg = f"{self.msg} - {msg}" if msg else self.msg
    def __str__(self):
        return self.msg