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
        tm2 = timedelta(seconds=int(seconds))
        new_time = tm1 + tm2
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
    def decoding_ns_string(str, ns):
        bin = binascii.unhexlify(bytes(str[:-2], encoding = 'utf-8')).__str__()
        list_ns = bin.split("\\x")
        for el in list_ns[1:]:
            nel = el[2:]
            if nel != "'":
                ns += nel + "."
        return ns

    @staticmethod
    def processing_received_message_for_ns(message):
        strings = message.split("c00c")
        count_answer = int(strings[0][15])
        ip = ""
        ttl = 10000000000000000000000000
        for i in range(1, count_answer + 1):
            ns = ""
            ttl_new = int(strings[i][12:16], 16)
            str = strings[i][20:]
            link = str[-2:]
            e = str[:-2]
            ns = SendGet.decoding_ns_string(str, ns)
            if link != "00":
                str_link = message[int(link, 16) * 2:]
                list_n = str_link.split("c00c")
                str_link = list_n[0]
                ns = SendGet.decoding_ns_string(str_link, ns)
            while ns[-1] == "." or ns[-1] == "'":
                ns = ns[:-1]
            ip += ns + " "
            if ttl_new < ttl:
                ttl = ttl_new
        return ip, ttl.__str__()

    @staticmethod
    def create_message(messages, type):
        new = "AAAA01000001000000000000"
        mess = messages.split('.')
        for message in mess:
            count = hex(message.__len__())[2:]
            if count.__len__() < 2:
                count = "0" + count
            new += count
            for letter in message:
                new += hex(ord(letter))[2:]
        new += "0000010001" if type == "A" else "0000020001"
        return(new)

    @staticmethod
    def send_get(messages):
        list_messages = messages.split(" ")
        type, mess = list_messages[0], list_messages[1]
        message = SendGet.create_message(mess, type)
        get_message = SendGet.send_get_message(message, "8.8.8.8", 53)
        if type == "A":
            ip, ttl = SendGet.processing_received_message(get_message)
        else:
            ip, ttl = SendGet.processing_received_message_for_ns(get_message)
        removal_time = SendGet.removal_time_counting(ttl)
        return ip, removal_time


if __name__ == "__main__":
    message = input()
    print(SendGet.send_get(message))

