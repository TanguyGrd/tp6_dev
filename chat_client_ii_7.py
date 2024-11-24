# pylint: disable=missing-module-docstring, import-error

import asyncio
import aioconsole
import argparse
import configparser

async def receive_responses(reader):
    """
    Used to receive server responses asynchronously
    """
    while True:
        data = await reader.read(1024)
        if data == b'':
            print("Annonce : Le serveur est hors ligne")
            return

        print(">>> ",data.decode())


async def send_data(writer):
    """
    Used to send data to server asynchronously
    """
    while True:
        message = await aioconsole.ainput()
        msg = message.encode()
        writer.write(msg)
        await writer.drain()


async def main():
    """
    Main function to have async
    """

    parser = argparse.ArgumentParser(
    prog='Chat Client TCP v7',
    description='Connect to Chat TCP server to chat un max avec les potes',
    epilog='Text at the bottom of help')

    parser.add_argument(
        '-a', '--address',
        help='Set TCP host to connect',
        nargs=1,
    )
    parser.add_argument(
        '-p', '--port',
        help='Set TCP port to connect',
        nargs=1,
    )
    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read('server.conf')

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



    pseudo = input("Pseudo: ")

    reader, writer = await asyncio.open_connection(host=HOST, port=PORT)

    writer.write(f"Hello|{pseudo}".encode())

    tasks = [receive_responses(reader), send_data(writer)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())