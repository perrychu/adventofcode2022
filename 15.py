input = '''Sensor at x=2150774, y=3136587: closest beacon is at x=2561642, y=2914773
Sensor at x=3983829, y=2469869: closest beacon is at x=3665790, y=2180751
Sensor at x=2237598, y=3361: closest beacon is at x=1780972, y=230594
Sensor at x=1872170, y=78941: closest beacon is at x=1780972, y=230594
Sensor at x=3444410, y=3965835: closest beacon is at x=3516124, y=3802509
Sensor at x=3231566, y=690357: closest beacon is at x=2765025, y=1851710
Sensor at x=3277640, y=2292194: closest beacon is at x=3665790, y=2180751
Sensor at x=135769, y=50772: closest beacon is at x=1780972, y=230594
Sensor at x=29576, y=1865177: closest beacon is at x=255250, y=2000000
Sensor at x=3567617, y=3020368: closest beacon is at x=3516124, y=3802509
Sensor at x=1774477, y=148095: closest beacon is at x=1780972, y=230594
Sensor at x=1807041, y=359900: closest beacon is at x=1780972, y=230594
Sensor at x=1699781, y=420687: closest beacon is at x=1780972, y=230594
Sensor at x=2867703, y=3669544: closest beacon is at x=3516124, y=3802509
Sensor at x=1448060, y=201395: closest beacon is at x=1780972, y=230594
Sensor at x=3692914, y=3987880: closest beacon is at x=3516124, y=3802509
Sensor at x=3536880, y=3916422: closest beacon is at x=3516124, y=3802509
Sensor at x=2348489, y=2489095: closest beacon is at x=2561642, y=2914773
Sensor at x=990761, y=2771300: closest beacon is at x=255250, y=2000000
Sensor at x=1608040, y=280476: closest beacon is at x=1780972, y=230594
Sensor at x=2206669, y=1386195: closest beacon is at x=2765025, y=1851710
Sensor at x=3932320, y=3765626: closest beacon is at x=3516124, y=3802509
Sensor at x=777553, y=1030378: closest beacon is at x=255250, y=2000000
Sensor at x=1844904, y=279512: closest beacon is at x=1780972, y=230594
Sensor at x=2003315, y=204713: closest beacon is at x=1780972, y=230594
Sensor at x=2858315, y=2327227: closest beacon is at x=2765025, y=1851710
Sensor at x=3924483, y=1797070: closest beacon is at x=3665790, y=2180751
Sensor at x=1572227, y=3984898: closest beacon is at x=1566446, y=4774401
Sensor at x=1511706, y=1797308: closest beacon is at x=2765025, y=1851710
Sensor at x=79663, y=2162372: closest beacon is at x=255250, y=2000000
Sensor at x=3791701, y=2077777: closest beacon is at x=3665790, y=2180751
Sensor at x=2172093, y=3779847: closest beacon is at x=2561642, y=2914773
Sensor at x=2950352, y=2883992: closest beacon is at x=2561642, y=2914773
Sensor at x=3629602, y=3854760: closest beacon is at x=3516124, y=3802509
Sensor at x=474030, y=3469506: closest beacon is at x=-452614, y=3558516'''

test_input = '''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3'''

import re
import math

def manhattan(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def xval_within_dist(yval,point,distance,xmin=-math.inf, xmax=math.inf):
    ydist = abs(yval - point[1])
    xdist = distance-ydist
    if (xdist<0):
        return None
    else:
        # print(point,distance,ydist,xdist)
        # print(point[0]-xdist,point[0]+xdist+1)
        return (max(xmin,point[0]-xdist),min(xmax,point[0]+xdist),)


def points_on_line(input, yval, xmin=-math.inf, xmax=math.inf, part=2):
    all_points = list()
    beacon_points = set()
    for r in input:
        sensor, beacon, distance = r

        if beacon[1] == yval:
            beacon_points.add(beacon[0])

        xvals = xval_within_dist(yval, sensor, distance,xmin,xmax)
        if xvals is None:
            continue
        min_x, max_x = xvals

        all_points.append((min_x,max_x))
    
    all_points.sort(key=lambda x:x[0])
    covered = 0
    uncovered = []
    min_x = all_points[0][0]
    max_x = all_points[0][1]
    for span in all_points[1:]:
        if span[0] <= max_x:
            max_x = max(max_x,span[1])
        else:
            covered += max_x-min_x+1
            uncovered.append((max_x+1,span[0]-1))
            min_x=span[0]
            max_x=span[1]
    covered += max_x-min_x+1


    if part==1:
        return covered-len(beacon_points)
    else:
        return uncovered

def parse(input):
    output = []
    for r in input.splitlines():
        coords = [int(x) for x in re.split(r'[-\D]+', r) if len(x) > 0]
        sensor = (coords[0],coords[1])
        beacon = (coords[2],coords[3])
        distance = manhattan(sensor,beacon)
        output.append([sensor,beacon,distance])
    return output


input = parse(input)
test_input = parse(test_input)

#Part 1
# print(points_on_line(test_input,10,part=1))
print(points_on_line(input,2000000,part=1))
print()

#Part 2
def find_beacon(input,lower,upper):
    for y in range(lower,upper+1):
        if y % 200000 == 0:
            print(y)
        valid = points_on_line(input,y,lower,upper)
        if len(valid) > 0:
            print(valid[0][0], y, valid[0][0]*4000000+y)
            return(valid[0],y)

# print(find_beacon(test_input,0,20))
print(find_beacon(input,0,4000000))