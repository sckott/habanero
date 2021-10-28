class NoWorks(object):
    """
    Habanero: agency class
    """

    def __init__(self, result):
        self.result = result

    def status(self):
        return self.result["status"]

    def message_type(self):
        return self.result["message-type"]

    def message_version(self):
        return self.result["message-version"]

    def message(self):
        return self.result["message"]
