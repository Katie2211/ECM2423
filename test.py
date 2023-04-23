import re
from datetime import datetime
Temp = "Harrison%20Building'>"
building = re.sub(r'%20', ' ', Temp)
building = re.sub(r"'>", '', building)
print(building)
print(datetime.now())
listTemp = "*a*b*c".split("*")
for i in listTemp:
    if(i != ""):
        print(i)
streaksTuple = [("a", 5),("b", 2),("c",3),("d", 8),("e",9)]
sortedTuple = sorted(streaksTuple, key=lambda tup: tup[1])
print(sortedTuple)
print(sortedTuple[-2:])
topStreaks = sortedTuple[-2:]
topStreak1Name = topStreaks[0][0]
topStreak1Number = topStreaks[0][1]
print(topStreak1Name)
print(topStreak1Number)
print(datetime.now().date())
