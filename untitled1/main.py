
def rec(a):
	if a <= 2: return 1
	elif a % 10 == 7: return rec(a-5)+1
	elif a % 4 == 0: return rec(a/4)+rec(a/2)
	else: return rec(a+1)+2


print(rec(int(input())))