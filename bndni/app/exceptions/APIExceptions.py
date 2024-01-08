

class APIDecodeError(Exception):
    """"""

    def __init__(self, message):
        self.message = message
        pass

    def __str__(self) -> str:
        return f'Error Loading Environment at {self.args} with {self.message}'
    pass

class APIKeyError(Exception):
    """"""

    def __init__(self, message):
        self.message = message
        pass

    def __str__(self) -> str:
        return f'Error Loading Environment at {self.args} with {self.message}'
    pass


class APISecretError(Exception):
    """API Secret is not loaded in the Enviornment"""

    def __init__(self, message):
        self.message = message
        pass

    def __str__(self) -> str:
        return f'Error Loading Environment at {self.args} with {self.message}'


class APIPassphraseError(Exception):
    """API Passphrase is not loaded in the Environment"""

    def __init__(self, message):
        self.message = message
        pass

    def __str__(self) -> str:
        return f'Error Loading Environment at {self.args} with {self.message}'



