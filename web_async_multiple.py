import aiohttp
import aiofiles
import sys
import asyncio
import time

DL_FILE = "/tmp/web_"

async def write_content(content:str, file:str):
    try:
        async with aiofiles.open(file, mode="w") as out:
            await out.write(content.decode())
            await out.flush()
    except Exception as e:
        print(f"Erreur lors de l'écriture dans le fichier {file}: {e}")

async def get_content(url:str):
    print(f"✓ {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp = await resp.read()
            return resp

async def process_url(url, dl_file):
    content = await get_content(url)
    await write_content(content, dl_file)

async def main():
    argv = sys.argv[1:]
    if len(argv)==0:
        print("Usage: python web_async_multiple.py <URL's file>")
    else:
        urls_file = argv[0]
        tasks = []
        with open(urls_file, "r", encoding="utf-8") as file:
            urls = file.readlines()
            for url in urls:
                url = url.split("\n")[0]
                url_formatted = url.split("://")[1]
                urlFile = DL_FILE+url_formatted

                tasks.append(process_url(url, urlFile))
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())