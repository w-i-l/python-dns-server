from  dns_header import DNSHeader
from  dns_question import DNSQuestion
from  dns_enums import DNSHeaderResponseCode
from  dns_answear import DNSAnswear
from typing import Self

class DNSPacket:
    '''
    A class representing a DNS packet split into header, question and answears
    '''
    def __init__(self, data: bytes):
        self.data = data
        self.header = DNSHeader(data)
        self.question = DNSQuestion(data[12:])
        self.answears = DNSAnswear(self.question)

    def build_response(self) -> tuple[bytes, DNSHeaderResponseCode]:
        '''
        Builds the response bytes for the packet from the current packet

        Returns the response bytes and the response code
        '''

        response_question_bytes = self.question.as_bytes()
        response_answears, answears_count = self.answears.build_response()
        response_code = DNSHeaderResponseCode.NO_ERROR if isinstance(response_answears, bytes) else response_answears
        authority_bytes = self.answears.get_authority()

        response_header = self.header.build_response_header(
            answers_count=answears_count,
            response_code=response_code,
            authority_count=1 if authority_bytes else 0
        )
        response_header_bytes = response_header.as_bytes()

        response_answears_bytes = response_answears if isinstance(response_answears, bytes) else b''
        authority_bytes = authority_bytes if authority_bytes else b''

        response_bytes = response_header_bytes + response_question_bytes + response_answears_bytes + authority_bytes
        
        return response_bytes, response_code

    def __str__(self) -> str:
        return f"{self.header}\n{self.question}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
