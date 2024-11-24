import asyncio
import random
import argparse
import configparser
from datetime import datetime

CLIENTS = {}

def generate_random_rgb():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def string_rgb(string:str, rgb:tuple):
    return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{string}\033[0m"

def send_to_client(writer, message:str, *args:tuple):
    current_time = datetime.now()
    formatted_time = current_time.strftime("[%H:%M]")

    stringFormatted = message.format(*args)
    stringFormatted = f"{formatted_time} {stringFormatted}"
    writer.write(stringFormatted.encode())

async def handle_client_msg(reader, writer):
    global CLIENTS
    while True:
        data = await reader.read(1024)
        addr = writer.get_extra_info('peername')

        # Déco
        if data == b'':
            if addr in CLIENTS.keys():
                pseudoColored = string_rgb(CLIENTS[addr]["pseudo"], CLIENTS[addr]["color"])

                del CLIENTS[addr]

                message_leave = "Annonce : {} a quitté la chatroom"

                for client in CLIENTS.keys():
                    send_to_client(CLIENTS[client]["w"], message_leave, (pseudoColored))

            break

        message = data.decode()
        print(f"Message received from {addr[0]}:{addr[1]} : {message!r}")

        if not addr in CLIENTS.keys():
            CLIENTS[addr] = {}
            CLIENTS[addr]["r"] = reader
            CLIENTS[addr]["w"] = writer

            if 'Hello|' in message:
                CLIENTS[addr]["pseudo"] = message.split("Hello|")[1]
                CLIENTS[addr]["color"] = generate_random_rgb()

                pseudoColored = string_rgb(CLIENTS[addr]["pseudo"], CLIENTS[addr]["color"])

                message = "Annonce : {} a rejoint la chatroom"

                for client in CLIENTS.keys():
                    send_to_client(CLIENTS[client]["w"], message, (pseudoColored))
    
        else:
            pseudoColored = string_rgb(CLIENTS[addr]["pseudo"], CLIENTS[addr]["color"])

            message_to_others = "{} a dit : {}"
            message_to_self = "Vous avez dit : {}"

            for client in CLIENTS.keys():
                if client != addr:
                    clientData = CLIENTS[client]

                    send_to_client(CLIENTS[client]["w"], message_to_others, *(pseudoColored, message))
                else:
                    send_to_client(writer, message_to_self, (message))

        await writer.drain()

async def main():
    # === Args and Config ===
    parser = argparse.ArgumentParser(
    prog='Chat Server TCP v7',
    description='Host TCP server to chat un max avec les potes',
    epilog='Text at the bottom of help')

    parser.add_argument(
        '-a', '--address',
        help='Set TCP host to listen',
        nargs=1,
    )
    parser.add_argument(
        '-p', '--port',
        help='Set TCP port to listen',
        nargs=1,
    )
    args = parser.parse_args()
    
    config = configparser.ConfigParser()
    config.read('client.conf')

    HOST = ''
    PORT = ''

    if 'DEFAULT' in config:
        if args.address == None:
            HOST = config['DEFAULT']['Host']
        else:
            HOST = args.address[0]

        if args.port == None:
            PORT = config['DEFAULT']['Port']
        else:
            PORT = args.port[0]



    server = await asyncio.start_server(handle_client_msg, HOST, PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())