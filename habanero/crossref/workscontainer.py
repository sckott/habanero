class WorksContainer:
    """
    WorksContainer: Class for working with works results

    :rtype: list

    Usage::

            from habanero import Crossref, WorksContainer
            cr = Crossref()

            res = cr.works(ids=['10.1136/jclinpath-2020-206745', '10.1136/esmoopen-2020-000776'])
            x = WorksContainer(res)
            x
            x.works
            x.doi
            x.license
            x.title
            x.abstract

            res2 = cr.works(limit = 2)
            x = WorksContainer(res2)
            x
            x.works
            x.doi
            x.license
            x.title
            x.abstract

            res3 = cr.members(ids = 98, works = True, limit = 5)
            x = WorksContainer(res3)
            x
            x.works
            x.doi
            x.license
            x.title
            x.abstract
    """

    def __init__(self, input) -> None:
        super(WorksContainer, self).__init__()
        if not input:
            raise ValueError("input len must be > zero")
        self.__input = input
        self.works = self.works_handler(self.__input)
        keys = list(self.works[0].keys())
        for key in keys:
            values = [work.get(key, None) for work in self.works]
            setattr(self, key.lower().replace("-", "_"), values)

    def __repr__(self) -> str:
        return """<%s: No. works: %s>""" % (
            type(self).__name__,
            len(self.works),
        )

    def works_handler(self, x: list | dict) -> list:
        message_type = (
            [w["message-type"] for w in x][0]
            if isinstance(x, list)
            else x["message-type"]
        )

        if isinstance(x, list):
            if x[0]["message-type"] == "work":
                x = list(filter(lambda w: w["message-type"] == "work", x))
                return [w["message"] for w in x]
            elif x[0]["message-type"] == "work-list":
                x = list(filter(lambda w: w["message-type"] == "work-list", x))
                items = [w["message"]["items"] for w in x]
                return [z for sublist in items for z in sublist]
            else:
                raise TypeError(
                    f"can only handle Crossref message-type 'work' & 'work-list', got: '{message_type}'"
                )
        elif isinstance(x, dict) and x["message-type"] == "work-list":
            return x["message"]["items"]
        elif isinstance(x, dict) and x["message-type"] == "work":
            return [x["message"]]
        else:
            raise TypeError(
                f"can only handle Crossref message-type 'work' & 'work-list', got: '{message_type}'"
            )
