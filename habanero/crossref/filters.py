works_filter_details = {
    "has_funder": {
        "possible_values": None,
        "description": "metadata which includes one or more funder entry",
    },
    "funder": {
        "possible_values": "{funder_id}",
        "description": "metadata which include the {funder_id} in FundRef data",
    },
    "location": {
        "possible_values": "{country_name}",
        "description": "funder records where location = {country name}. Only works on /funders route",
    },
    "prefix": {
        "possible_values": "{owner_prefix}",
        "description": "metadata belonging to a DOI owner prefix {owner_prefix} (e.g. '10.1016' )",
    },
    "member": {
        "possible_values": "{member_id}",
        "description": "metadata belonging to a CrossRef member",
    },
    "from_index_date": {
        "possible_values": "{date}",
        "description": "metadata indexed since (inclusive) {date}",
    },
    "until_index_date": {
        "possible_values": "{date}",
        "description": "metadata indexed before (inclusive) {date}",
    },
    "from_deposit_date": {
        "possible_values": "{date}",
        "description": "metadata last (re)deposited since (inclusive) {date}",
    },
    "until_deposit_date": {
        "possible_values": "{date}",
        "description": "metadata last (re)deposited before (inclusive) {date}",
    },
    "from_update_date": {
        "possible_values": "{date}",
        "description": "Metadata updated since (inclusive) {date} Currently the same as 'from_deposit_date'",
    },
    "until_update_date": {
        "possible_values": "{date}",
        "description": "Metadata updated before (inclusive) {date} Currently the same as 'until_deposit_date'",
    },
    "from_created_date": {
        "possible_values": "{date}",
        "description": "metadata first deposited since (inclusive) {date}",
    },
    "until_created_date": {
        "possible_values": "{date}",
        "description": "metadata first deposited before (inclusive) {date}",
    },
    "from_pub_date": {
        "possible_values": "{date}",
        "description": "metadata where published date is since (inclusive) {date}",
    },
    "until_pub_date": {
        "possible_values": "{date}",
        "description": "metadata where published date is before (inclusive)  {date}",
    },
    "from_online_pub_date": {
        "possible_values": "{date}",
        "description": "metadata where online published date is since (inclusive) {date}",
    },
    "until_online_pub_date": {
        "possible_values": "{date}",
        "description": "metadata where online published date is before (inclusive) {date}",
    },
    "from_print_pub_date": {
        "possible_values": "{date}",
        "description": "metadata where print published date is since (inclusive) {date}",
    },
    "until_print_pub_date": {
        "possible_values": "{date}",
        "description": "metadata where print published date is before (inclusive) {date}",
    },
    "from_posted_date": {
        "possible_values": "{date}",
        "description": "metadata where posted date is since (inclusive) {date}",
    },
    "until_posted_date": {
        "possible_values": "{date}",
        "description": "metadata where posted date is before (inclusive) {date}",
    },
    "from_accepted_date": {
        "possible_values": "{date}",
        "description": "metadata where accepted date is since (inclusive) {date}",
    },
    "until_accepted_date": {
        "possible_values": "{date}",
        "description": "metadata where accepted date is before (inclusive) {date}",
    },
    "has_license": {
        "possible_values": None,
        "description": "metadata that includes any '<license_ref>' elements",
    },
    "license_url": {
        "possible_values": "{url}",
        "description": "metadata where '<license_ref>' value equals {url}",
    },
    "license_version": {
        "possible_values": "{string}",
        "description": "metadata where the '<license_ref>''s 'applies_to' attribute  is '{string}'",
    },
    "license_delay": {
        "possible_values": "{integer}",
        "description": "metadata where difference between publication date and the '<license_ref>''s 'start_date' attribute is <= '{integer}' (in days",
    },
    "has_full_text": {
        "possible_values": None,
        "description": "metadata that includes any full text '<resource>' elements_",
    },
    "full_text_version": {
        "possible_values": "{string}",
        "description": "metadata where '<resource>' element's 'content_version' attribute is '{string}'",
    },
    "full_text_type": {
        "possible_values": "{mime_type}",
        "description": "metadata where '<resource>' element's 'content_type' attribute is '{mime_type}' (e.g. 'application/pdf')",
    },
    "full_text_application": {
        "possible_values": "{string}",
        "description": "metadata where <resource> link has one of the following intended applications: text-mining, similarity-checking or unspecified",
    },
    "has_references": {
        "possible_values": None,
        "description": "metadata for works that have a list of references",
    },
    "has_archive": {
        "possible_values": None,
        "description": "metadata which include name of archive partner",
    },
    "archive": {
        "possible_values": "{string}",
        "description": "metadata which where value of archive partner is '{string}'",
    },
    "has_orcid": {
        "possible_values": None,
        "description": "metadata which includes one or more ORCIDs",
    },
    "has_authenticated_orcid": {
        "possible_values": None,
        "description": "metadata which includes one or more ORCIDs where the depositing publisher claims to have witness the ORCID owner authenticate with ORCID",
    },
    "orcid": {
        "possible_values": "{orcid}",
        "description": "metadata where '<orcid>' element's value = '{orcid}'",
    },
    "issn": {
        "possible_values": "{issn}",
        "description": "metadata where record has an ISSN = '{issn}' Format is 'xxxx_xxxx'.",
    },
    "type": {
        "possible_values": "{type}",
        "description": "metadata records whose type = '{type}' Type must be an ID value from the list of types returned by the '/types' resource",
    },
    "directory": {
        "possible_values": "{directory}",
        "description": "metadata records whose article or serial are mentioned in the given '{directory}'. Currently the only supported value is 'doaj'",
    },
    "doi": {
        "possible_values": "{doi}",
        "description": "metadata describing the DOI '{doi}'",
    },
    "updates": {
        "possible_values": "{doi}",
        "description": "metadata for records that represent editorial updates to the DOI '{doi}'",
    },
    "is_update": {
        "possible_values": None,
        "description": "metadata for records that represent editorial updates",
    },
    "has_update_policy": {
        "possible_values": None,
        "description": "metadata for records that include a link to an editorial update policy",
    },
    "container_title": {
        "possible_values": None,
        "description": "metadata for records with a publication title exactly with an exact match",
    },
    "category_name": {
        "possible_values": None,
        "description": "metadata for records with an exact matching category label",
    },
    "type": {
        "possible_values": None,
        "description": "metadata for records with type matching a type identifier (e.g. journal-article)",
    },
    "type_name": {
        "possible_values": None,
        "description": "metadata for records with an exacty matching type label",
    },
    "award_number": {
        "possible_values": "{award_number}",
        "description": "metadata for records with a matching award nunber_ Optionally combine with 'award_funder'",
    },
    "award_funder": {
        "possible_values": "{funder doi or id}",
        "description": "metadata for records with an award with matching funder. Optionally combine with 'award_number'",
    },
    "has_assertion": {
        "possible_values": None,
        "description": "metadata for records with any assertions",
    },
    "assertion_group": {
        "possible_values": None,
        "description": "metadata for records with an assertion in a particular group",
    },
    "assertion": {
        "possible_values": None,
        "description": "metadata for records with a particular named assertion",
    },
    "has_affiliation": {
        "possible_values": None,
        "description": "metadata for records that have any affiliation information",
    },
    "alternative_id": {
        "possible_values": None,
        "description": "metadata for records with the given alternative ID, which may be a publisher_specific ID, or any other identifier a publisher may have provided",
    },
    "article_number": {
        "possible_values": None,
        "description": "metadata for records with a given article number",
    },
    "has_abstract": {
        "possible_values": None,
        "description": "metadata for records which include an abstract",
    },
    "has_clinical_trial_number": {
        "possible_values": None,
        "description": "metadata for records which include a clinical trial number",
    },
    "content_domain": {
        "possible_values": None,
        "description": "metadata where the publisher records a particular domain name as the location Crossmark content will appear",
    },
    "has_content_domain": {
        "possible_values": None,
        "description": "metadata where the publisher records a domain name location for Crossmark content",
    },
    "has_crossmark_restriction": {
        "possible_values": None,
        "description": "metadata where the publisher restricts Crossmark usage to content domains",
    },
    "has_relation": {
        "possible_values": None,
        "description": "metadata for records that either assert or are the object of a relation",
    },
    "relation_type": {
        "possible_values": None,
        "description": "One of the relation types from the Crossref relations schema (e.g. is-referenced-by, is-parent-of, is-preprint-of)",
    },
    "relation_object": {
        "possible_values": None,
        "description": "Relations where the object identifier matches the identifier provided",
    },
    "relation_object_type": {
        "possible_values": None,
        "description": "One of the identifier types from the Crossref relations schema (e.g. doi, issn)",
    },
    "public_references": {
        "possible_values": None,
        "description": "metadata where publishers allow references to be distributed publically",
    },
    "publisher_name": {
        "possible_values": None,
        "description": "metadata for records with an exact matching publisher name",
    },
    "affiliation": {
        "possible_values": None,
        "description": "metadata for records with at least one contributor with the given affiliation",
    },
}

members_filter_details = {
    "has_public_references": {
        "possible_values": None,
        "description": "member has made their references public for one or more of their prefixes",
    },
    "reference_visibility": {
        "possible_values": ["open", "limited", "closed"],
        "description": "members who have made their references either open, limited (to Metadata Plus subscribers) or closed",
    },
    "backfile_doi_count": {
        "possible_values": "{integer}",
        "description": "count of DOIs for material published more than two years ago",
    },
    "current_doi_count": {
        "possible_values": "{integer}",
        "description": "count of DOIs for material published within last two years",
    },
}

funders_filter_details = {
    "location": {
        "possible_values": None,
        "description": "funders located in specified country",
    }
}
