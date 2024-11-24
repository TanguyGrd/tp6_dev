# pylint: disable=missing-module-docstring, global-variable-not-assigned, line-too-long

import asyncio

CLIENTS = {}

async def handle_client_msg(reader, writer):
    """
    Used to handle data received from client
    """

    global CLIENTS
    while True:
        data = await reader.read(1024)
        if data == b'':
            break

        addr = writer.get_extra_info('peername')

        message = data.decode()
        print(f"Message received from {addr[0]}:{addr[1]} : {message!r}")

        if not addr in CLIENTS.keys():
            CLIENTS[addr] = {}
            CLIENTS[addr]["r"] = reader
            CLIENTS[addr]["w"] = writer

            if 'Hello|' in message:
                CLIENTS[addr]["pseudo"] = message.split("Hello|")[1]

                for client in CLIENTS.keys():
                    clientData = CLIENTS[client]

                    clientData["w"].write(f"Annonce : {CLIENTS[addr]["pseudo"]} a rejoint la chatroom".encode())

        else:
            for client in CLIENTS.keys():
                if client != addr:
                    clientData = CLIENTS[client]
                    clientData["w"].write(f"{CLIENTS[addr]["pseudo"]} a dit : {message}".encode())

        await writer.drain()

async def main():
    """
    Main function to have async
    """
    server = await asyncio.start_server(handle_client_msg, '127.0.0.1', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())