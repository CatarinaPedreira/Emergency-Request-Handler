import matplotlib.pyplot as plt
import os

n_vehicles = 0
counter = 0
x_list = []
y_list = []
index_counter = 0

for i in range(3, 12, 4):  # for loop parameters may differ according to what we are testing
	y_list += [],
	for j in range(3):  # 5 is the number of runs
		counter = 0
		f = open('out' + str(i) + '_' + str(j) + '.txt', 'r')
		for line in f.readlines():
			if not line.startswith("+"):
				n_vehicles = int(line.strip())
			else:
				counter += int(line.strip().split("+ ")[1])  # number of vehicles lent during collaboration
		y_list[index_counter].append(counter)
		f.close()
		#  os.remove('out' + str(i) + '_' + str(j) + '.txt')
	x_list.append(n_vehicles)
	index_counter += 1

y_average = []

for i in range(len(y_list)):
	average = 0
	for run in y_list[i]:
		average += run
	average = average / 15
	y_average.append(average)


plt.plot(x_list, y_average, "ro")

plt.xlabel('Number of vehicles per hospital')
plt.ylabel('Number of backup vehicles')
plt.title('Collaboration between Medical Vehicles')
plt.grid(True)
plt.savefig("vehicles-collab.png")
plt.show()

