import matplotlib.pyplot as plt
import os

frequency = 0
counter = 0
x_list = []
y_list = []
index_counter = 0

for i in range(3):  # for loop parameters may differ according to what we are testing
	y_list += [],
	for j in range(3):  # 5 is the number of runs
		counter = 0
		f = open('out' + str(i) + '_' + str(j) + '.txt', 'r')
		for line in f.readlines():
			if not line.startswith("+"):
				frequency = int(line.strip())
			else:
				counter += int(line.strip().split("+ ")[1])  # number of vehicles lent during collaboration
		y_list[index_counter].append(counter)
		f.close()
		#  os.remove('out' + str(i) + '_' + str(j) + '.txt')
	x_list.append(frequency)
	index_counter += 1

y_average = []

for i in range(len(y_list)):
	average = 0
	for run in y_list[i]:
		average += run
	average = average / 3
	y_average.append(average)


plt.plot(x_list, y_average, "ro-",)

plt.xlabel("Emergencies' Frequency")
plt.ylabel('Collaborative Behaviour')
plt.title("Collaboration vs Emergencies' Frequency")
plt.grid(False)
plt.savefig("frequency-collab.png")
plt.show()
