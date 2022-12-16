from re import T
from typing import ItemsView
from unittest import case


class monkey:
    def __init__(self, items, op, test, t, f):
        self.items = items
        self.op = op
        self.test = test
        self.t = t
        self.f = f
        self.count = 0

    def inspect(self):
        if len(self.items)==0:
            return None

        self.count += 1

        i = self.items.pop(0) 
        i = self.op(i)
        #part 1 only
        #i = i//3
        #part 2 only
        i = i % 9699690
        if i % self.test == 0:
            return (i,self.t)
        else:
            return (i,self.f)

    def receive(self, item):
        self.items.append(item)

input = '''Monkey 0:
  Starting items: 77, 69, 76, 77, 50, 58
  Operation: new = old * 11
  Test: divisible by 5
    If true: throw to monkey 1
    If false: throw to monkey 5

Monkey 1:
  Starting items: 75, 70, 82, 83, 96, 64, 62
  Operation: new = old + 8
  Test: divisible by 17
    If true: throw to monkey 5
    If false: throw to monkey 6

Monkey 2:
  Starting items: 53
  Operation: new = old * 3
  Test: divisible by 2
    If true: throw to monkey 0
    If false: throw to monkey 7

Monkey 3:
  Starting items: 85, 64, 93, 64, 99
  Operation: new = old + 4
  Test: divisible by 7
    If true: throw to monkey 7
    If false: throw to monkey 2

Monkey 4:
  Starting items: 61, 92, 71
  Operation: new = old * old
  Test: divisible by 3
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 5:
  Starting items: 79, 73, 50, 90
  Operation: new = old + 2
  Test: divisible by 11
    If true: throw to monkey 4
    If false: throw to monkey 6

Monkey 6:
  Starting items: 50, 89
  Operation: new = old + 3
  Test: divisible by 13
    If true: throw to monkey 4
    If false: throw to monkey 3

Monkey 7:
  Starting items: 83, 56, 64, 58, 93, 91, 56, 65
  Operation: new = old + 5
  Test: divisible by 19
    If true: throw to monkey 1
    If false: throw to monkey 0
'''

monkeys = {}
ops = [lambda x: x*11, lambda x:x+8, lambda x:x*3, lambda x:x+4, lambda x:x*x, lambda x:x+2, lambda x:x+3, lambda x:x+5]

for m in input.split('\n\n'):
    details = m.split('\n')
    num = int(details[0][-2])
    items = [int(i) for i in details[1][18:].split(", ")]
    op = ops[num]
    test = int(details[3].split(' ')[-1])
    t = int(details[4].split(' ')[-1])
    f = int(details[5].split(' ')[-1])

    monkeys[num] = monkey(items, op, test, t, f)

for r in range(10000):
    print(r)
    maxval = 0
    for m in monkeys:
        result = monkeys[m].inspect()
        while result is not None:
            maxval = max(result[0], maxval)
            monkeys[result[1]].receive(result[0])
            result = monkeys[m].inspect()
    print(maxval)

for m in monkeys:
    print(m, monkeys[m].count)
    
    



    