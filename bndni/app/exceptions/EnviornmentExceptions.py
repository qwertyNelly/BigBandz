

class ErrorLoadingEnviornment(Exception):
    """Error while loading the Environment on Application Start"""

    def __init__(self, message):
        self.message = message
        pass

    def __str__(self) -> str:
        return f'Error Loading Enviornment at {self.args} with {self.message}'
