from datetime import datetime
from collections import defaultdict

print("--- Day 6: Lanternfish ---")

def naissance(couveuse, numberOfDays, caption):

    for i in range(numberOfDays):
        naissances = defaultdict(lambda: 0)
        for day in range(1,9):
            naissances[day-1] = couveuse[day]
        naissances[6] += couveuse[0]
        naissances[8] += couveuse[0]

        couveuse = naissances
        #print(f"After {i+1} days : {couveuse} ")

    numberOfFishs = sum(couveuse.values())
    print(f"  ** {caption} : Number of fish after {numberOfDays} days = {numberOfFishs}")
    return(numberOfFishs)

start_time = datetime.now()
couveuse = defaultdict(lambda: 0)

f = open(".\Day6.txt", "r")
for line in f:
    instruction = line.rstrip().split(",")
    for v in instruction:
        couveuse[int(v)] += 1
f.close()


print(couveuse)

nbOfFish = naissance(couveuse, 80, "Star 1")
nbOfFish = naissance(couveuse, 256, "Star 2")

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))