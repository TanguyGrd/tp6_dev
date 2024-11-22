import time 
import asyncio

async def sleep_and_print():
  count = 1
  while count <= 10:
    print(count)
    await asyncio.sleep(0.5) 
    count += 1
    
async def sleep_and_print1():
  count1= 10
  while count1 >= 1:
    print(count1)
    await asyncio.sleep(0.5)
    count1 -=1
    
async def main():
  
  await asyncio.gather(sleep_and_print(), sleep_and_print1())

asyncio.run(main()) 