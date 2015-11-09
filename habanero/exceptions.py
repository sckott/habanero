class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class RequestError(Error):
    """
    Exception raised for request errors.
    """

    @property
    def status_code(self):
        """
        The HTTP status code of the response that precipitated the error or
        ``'N/A'`` if not applicable.
        """
        return self.args[0]

    @property
    def error(self):
        """ A string error message. """
        return self.args[1]

    def __str__(self):
      return 'RequestError(%s) caused by "%s"' % (
        self.status_code, self.error)

