import matplotlib.pyplot as plt
import os
import route as r


if not os.path.exists('../images'):
    os.makedirs('../images')
for fileName in os.listdir("../instances"):
    if fileName.endswith(".txt"):
        plt.cla()  # Clear axis
        plt.clf()  # Clear figure
        # print('file', fileName)
        route = r.Route('../instances/' + fileName)
        # print(route.getCapacity())
        stops = route.getStops()
        students = route.getStudents()

        plt.title(fileName)
        plt.scatter(stops[0][0], stops[0][1], marker='o', color='red')
        for keyStop, valueStop in list(stops.items())[1:]:
            plt.scatter(valueStop[0], valueStop[1], marker='.', color='black')
        for keyStudent, valueStudent in students.items():
            plt.scatter(valueStudent[0], valueStudent[1], marker='.', color='blue')

        plt.savefig('../images/' + fileName.split('.')[0] + '.jpg', dpi = 250)
