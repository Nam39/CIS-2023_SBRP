import route

if __name__ == '__main__':
    fileName = "../instances/sbr3.txt"
    route = route.Route(fileName)

    count = 0
    loop = 1000
    for i in range(loop):
        print('{0}/{1} ({2}%)'.format(i, loop, 100 * (i / loop)))
        globalPathList, globalStudentsDict = route.routeLocalSearch()
        if globalPathList == None and globalStudentsDict == None:
            count += 1
    print('Not feasible solutions: {0}/{1} ({2}%)'.format(count, loop, 100 * (count / loop)))
