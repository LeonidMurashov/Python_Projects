class A:
    history = []
    id = 0

    def __init__(self, i):
        self.history = []
        self.id = i

    def add(self):
        self.history.append("some")

units = []
for i in range(10):
    a = A(i)
    units.append(a)
    units[i].add()

for unit in units:
    print(unit.id, len(unit.history), end='\n')
