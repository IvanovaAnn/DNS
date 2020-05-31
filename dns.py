import binascii
import socket
import time
from datetime import timedelta


class SendGet:
    @staticmethod
    def send_get_message(message, address, port):
        """
        send and get udp message to UDP server
        """
        server_address = (address, port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(binascii.unhexlify(message), server_address)
            data, _ = sock.recvfrom(4096)
        finally:
            sock.close()
        return binascii.hexlify(data).decode("utf-8")

    @staticmethod
    def removal_time_counting(seconds):
        real_time = time.strftime("%D.%H.%M.%S", time.localtime())
        tm1 = timedelta(days=int(real_time[3:5]), hours=int(real_time[9:11]),
                        minutes=int(real_time[12:14]),
                        seconds=int(real_time[15:17]))
        #print(tm1.__str__())
        tm2 = timedelta(seconds=int(seconds))
        new_time = tm1 + tm2
        #print(new_time)
        return new_time.__str__()

    @staticmethod
    def processing_received_message(message):
        ip = int(message[-8:-6], 16).__str__() + "." +\
             int(message[-6:-4], 16).__str__() + "." +\
             int(message[-4:-2], 16).__str__() + "." +\
             int(message[-2:], 16).__str__()
        ttl = int(message[-20:-12], 16).__str__()
        return ip, ttl

    @staticmethod
    def create_message(messages):
        new = "AAAA01000001000000000000"
        mess = messages.split('.')
        for message in mess:
            count = hex(message.__len__())[2:]
            if count.__len__() < 2:
                count = "0" + count
            new += count
            for letter in message:
                new += hex(ord(letter))[2:]
        new += "0000010001"
        return(new)

    @staticmethod
    def send_get(messages):
        message = SendGet.create_message(messages)
        get_message = SendGet.send_get_message(message, "8.8.8.8", 53)
        ip, ttl = SendGet.processing_received_message(get_message)
        removal_time = SendGet.removal_time_counting(ttl)
        return ip, removal_time


if __name__ == "__main__":
    #message = input()
    message = "example.com"
    print(SendGet.send_get(message))
