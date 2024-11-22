import time 

def sleep_and_print():
  count = 1
  while count <= 10:
    print(count)
    time.sleep(0.5) 
    count += 1

sleep_and_print()