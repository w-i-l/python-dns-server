class DNSNoDomainFoundError(Exception):
    '''
    Exception raised when the domain is not found in the zone
    '''
    def __init__(self, domain: str):
        self.domain = domain
        self.message = f"Domain {domain} not found in the zone"
        super().__init__(self.message)

class DNSServerError(Exception):
    '''
    Exception raised when the server encounters an error
    '''
    def __init__(self, message: str = "Server error"):
        self.message = message
        super().__init__(self.message)

class DNSFormatError(Exception):
    '''
    Exception raised when the DNS packet format is invalid
    '''
    def __init__(self, message: str = "Invalid DNS packet format"):
        self.message = message
        super().__init__(self.message)