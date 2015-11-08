habanero
=======

[![Build Status](https://travis-ci.org/sckott/habanero.svg)](https://travis-ci.org/sckott/habanero)
[![Coverage Status](https://coveralls.io/repos/sckott/habanero/badge.svg?branch=master&service=github)](https://coveralls.io/github/sckott/habanero?branch=master)

This is a low level client for working with Crossref's search API. It's been named to be more generic, as other organizations are/will adopt Crossref's search API, making it possible to ineract with all from one client. 

Crossref API docs: [https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md](https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md)

Other Crossref API clients:

- Ruby: [serrano](https://github.com/sckott/serrano)
- R: [rcrossref](https://github.com/ropensci/rcrossref)

`habanero` includes methods matching Crossref API routes:

- `/works`
- `/members`
- `/prefixes`
- `/funders`
- `/journals`
- `/types`
- `/licenses`

Other methods

- `agency` - get DOI minting agency
- `content_negotiation` - get citations in a variety of formats

### Installation

```
sudo pip install git+git://github.com/sckott/habanero.git#egg=habanero
```

OR 

```
git clone git@github.com:sckott/habanero.git
cd habanero
make install
```

### Usage

Initialize

```python
from habanero import Habanero
hb = Habanero()
```

Works route

```python
x = hb.works(query = "ecology")
x.status()
x.message()
x.total_results()
x.items()
```

Members route

```python
hb.members(ids = 98, works = True)
```

###Meta

* Please note that this project is released with a [Contributor Code of Conduct](CONDUCT.md). By participating in this project you agree to abide by its terms.
* License: MIT; see [LICENSE](LICENSE) for details
