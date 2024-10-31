class NoModelException(Exception):
    def __init__(self):
        self.message = "No Model in Model Registry"
        super().__init__(self.message)

class ParserError(Exception):
    def __init__(self, info):
        super().__init__(info)
        
class ImpossibleIntegration(Exception):
    def __init__(self, info):
        super().__init__(info)