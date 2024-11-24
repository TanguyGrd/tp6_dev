import asyncio

CLIENTS = {}

def send_to_client(writer, message:str, *args:tuple):
    stringFormatted = message.format(*args)
    writer.write(stringFormatted.encode())

async def handle_client_msg(reader, writer):
    global CLIENTS
    while True:
        data = await reader.read(1024)
        addr = writer.get_extra_info('peername')

        # Déco
        if data == b'':
            if addr in CLIENTS.keys():
                pseudoSave = CLIENTS[addr]["pseudo"]
                del CLIENTS[addr]

                message_leave = "Annonce : {} a quitté la chatroom"

                for client in CLIENTS.keys():
                    send_to_client(CLIENTS[client]["w"], message_leave, (pseudoSave))

            break

        message = data.decode()
        print(f"Message received from {addr[0]}:{addr[1]} : {message!r}")

        if not addr in CLIENTS.keys():
            CLIENTS[addr] = {}
            CLIENTS[addr]["r"] = reader
            CLIENTS[addr]["w"] = writer

            if 'Hello|' in message:
                CLIENTS[addr]["pseudo"] = message.split("Hello|")[1]

                message = "Annonce : {} a rejoint la chatroom"

                for client in CLIENTS.keys():
                    send_to_client(CLIENTS[client]["w"], message, (CLIENTS[addr]["pseudo"]))
    
        else:
            message_to_others = "{} a dit : {}"

            for client in CLIENTS.keys():
                if client != addr:
                    send_to_client(CLIENTS[client]["w"], message_to_others, *(CLIENTS[addr]["pseudo"], message))

        await writer.drain()

async def main():
    server = await asyncio.start_server(handle_client_msg, '127.0.0.1', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())