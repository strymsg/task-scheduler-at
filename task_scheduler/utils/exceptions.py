class DbErrorHandler(Exception):
    def __init__(self, m):
        self.message = m

class ConfigurationError(Exception):
    def __init__(self, m):
        self.message = m