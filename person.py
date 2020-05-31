import asyncio


class Person:
    """
    This is where the client communicates with the server
    """
    @staticmethod
    async def speak_with_server(message, loop):
        """
        This is where information is exchanged with the server
        """
        ip = "127.0.0.1"
        port = 53
        reader, writer = await asyncio.open_connection(
            ip, port, loop=loop)
        writer.write(bytes(message, encoding='utf-8'))
        data = await reader.read(1024)
        text = data.decode()
        print(text)
        return(text)

    @staticmethod
    def person(message):
        """
        This is client
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(Person.speak_with_server(
            message, loop))


if __name__ == "__main__":
    message = input()
    Person.person(message)
