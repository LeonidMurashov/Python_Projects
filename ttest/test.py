k = 0; m = 0; l = 0
n = int(input())

a = [int(input()) for i in range(4)]
for i in range(n-4):
	if a[0]%31==0:
		k += 1
	l+=1
	a.pop(0)
	a.append(int(input()))
	if a[3]%31==0:
		m+=l
	else:
		m+=k
print(m)
