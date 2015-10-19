class Response(object):
  '''
  Habanero: habanero response class
  '''
  def __init__(self, result):
    self.result = result

  def status(self):
    return self.result['status']

  def message_type(self):
    return self.result['message-type']

  def message_version(self):
    return self.result['message-version']

  def message(self):
    return self.result['message']

  def total_results(self):
      return self.result['message']['total-results']

  def items_per_page(self):
      return self.result['message']['items-per-page']

  def query(self):
      return self.result['message']['query']

  def items(self):
      return self.result['message']['items']
