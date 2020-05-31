import asyncio
import dns
import hashing


class Server:
    def __init__(self, test, ip, port):
        self.test = test
        self.loop = asyncio.get_event_loop()
        self.server = asyncio.start_server(self.handle_connection,
                                           ip, port, loop=self.loop)
        self.cl_hash = hashing.Hash()
        print(self.cl_hash.time)

    async def handle_connection(self, reader, writer):
        """
        This is where the server processes the received message
        """
        import time
        from datetime import timedelta
        data = await reader.read(1024)
        message = data.decode()
        address = writer.get_extra_info("peername")
        if message != "stop":
            if self.cl_hash.contains_name(message):
                ip = self.cl_hash.get_elements(message)
                print("get")
            else:
                ip, removal_time = dns.SendGet.send_get(message)
                self.cl_hash.add_item(message, ip, removal_time)
                print("create")
            writer.write(bytes(ip, encoding='utf-8'))
            print(self.cl_hash.dict, self.cl_hash.time)
            writer.close()
        else:
            self.test = True
            self.cl_hash.save_disk()
        if self.test:
            self.loop.stop()

    def my_server(self):
        """
            This is server
        """
        self.server = self.loop.run_until_complete(self.server)
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            print("what?")
        self.server.close()
        self.loop.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


if __name__ == '__main__':
    ip = "127.0.0.1"
    port = 53
    my_good_server = Server(False, ip, port)
    my_good_server.my_server()
