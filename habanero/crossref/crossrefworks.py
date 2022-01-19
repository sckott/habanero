class CrossrefWorks(object):
    """
    CrossrefWorks Class

    Usage::
            from habanero import Crossref, CrossrefWorks
            cr = Crossref()

            res = cr.works(ids=['10.1136/jclinpath-2020-206745', '10.1136/esmoopen-2020-000776'])
            x = CrossrefWorks(res)
            x
            x.works
            x.doi
            x.license
            x.title
            x.abstract

            res2 = cr.works(limit = 2)
            x = CrossrefWorks(res2)
            x
            x.works
            x.doi
            x.license
            x.title
            x.abstract

            res3 = cr.members(ids = 98, works = True, limit = 5)
            x = CrossrefWorks(res3)
            x
            x.works
            x.doi
            x.license
            x.title
            x.abstract
    """

    def __init__(self, input):
        super(CrossrefWorks, self).__init__()
        self.__input = input
        self.works = self.works_handler(self.__input)
        keys = list(self.works[0].keys())
        for key in keys:
            values = [work.get(key, None) for work in self.works]
            setattr(self, key.lower().replace("-", "_"), values)

    def __repr__(self):
        return """<%s: No. works: %s>""" % (
            type(self).__name__,
            len(self.works),
        )

    def works_handler(self, x):
        singletons = [
            "work",
            "member",
            "prefix",
            "funder",
        ]
        lists = [w + "-list" for w in singletons]
        if isinstance(x, list):
            return [w["message"] for w in x]
        elif isinstance(x, dict) and x["message-type"] in lists:
            return x["message"]["items"]
        elif isinstance(x, dict) and x["message-type"] in singletons:
            return [x["message"]]
        else:
            raise TypeError(f"can't handle type: {type(x)}")
