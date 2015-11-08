from setuptools import setup
from setuptools import find_packages

setup(
	name             = 'habanero',
	version          = '0.0.4.9000',
	description      = 'Low Level Client for Crossref Search API',
  author           = 'Scott Chamberlain',
  author_email     = 'myrmecocystus@gmail.com',
  url              = 'https://github.com/sckott/habanero',
  packages         = find_packages(exclude=['test-*']),
  install_requires = ['requests>=2.7.0']
)
