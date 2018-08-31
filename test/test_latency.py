import time

latency = 0

start_time = time.time()
print('start_time : ', start_time)
time.sleep(1.222)
end_time = time.time()
latency = end_time - start_time
print('end_time : ', end_time)
print('latency : ', latency)