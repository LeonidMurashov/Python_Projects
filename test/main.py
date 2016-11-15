roofTop = input().split()
roofLeft = input().split()
roofRight = input().split()

if roofRight[1] != 0:
    chislo = abs(float(roofRight[0]) - float(roofLeft[0])) * float(roofRight[1])
    print(chislo)
