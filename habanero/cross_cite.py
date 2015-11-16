import requests

crossciteurl = "http://crosscite.org/citeproc/format"

def ccite(doi, style, locale, **kwargs):
  '''
  Crosscite helper

  Usage::
    ccite("10.5284/1011335")
  '''
  args = {"doi": doi, "style": style, "locale": locale}
  tt = requests.get(crossciteurl, params = args, **kwargs)
  tt.raise_for_status()
  return tt.content
