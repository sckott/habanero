import re


def filter_handler(x=None):
    if x.__class__.__name__ == "NoneType":
        return None
    else:
        # lowercase bools
        for k, v in x.items():
            if v.__class__ == bool:
                x[k] = str(v).lower()

        # combine
        nn = x.keys()
        if any([i in others for i in nn]):
            out = []
            for i in nn:
                if i in others:
                    out.append(switch_filters(i))
                else:
                    out.append(i)
            nn = out

        newnn = [re.sub("_", "-", z) for z in nn]
        newnnd = dict(zip(x.keys(), newnn))
        x = rename_keys(x, newnnd)

        # split any lists into duplicated key/filter names
        newx = []
        for k, v in x.items():
            if v.__class__ == list:
                for a, b in enumerate(v):
                    newx.append(":".join([k, b]))
            else:
                newx.append(":".join([k, v]))

        newx = ",".join(newx)
        return newx


others = [
    "license_url",
    "license_version",
    "license_delay",
    "full_text_version",
    "full_text_type",
    "full_text_application",
    "award_number",
    "award_funder",
]

dict_filts = {
    "license_url": "license.url",
    "license_version": "license.version",
    "license_delay": "license.delay",
    "full_text_version": "full-text.version",
    "full_text_type": "full-text.type",
    "award_number": "award.number",
    "award_funder": "award.funder",
    "relation_type": "relation.type",
    "relation_object": "relation.object",
    "relation_object_type": "relation.object-type",
}


def switch_filters(x):
    return switch(x, dict_filts)


def switch(x, dict):
    return dict[x]


# https://github.com/healthsites/healthsites/blob/3b10b12f004bfa783ee3121647ff9856836717f3/django_project/api/utils.py
def rename_keys(old_dict, transform):
    new_dict = {}
    for k, v in old_dict.items():
        if k in transform:
            new_dict.update({transform[k]: v})
        else:
            new_dict.update({k: v})
    return new_dict
