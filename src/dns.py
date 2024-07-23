import socket
from dns_header import DNSHeader
from dns_packet import DNSPacket
from dns_answear import DNSAnswear
from dns_enums import DNSHeaderResponseCode, DNSHeaderRecursionDesired
from datetime import datetime

LOOPBACK_IP = '127.0.0.1'
GOOGLE_DNS_IP = '8.8.8.8'
DNS_PORT = 53

def redirect_to_google(query: bytes) -> tuple[bytes, DNSHeaderResponseCode]:
    '''
    Redirects the query to google and returns the response data and response code
    '''

    google_connection = socket.socket(
        socket.AF_INET, # IPv4 
        socket.SOCK_DGRAM # UDP
    )

    # send the original query to google
    google_connection.sendto(query, (GOOGLE_DNS_IP, DNS_PORT))
    
    google_data, _ = google_connection.recvfrom(1024)
    google_connection.close()

    # get the response code from the google response
    dns_header = DNSHeader(google_data)
    response_code = dns_header.flags.rcode

    return google_data, response_code


def main():
    connection = socket.socket(
        socket.AF_INET, # IPv4 
        socket.SOCK_DGRAM # UDP
    )

    connection.bind((LOOPBACK_IP, DNS_PORT))

    DNSAnswear.load_zones()

    while True:
        print("--------------------")
        data, address = connection.recvfrom(1024) # buffer size

        curent_date = datetime.strftime(datetime.now(), "%d-%m-%Y %H:%M:%S")
        packet = DNSPacket(data)
        print(f"[{curent_date}] Received request for \"{packet.question.domain}\"")
        
        response_data, response_code = packet.build_response()

        curent_date = datetime.strftime(datetime.now(), "%d-%m-%Y %H:%M:%S")

        # redirect to google if the domain is not found
        # and recursion is desired
        if response_code == DNSHeaderResponseCode.NAME_ERROR and packet.header.flags.rd == DNSHeaderRecursionDesired.RECURSION:
            print(f"[{curent_date}] Redirecting to Google")

            response_data, response_code = redirect_to_google(data)
            # send the response back to the client
            connection.sendto(response_data, address)

            print(f"[{curent_date}] Responded from Google with {response_code.name} for \"{packet.question.domain}\"")
            continue

        print(f"[{curent_date}] Responded with {response_code.name} for \"{packet.question.domain}\"")
        connection.sendto(response_data, address)


if __name__ == "__main__":
    main()
