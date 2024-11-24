# pylint: disable=missing-module-docstring, import-error

import asyncio
import aioconsole

async def receive_responses(reader):
    """
    Used to receive server responses asynchronously
    """
    while True:
        data = await reader.read(1024)
        print("\n",data.decode(), "\n")


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
    pseudo = input("Pseudo: ")

    reader, writer = await asyncio.open_connection(host="127.0.0.1", port=8888)

    writer.write(f"Hello|{pseudo}".encode())

    tasks = [receive_responses(reader), send_data(writer)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())