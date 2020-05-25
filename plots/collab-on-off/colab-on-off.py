import matplotlib.pyplot as plt
import os

collab = ""
counter = 0
x_list = []
y_list = []
index_counter = 0

for i in range(1, 3, 1):  # for loop parameters may differ according to what we are testing
    y_list += [],
    for j in range(3):  # 5 is the number of runs
        counter = 0
        f = open('out' + str(i) + '_' + str(j) + '.txt', 'r')
        for line in f.readlines():
            if not line.startswith("+"):
                collab = line.strip()
            else:
                counter += int(line.strip().split("+ ")[1])  # number of hospitals
        y_list[index_counter].append(counter)
        f.close()
    #  os.remove('out' + str(i) + '_' + str(j) + '.txt')
    x_list.append(collab)
    index_counter += 1

y_average = []

for i in range(len(y_list)):
    average = 0
    for run in y_list[i]:
        average += run
    average = average / 3
    y_average.append(average)

n, bins, patches = plt.hist(x=x_list, color='#FF0000', weights=y_average)
plt.grid(False)
plt.xlabel('Collaboration')
plt.ylabel('Emergencies Successful')
plt.title('Collaboration On vs. Off')
maxfreq = n.max()
# Set a clean upper y-axis limit.
plt.bar(x_list, y_average, 0.4)
plt.show()
