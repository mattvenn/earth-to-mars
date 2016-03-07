from mission import Mission

mission = Mission()

# fetch all the samples
samples = mission.getAllSamples()

# samples is a type of variable called a list, we can loop through it like this:
min = 1000
max = -1000
total = 0
number = 0

for sample in samples:

    # store the amount for methane
    amount = sample['methane']

    # keep a track of the total
    total = total + amount

    # number of samples
    number = number + 1

    # check minimum
    if amount < min:
        min = amount

    # check max
    if amount > max:
        max = amount

print("number samples = ")
print(number)

print("min = ")
print(min)

print("max = ")
print(max)

print("avg = ")
print(total / number)
