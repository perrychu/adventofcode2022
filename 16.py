input = '''Valve GV has flow rate=23; tunnel leads to valve WO
Valve TS has flow rate=0; tunnels lead to valves IG, TX
Valve UC has flow rate=0; tunnels lead to valves XJ, VZ
Valve TJ has flow rate=0; tunnels lead to valves GJ, YV
Valve KF has flow rate=0; tunnels lead to valves QY, VP
Valve PO has flow rate=0; tunnels lead to valves YF, VP
Valve CV has flow rate=0; tunnels lead to valves VB, QK
Valve NK has flow rate=6; tunnels lead to valves MI, QY, DO, QJ, YH
Valve IG has flow rate=4; tunnels lead to valves MI, FP, OP, UV, TS
Valve KN has flow rate=0; tunnels lead to valves RF, CY
Valve KR has flow rate=0; tunnels lead to valves VP, DI
Valve VZ has flow rate=19; tunnel leads to valve UC
Valve MW has flow rate=0; tunnels lead to valves UZ, VB
Valve LJ has flow rate=25; tunnels lead to valves XJ, LI
Valve DI has flow rate=0; tunnels lead to valves KR, AA
Valve TO has flow rate=12; tunnels lead to valves TG, PB, BZ
Valve CG has flow rate=0; tunnels lead to valves VP, TX
Valve GJ has flow rate=0; tunnels lead to valves QL, TJ
Valve UZ has flow rate=0; tunnels lead to valves MW, VP
Valve RF has flow rate=16; tunnels lead to valves RD, KN, AU
Valve CY has flow rate=0; tunnels lead to valves KN, YV
Valve AA has flow rate=0; tunnels lead to valves UV, VS, NB, XO, DI
Valve YV has flow rate=11; tunnels lead to valves CY, PW, TJ
Valve VS has flow rate=0; tunnels lead to valves QK, AA
Valve TX has flow rate=14; tunnels lead to valves RM, CG, TS, DM, YH
Valve SB has flow rate=0; tunnels lead to valves YF, BZ
Valve QY has flow rate=0; tunnels lead to valves NK, KF
Valve PB has flow rate=0; tunnels lead to valves HP, TO
Valve YF has flow rate=20; tunnels lead to valves DM, SB, PO
Valve TG has flow rate=0; tunnels lead to valves RM, TO
Valve UV has flow rate=0; tunnels lead to valves IG, AA
Valve XJ has flow rate=0; tunnels lead to valves LJ, UC
Valve DM has flow rate=0; tunnels lead to valves YF, TX
Valve PW has flow rate=0; tunnels lead to valves YV, LI
Valve RD has flow rate=0; tunnels lead to valves QL, RF
Valve OM has flow rate=0; tunnels lead to valves QK, OP
Valve RM has flow rate=0; tunnels lead to valves TX, TG
Valve SH has flow rate=0; tunnels lead to valves AU, HP
Valve LI has flow rate=0; tunnels lead to valves PW, LJ
Valve FP has flow rate=0; tunnels lead to valves IG, VB
Valve BZ has flow rate=0; tunnels lead to valves SB, TO
Valve DO has flow rate=0; tunnels lead to valves NK, VB
Valve WO has flow rate=0; tunnels lead to valves QK, GV
Valve MI has flow rate=0; tunnels lead to valves IG, NK
Valve QK has flow rate=10; tunnels lead to valves VS, OM, WO, CV
Valve OP has flow rate=0; tunnels lead to valves IG, OM
Valve AU has flow rate=0; tunnels lead to valves SH, RF
Valve QJ has flow rate=0; tunnels lead to valves NK, XO
Valve VP has flow rate=8; tunnels lead to valves PO, CG, KF, KR, UZ
Valve HP has flow rate=17; tunnels lead to valves SH, PB
Valve XO has flow rate=0; tunnels lead to valves QJ, AA
Valve QL has flow rate=15; tunnels lead to valves RD, GJ
Valve NB has flow rate=0; tunnels lead to valves VB, AA
Valve VB has flow rate=7; tunnels lead to valves DO, CV, MW, NB, FP
Valve YH has flow rate=0; tunnels lead to valves NK, TX'''

test_input = '''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II'''


from collections import defaultdict
import re

map = dict()
for r in test_input.splitlines():
    key = r[6:8]
    rate = int(r.split('=')[-1].split(';')[0])
    paths = re.split('valves* ',r)[-1].split(', ')
    map[key] = (rate,paths)

value_map = dict()
skip_value_map = dict()
for key in map:
    value_map[key]=dict()
    skip_value_map[key]=dict()
    for i in range(31):
        value_map[key][i]=dict()
        skip_value_map[key][i]=dict()

def get_max_value(key, minute, opened = []):
    if minute <= 1:
        return 0, opened

    #open current
    total_current = 0

    if key not in opened and map[key][0] > 0:
        if minute in value_map[key] and save(opened) in value_map[key][minute]:
            total_current = value_map[key][minute][save(opened)]
            open_current = opened
        else:
            value_current = get_value(key,minute-1)
            max_val_next = -1
            max_opened_next = None
            for i in map[key][1]:
                value_next, opened_next = get_max_value(i,minute-2,opened+[key])
                if value_next > max_val_next:
                    max_val_next = value_next
                    max_opened_next = opened_next
            total_current = value_current + max_val_next
            open_current = max_opened_next
            value_map[key][minute][save(max_opened_next)] = total_current
    
    #skip to next
    if minute in skip_value_map[key] and save(opened) in skip_value_map[key][minute]:
        total_next = skip_value_map[key][minute][save(opened)]
        open_next = opened
    else:
        max_val_next = -1
        max_opened_next = None
        for i in map[key][1]:
            value_next, opened_next = get_max_value(i,minute-1,opened)
            if value_next > max_val_next:
                max_val_next = value_next
                max_opened_next = opened_next
        total_next = max_val_next
        open_next = max_opened_next
        skip_value_map[key][minute][save(max_opened_next)] = total_next

    if total_current > total_next:
        return total_current, open_current
    else:
        return total_next, open_next

def get_value(key, minute):
    return map[key][0] * minute

def save(opened):
    return tuple(sorted(opened))


for minute in range(0,10):
    # for key in map:
    #     get_max_value(key, minute, [])
    print(minute, get_max_value('AA', minute, []))

print("*****")
print(value_map)
print("-----")
print(skip_value_map)


