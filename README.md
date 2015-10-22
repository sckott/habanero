habanero
=======

[![Build Status](https://travis-ci.org/sckott/habanero.svg)](https://travis-ci.org/sckott/habanero)
[![codecov.io](https://codecov.io/github/sckott/habanero/coverage.svg?branch=master)](https://codecov.io/github/sckott/habanero?branch=master)

This is a low level client for working with Crossref's search API. It's been named to be more generic, as other organizations are/will adopt Crossref's search API, making it possible to ineract with all from one client. 

Crossref API docs: [https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md](https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md)

Other Crossref API clients:

- Ruby: [serrano](https://github.com/sckott/serrano)
- R: [rcrossref](https://github.com/ropensci/rcrossref)

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

### License

MIT; see [LICENSE](LICENSE) for details
