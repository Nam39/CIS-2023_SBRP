import numpy as np
import random


class Route():
    def __init__(self, routesFn):
        self.stops = None
        self.students = None
        self.maximumWalk = None
        self.capacity = None
        self.studentNearStops = None
        self.stopNearStops = None
        self.globalPathList = None
        self.globalStudentsDict = None

        self.processFile(routesFn)
        self.generateStudentNearStops()
        self.generateStopNearStops()
        self.generateStopNearStudents()

    def processFile(self, fileName):
        self.stops = dict()
        self.students = dict()
        self.maximumWalk = None
        self.capacity = None
        stopsMax = None
        studentsMax = None
        currentStop = 0
        currentStudent = 1

        with open(fileName, 'r') as f:
            for number, line in enumerate(f):
                if number == 0:
                    cons = line.split()
                    stopsMax = int(cons[0])
                    studentsMax = int(cons[2])
                    self.maximumWalk = float(cons[4])
                    self.capacity = float(cons[7])
                else:
                    if len(line) < 2:
                        # empty line
                        continue
                    else:
                        id, xCoordinate, yCoordinate = [float(i) for i in line.split()]
                        if (currentStop < stopsMax):
                            currentStop = currentStop + 1
                            self.stops[int(id)] = np.array([xCoordinate, yCoordinate])
                        elif (currentStudent <= studentsMax):
                            currentStudent = currentStudent + 1
                            self.students[int(id)] = np.array([xCoordinate, yCoordinate])

    def generateStudentNearStops(self):
        self.studentNearStops = dict()
        for keyStudent, valueStudent in self.students.items():
            availableStops = set()
            for keyStop, valueStop in list(self.stops.items())[1:]:
                if np.linalg.norm(valueStudent - valueStop) < self.maximumWalk:
                    availableStops.add(keyStop)
            self.studentNearStops[keyStudent] = availableStops

    def generateStopNearStops(self):
        self.stopNearStops = dict()
        for keyStop, valueStop in list(self.stops.items())[1:]:
            stops_distances = []
            for keyOtherStop, valueOtherStop in list(self.stops.items())[1:]:
                if valueStop is not valueOtherStop:
                    stops_distances.extend([tuple([keyOtherStop, np.linalg.norm(valueStop - valueOtherStop)])])
            self.stopNearStops[keyStop] = tuple(sorted(stops_distances, key=lambda x: x[1]))

    def generateStopNearStudents(self):
        self.stopNearStudents = dict()
        for keyStop, valueStop in list(self.stops.items())[1:]:
            if keyStop == 0:
                continue
            availableStudents = set()
            for keyStudent, valueStudent in self.students.items():
                if np.linalg.norm(valueStop - valueStudent) < self.maximumWalk:
                    availableStudents.add(keyStudent)
            self.stopNearStudents[keyStop] = availableStudents

    # Ma gia:
        # LOCAL SEARCH = TIM KIEM DIA PHUONG
        # S = S0; Chu S la Solution // Khoi tao 1 giai phap ban dau S0
        # While not Termination_Criterion do
        #   Generate(N(S)); // Sinh ra cac lan can cua giai phap S
        #   If there is no better neighbor then stop
        #   // Coi nhu current_solution la optimal solution
        #   S = S'; // Giai phap S' thuoc N(S) tot hon S nen duoc gan.
        # Endwhile

    def routeLocalSearch(self):
        globalStops = list(self.stops.copy().keys())[1:]  # skip the base stop
        baseStop = globalStops[0]
        globalPathList = []

        globalStudentsDict = dict()
        globalStudents = set(self.students.copy().keys())
        for student in range(1, len(self.students) + 1):
            globalStudentsDict[student] = None

        while len(globalStudents) != 0:
            localStops = globalStops.copy()
            nextStop = random.choice(localStops)
            currentStop = 0  # base stop
            capacity = self.capacity
            localPathList = list()
            while True:
                if nextStop == None or len(globalStudents) == 0:
                    if localPathList not in globalPathList:
                        globalPathList.extend([localPathList])
                    break
                if len(globalStudents) > capacity and localStops == []:
                    return [None, None]  # not enough capacity

                # list of students connected with only our stop or many stops
                studentOnly = set()
                studentMany = set()
                for student in self.stopNearStudents[nextStop]:
                    temp = [i for i in self.studentNearStops[student] if i in globalStops]
                    if student in globalStudents:
                        if len(temp) == 1:
                            studentOnly.add(student)
                        elif len(temp) > 1:
                            studentMany.add(student)

                if capacity < len(studentOnly):  # students with the same stop
                    if localStops == []:
                        if len(globalStudents) > capacity and localStops == []:
                            return [None, None]  # not enough capacity
                        globalPathList.extend([localPathList])
                        nextStop = None
                        break
                    localStops.remove(nextStop)
                    for student in self.stopNearStops[nextStop]:
                        if student[0] in localStops:
                            nextStop = student[0]
                            break
                else:
                    currentStop = nextStop
                    for student in studentOnly:
                        # pickup single and assign to stop
                        globalStudentsDict[student] = currentStop
                        # remove from available list
                        globalStudents.remove(student)
                        capacity -= 1

                    for student in studentMany:
                        if capacity > 0:
                            # pickup multi and assign to stop
                            globalStudentsDict[student] = currentStop
                            globalStudents.remove(student)
                            capacity -= 1

                    localStops.remove(currentStop)
                    globalStops.remove(currentStop)
                    localPathList.extend([currentStop])

                    if capacity > 0 and localStops != []:
                        for student in self.stopNearStops[nextStop]:
                            if student[0] in localStops:
                                nextStop = student[0]
                                break
                        if np.linalg.norm(currentStop - nextStop) > np.linalg.norm(nextStop - baseStop):
                            nextStop = None
                            globalPathList.extend([localPathList])
                    else:
                        nextStop = None
                        globalPathList.extend([localPathList])

        self.globalPathList = globalPathList
        self.globalStudentsDict = globalStudentsDict
        return [self.globalPathList, self.globalStudentsDict]

    def getStops(self):
        return self.stops

    def getStudents(self):
        return self.students

    def getMaximumWalk(self):
        return self.maximumWalk

    def getCapacity(self):
        return self.capacity

    def getStudentNearStops(self):
        return self.studentNearStops

    def getDistance(self):
        distance = 0.0
        for path in self.globalPathList:
            for i in range(len(path) + 1):
                if i == 0:
                    distance += np.linalg.norm(np.array(self.stops[0]) - np.array(self.stops[path[0]]))
                elif i == len(path):
                    distance += np.linalg.norm(np.array(self.stops[0]) - np.array(self.stops[path[i - 1]]))
                elif i < len(path):
                    distance += np.linalg.norm(np.array(self.stops[path[i]]) - np.array(self.stops[path[i - 1]]))
        return distance


if __name__ == "__main__":
    # fileName = "C:\\Users\\PC HIEP\\Documents\\pp-nghien-cuu-khoa-hoc\\SBRP\\CIS-DS_The-School-Bus-Routing-Problem\\instances\\my1.txt"
    fileName = "../instances/my1.txt"
    route = Route(fileName)

    # print some information about the stops and students
    # print("Number of stops: ", route.getStops())
    # print("Number of students: ", route.getStudents())
    # print("Maximum walking distance: ", route.getMaximumWalk())
    print("Capacity of each vehicle: ", route.getCapacity())

    optimalRoute = route.routeLocalSearch()
    print(optimalRoute)
