a = [-1 for i in range(1024)]
c = []
for i in range(6,41):
	b = int(input())
	a[b] = i

last = 50
for i in range(1024):
	if a[i] == -1:
		a[i] = last
	else:
		last = a[i]

for i in range(1024//16):
	c.append(sum(a[16*i:16*(i+1)])//16)
print(c)