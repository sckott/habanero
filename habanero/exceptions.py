class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class RequestError(Error):
    """
    Exception raised for request errors.

    This error occurrs when a request sent to the Crossref API
    results in an error. We give back:

    - HTTP status code
    - Error message
    """

    @property
    def status_code(self):
        return self.args[0]

    @property
    def error(self):
        return self.args[1]

    def __str__(self):
        return '(%s) caused by "%s"' % (self.status_code, self.error)


# url = "http://api.crossref.org/works?rows=fart"
# url = "http://api.crossref.org/funders?filter=from-pub-date%3A2014-03-03"
# foobar(url)
# def foobar(x):
#     try:
#         r = requests.get(x)
#         r.raise_for_status()
#     except requests.exceptions.HTTPError:
#         raise RequestError(r.status_code, r.json()['message'][0]['message'])
#     except requests.exceptions.RequestException as e:
#         print e
