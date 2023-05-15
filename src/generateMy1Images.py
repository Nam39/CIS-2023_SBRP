import route as r
import matplotlib.pyplot as plt
import time


def plotStops(stops):
    plt.scatter(stops[0][0], stops[0][1], marker='o', s=200, color='red',
                edgecolor='xkcd:dark grey')  # ve diem dau tien trong danh sach cac diem dung
    for keyStop, valueStop in list(stops.items())[1:]:
        plt.scatter(valueStop[0], valueStop[1], marker='.', s=200, color='pink', edgecolor='xkcd:dark grey')
        plt.text(valueStop[0] + 0.2, valueStop[1] + 0.2, str(keyStop), fontdict=dict(color='xkcd:dark grey'))


def plotStudents(students):
    for keyStudent, valueStudent in students.items():
        plt.scatter(valueStudent[0], valueStudent[1], marker='.', s=200, color='blue', edgecolor='xkcd:dark grey')
        plt.text(valueStudent[0] + 0.2, valueStudent[1] + 0.2, str(keyStudent), fontdict=dict(color='xkcd:dark grey'))


def plotStudentPotentialAssignments(studentNearStops):
    for key, value in studentNearStops.items():
        studentX, studentY = students[key]
        for i in value:
            stopX, stopY = stops[i]
            plt.plot([studentX, stopX], [studentY, stopY], 'k:', lw=1.5)  # Ve duong manh 'k' co do day la 1.5


def routeLocalSearch(loop):
    startTime = time.process_time()
    minValue = float('+Inf')  # gia tri khoang cach nho nhat tim thay
    # 2 gia tri tuong ung voi khoang cach nho nhat hien tai!
    minPathList = None
    minStudentsDict = None
    print('Local search: {0} iterations'.format(loop))
    for i in range(loop):
        globalPathList, globalStudentsDict = route.routeLocalSearch()
        if globalPathList == None or globalStudentsDict == None:
            i = i - 1
        distance = route.getDistance()
        if distance < minValue:
            print('Distance:', distance)
            minValue = distance
            minPathList = globalPathList
            minStudentsDict = globalStudentsDict
    endTime = time.process_time()
    print(endTime - startTime)
    return [minPathList, minStudentsDict]


def drawCoordinateAxis():
    # clear all
    plt.cla()
    plt.clf()
    plt.title(
        '{0}\nstops: {1}, students: {2}, maximum walk: {3}, capacity: {4}'.format(fileName, len(stops), len(students),
                                                                                  maximumWalk, capacity))
    # Ve truc x va y
    plt.axhline(0, color='k', lw=0.5)
    plt.axvline(0, color='k', lw=0.5)

    # Ve luoi:
    # plt.grid(True)
    # plt.xticks(np.arange(-15, 15, 1))
    # plt.yticks(np.arange(-15, 15, 1))
    # plt.axis([-15, 15, -15, 15])

    plt.tight_layout()  # auto fixed

if __name__ == '__main__':
    fileName = '../instances/my1.txt'
    route = r.Route(fileName)

    stops = route.getStops()
    students = route.getStudents()
    maximumWalk = route.getMaximumWalk()
    capacity = route.getCapacity()
    studentNearStops = route.getStudentNearStops()

    print('Route local search', end=' ')
    paths, studentAssignments = routeLocalSearch(1000)

    drawCoordinateAxis()
    plotStudents(students)
    plotStops(stops)

    plt.savefig('../images/my1-stops.jpg')

    plotStudentPotentialAssignments(studentNearStops)

    plt.savefig('../images/my1-potential-stops.jpg')

    ## khoi tao lai de xoa cac tuyen duong tiem nang
    drawCoordinateAxis()
    plotStudents(students)
    plotStops(stops)

    for key, value in studentAssignments.items():
        studentX, studentY = students[key]
        stopX, stopY = stops[value]
        plt.plot([studentX, stopX], [studentY, stopY], 'b-', lw=1.0)

    for path in paths:
        for i in range(len(path) + 1):
            if i == 0:
                stopX, stopY = stops[path[0]]
                plt.plot([stops[0][0], stopX], [stops[0][1], stopY], 'r-', lw=1.0)
            elif i == len(path):
                stopX, stopY = stops[path[i - 1]]
                plt.plot([stops[0][0], stopX], [stops[0][1], stopY], 'r-', lw=1.0)
            elif i < len(path):
                firstX, firstY = stops[path[i]]
                secondX, secondY = stops[path[i - 1]]
                plt.plot([firstX, secondX], [firstY, secondY], 'r-', lw=1.0)

    plt.savefig('../images/my1-route.jpg')
