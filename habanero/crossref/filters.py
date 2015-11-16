# def names():
#   '''
#   Crossref filter names

#   :return: list

#   Usage:
#   >>> from habanero import filters
#   >>> filters.names
#   '''
#   return filter_list

# def details():
#   '''
#   Crossref filters details

#   :return: list

#   Usage:
#   >>> from habanero import filters
#   >>> filters.filters
#   >>> filters.filters['has_funder']
#   >>> filters.filters['has_funder']['description']
#   '''
#   return filter_details

filter_names = [
  'has_funder','funder','prefix','member','from_index_date','until_index_date',
  'from_deposit_date','until_deposit_date','from_update_date','until_update_date',
  'from_first_deposit_date','until_first_deposit_date','from_pub_date','until_pub_date',
  'has_license','license_url','license_version','license_delay','has_full_text',
  'full_text_version','full_text_type','public_references','has_references','has_archive',
  'archive','has_orcid','orcid','issn','type','directory','doi','updates','is_update',
  'has_update_policy','container_title','publisher_name','category_name','type_name',
  'from_created_date', 'until_created_date', 'affiliation', 'has_affiliation',
  'assertion_group', 'assertion', 'article_number', 'alternative_id'
]

filter_details = {
  "has_funder": { "possible_values": None, "description": "metadata which includes one or more funder entry" },
  "funder": { "possible_values": "{funder_id}", "description": "metadata which include the {funder_id} in FundRef data" },
  "prefix": { "possible_values": "{owner_prefix}", "description": "metadata belonging to a DOI owner prefix {owner_prefix} (e.g. '10.1016' )" },
  "member": { "possible_values": "{member_id}", "description": "metadata belonging to a CrossRef member" },
  "from_index_date": { "possible_values": '{date}', "description": "metadata indexed since (inclusive) {date}" },
  "until_index_date": { "possible_values": '{date}', "description": "metadata indexed before (inclusive) {date}" },
  "from_deposit_date": { "possible_values": '{date}', "description": "metadata last (re)deposited since (inclusive) {date}" },
  "until_deposit_date": { "possible_values": '{date}', "description": "metadata last (re)deposited before (inclusive) {date}" },
  "from_update_date": { "possible_values": '{date}', "description": "Metadata updated since (inclusive) {date} Currently the same as 'from_deposit_date'" },
  "until_update_date": { "possible_values": '{date}', "description": "Metadata updated before (inclusive) {date} Currently the same as 'until_deposit_date'" },
  "from_created_date": { "possible_values": '{date}', "description": "metadata first deposited since (inclusive) {date}" },
  "until_created_date": { "possible_values": '{date}', "description": "metadata first deposited before (inclusive) {date}" },
  "from_pub_date": { "possible_values": '{date}', "description": "metadata where published date is since (inclusive) {date}" },
  "until_pub_date": { "possible_values": '{date}', "description": "metadata where published date is before (inclusive)  {date}" },
  "has_license": { "possible_values": None, "description": "metadata that includes any '<license_ref>' elements" },
  "license_url": { "possible_values": '{url}', "description": "metadata where '<license_ref>' value equals {url}" },
  "license_version": { "possible_values": '{string}', "description": "metadata where the '<license_ref>''s 'applies_to' attribute  is '{string}'"},
  "license_delay": { "possible_values": "{integer}", "description": "metadata where difference between publication date and the '<license_ref>''s 'start_date' attribute is <= '{integer}' (in days"},
  "has_full_text": { "possible_values": None, "description": "metadata that includes any full text '<resource>' elements_" },
  "full_text_version": { "possible_values": '{string}' , "description": "metadata where '<resource>' element's 'content_version' attribute is '{string}'" },
  "full_text_type": { "possible_values": '{mime_type}' , "description": "metadata where '<resource>' element's 'content_type' attribute is '{mime_type}' (e.g. 'application/pdf')" },
  "public_references": { "possible_values": None, "description": "metadata where publishers allow references to be distributed publically" },
  "has_references": { "possible_values": None , "description": "metadata for works that have a list of references" },
  "has_archive": { "possible_values": None , "description": "metadata which include name of archive partner" },
  "archive": { "possible_values": '{string}', "description": "metadata which where value of archive partner is '{string}'" },
  "has_orcid": { "possible_values": None, "description": "metadata which includes one or more ORCIDs" },
  "orcid": { "possible_values": '{orcid}', "description": "metadata where '<orcid>' element's value = '{orcid}'" },
  "issn": { "possible_values": '{issn}', "description": "metadata where record has an ISSN = '{issn}' Format is 'xxxx_xxxx'." },
  "type": { "possible_values": '{type}', "description": "metadata records whose type = '{type}' Type must be an ID value from the list of types returned by the '/types' resource" },
  "directory": { "possible_values": "{directory}", "description": "metadata records whose article or serial are mentioned in the given '{directory}'. Currently the only supported value is 'doaj'" },
  "doi": { "possible_values": '{doi}', "description": "metadata describing the DOI '{doi}'" },
  "updates": { "possible_values": '{doi}', "description": "metadata for records that represent editorial updates to the DOI '{doi}'" },
  "is_update": { "possible_values": None, "description": "metadata for records that represent editorial updates" },
  "has_update_policy": { "possible_values": None, "description": "metadata for records that include a link to an editorial update policy" },
  "container_title": { "possible_values": None, "description": "metadata for records with a publication title exactly with an exact match" },
  "publisher_name": { "possible_values": None, "description": "metadata for records with an exact matching publisher name" },
  "category_name": { "possible_values": None, "description": "metadata for records with an exact matching category label" },
  "type_name": { "possible_values": None, "description": "metadata for records with an exacty matching type label" },
  "award_number": { "possible_values": "{award_number}", "description": "metadata for records with a matching award nunber_ Optionally combine with 'award_funder'" },
  "award_funder": { "possible_values": '{funder doi or id}', "description": "metadata for records with an award with matching funder. Optionally combine with 'award_number'" },
  "assertion_group": { "possible_values": None, "description": "metadata for records with an assertion in a particular group" },
  "assertion": { "possible_values": None, "description": "metadata for records with a particular named assertion" },
  "affiliation": { "possible_values": None, "description": "metadata for records with at least one contributor with the given affiliation" },
  "has_affiliation": { "possible_values": None, "description": "metadata for records that have any affiliation information" },
  "alternative_id": { "possible_values": None, "description": "metadata for records with the given alternative ID, which may be a publisher_specific ID, or any other identifier a publisher may have provided" },
  "article_number": { "possible_values": None, "description": "metadata for records with a given article number" }
}
