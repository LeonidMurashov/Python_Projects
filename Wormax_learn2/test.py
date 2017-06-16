from grabscreen import grab_screen
import time
import numpy as np

times = []
for i in range(30):
	last_time = time.clock()
	img = grab_screen()
	times.append(time.clock() - last_time)
	print(times[len(times)-1])
print("Average fps:", 1/np.mean(times))