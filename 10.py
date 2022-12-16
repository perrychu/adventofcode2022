input = '''noop
addx 24
addx -19
noop
noop
noop
addx 5
noop
addx 1
addx 5
addx -1
addx 5
addx 1
addx 14
addx -9
addx -1
addx 5
noop
addx 2
addx -20
addx 24
addx -36
addx -2
noop
addx 3
addx 2
addx 5
addx 21
addx -16
noop
addx 2
addx 15
addx -14
addx 2
addx 5
addx 2
addx -4
addx 5
addx -8
addx 15
addx 2
addx 3
addx -2
addx -38
noop
addx 3
addx 4
noop
addx 7
noop
noop
addx -2
addx 5
addx -16
addx 21
noop
addx -10
addx 11
addx 2
addx 5
addx 4
noop
noop
addx -6
addx 7
noop
addx 3
addx -36
noop
addx 5
noop
addx 20
addx -19
addx 5
addx 4
noop
addx -2
addx 3
noop
addx 4
noop
addx -1
addx 5
addx 3
addx -28
addx 30
noop
addx 6
noop
noop
addx 1
addx -38
addx 40
addx -33
addx 20
addx -19
addx 2
noop
addx 28
addx -23
addx 5
addx 2
addx 2
addx 3
addx -2
addx 5
addx 2
addx -7
addx 12
addx -2
noop
addx 3
addx -38
noop
addx 24
addx -17
noop
addx 5
noop
noop
addx 1
addx -8
addx 13
noop
noop
addx 2
addx 5
addx 2
addx 6
addx -5
addx 4
noop
addx 1
addx 2
noop
addx 3
noop
noop'''

cycles = []
value = 1
for r in input.splitlines():
    if r[:4] == 'noop':
        cycles.append(value)
    else:
        add_val = int(r.split(' ')[-1])
        cycles.append(value)
        cycles.append(value)
        value += add_val

tot=0
for i in range(20,240,40):
    print(i, cycles[i]-1, i*cycles[i-1])
    tot+=i*cycles[i-1]
print(tot)

output = []
row = []
for i,v in enumerate(cycles):
    if abs((i%40)-v) <= 1:
        row.append("#")
    else:
        row.append(".")
    
    if (i+1)%40 == 0:
        output.append(row)
        row = []
output.append(row)

for r in output:
    print("".join(r))

