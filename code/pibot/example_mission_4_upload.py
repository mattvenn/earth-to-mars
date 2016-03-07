from mission import Mission

mission = Mission()

# read all the samples into a list called data
data = mission.loadData()

# go through each sample the robot took and print it out
for sample in data:
    uploaded = mission.uploadSample(sample, 'Aurora')
    print(uploaded)

