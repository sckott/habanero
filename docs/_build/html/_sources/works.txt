.. _works:

works
=====

Search all works (journal articles, conference proceedings, books, components, etc),
by one or more DOIs, or a query phrase.

Load
-------------

::

    import habanero
    hb = Habanero()


Example Usage
-------------

::

    # Parse output to various data pieces
		x = hb.works(filter = {'has_full_text': True})

		## get doi for each item
		[ z['DOI'] for z in x.result['message']['items'] ]

		## get doi and url for each item
		[ {"doi": z['DOI'], "url": z['URL']} for z in x.result['message']['items'] ]

		### print every doi
		for i in x.result['message']['items']:
		     print i['DOI']

		# filters - pass in as a dict
		## see https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md#filter-names
		hb.works(filter = {'has_full_text': True})

.. automethod:: works
   :members:
