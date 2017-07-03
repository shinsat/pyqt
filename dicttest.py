import sys

items = {'1234.T':[{'L1':'ABCD', 'L2':'EFG', 'L3':'HIJK', 'L4':'123'},{'L1':'abcd', 'L2':'efg', 'L3':'hijk', 'L4':'321'}]}
add = {'L1':'X1', 'L2':'X2', 'L3':'X3', 'L4':'111'}
print(items)

items['1234.T'].append(add)
print(items)

sortables = items.values()
#for s in sortables:
#    for ss in s:
#        print(ss['L4'])

for s in sortables:
    goal = {ss['L4']: ss for ss in s}  # for s in sortables}
#    goal = {ss['L4']: ss for ss in s}   # for s in sortables}
 #   print('Goal = ', goal)



goal = dict(sorted(goal.items()))
print('Goal = ', goal)
items['1234.T'].clear()
items['1234.T'].append(goal)
print('final:', items)
#print('sortables ', sortables)

#一括初期化
inits = dict()
inits['111'] = 0
inits['222'] = 0
inits['333'] = 0
print(inits)

inits = {key: 1 for key in inits.keys()}
print(inits)