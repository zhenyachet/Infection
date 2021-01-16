
def initialization(numberOfPeople):
    young = int(round(numberOfPeople * 0.07, 1))
    teen = int(round(numberOfPeople * 0.14, 1))
    adult = int(round(numberOfPeople * 0.12, 1))
    major = int(round(numberOfPeople * 0.45, 1))
    pensioner = int(round(numberOfPeople * 0.22, 1))

    homebodyYoung = int(round(young * 1))
    homebodyMajor = int(round(major * 0.11111))
    homebodyPensioner = int(round(pensioner * 0.409))
    factoryWorkerMajor = int(round(major * 0.7112))
    factoryWorkerPensioner = int(round(pensioner * 0.3182))
    hospitalWorkerAdult = int(round(adult * 0.25))
    factoryWorkerAdult = int(round(adult * 0.5))
    hospitalWorkerMajor = int(round(major * 0.06667))
    hospitalWorkerPensioner = int(round(pensioner * 0.1364))
    schoolWorkerTeen = int(round(teen * 1))
    schoolWorkerMajor = int(round(major * 0.08887))
    schoolWorkerPensioner = int(round(pensioner * 0.1365))
    shopWorkerAdult = int(round(adult * 0.25))
    shopWorkerMajor = int(round(major * 0.0222))

    schoolWorker = schoolWorkerTeen + schoolWorkerMajor + schoolWorkerPensioner
    homebody = homebodyYoung + homebodyMajor + homebodyPensioner
    factoryWorker = factoryWorkerAdult + factoryWorkerPensioner + factoryWorkerMajor
    hospitalWorker = hospitalWorkerAdult + hospitalWorkerPensioner + hospitalWorkerMajor
    shopWorker = shopWorkerMajor + shopWorkerAdult

    activeAdult = int(round(adult / 2))
    activeMajor = int(round(major / 2))
    activePensioner = int(round(pensioner / 2))
    # generate lists of zeros
    beInfected = True
    numberOfFields = 7
    # noinspection PyUnusedLocal
    state = [[0] * numberOfFields for i in range(numberOfPeople)]
    # fill the list
    for i in range(numberOfPeople):
        # fill young
        if i < young:
            # noinspection PyTypeChecker
            state[i][0] = 0.05
            state[i][1] = 0.01
            state[i][3] = 0
            homebody = homebody - 1
        # fill teens
        elif i > young - 1 and (i < teen + young):
            state[i][0] = 0.11
            state[i][1] = 0.08
            schoolWorker = schoolWorker - 1
            # fill teens who work from the beginning
            state[i][3] = 1
            # remaining work days
            state[i][5] = 2
        # activeTeen = activeTeen - 1
        elif i > young + teen - 1 and (i < teen + young + adult):
            state[i][0] = 0.14
            # fill adults who work from the beginning
            if activeAdult > 0:
                state[i][3] = 1
                # remaining work days
                state[i][5] = 2
            else:
                state[i][3] = 0
                state[i][5] = 2
            activeAdult = activeAdult - 1

            if factoryWorker > factoryWorkerPensioner + factoryWorkerMajor:
                state[i][1] = 0.47
                factoryWorker = factoryWorker - 1
            elif hospitalWorker > hospitalWorkerMajor + hospitalWorkerPensioner:
                state[i][1] = 0.3
                # shift for hospitals
                state[i][3] = 1
                state[i][5] = 3
                hospitalWorker = hospitalWorker - 1
            elif shopWorker > shopWorkerMajor:
                state[i][1] = 0.14
                shopWorker = shopWorker - 1
        elif i > young + teen + adult - 1 and (i < numberOfPeople - pensioner):
            state[i][0] = 0.25
            if activeMajor > 0:
                state[i][3] = 1
                # remaining work days
                state[i][5] = 2
            else:
                state[i][3] = 0
                state[i][5] = 2
            activeMajor = activeMajor - 1
            if schoolWorker > schoolWorkerPensioner:
                state[i][1] = 0.08
                # work for teachers 5/2 from the beginning
                state[i][3] = 1
                state[i][5] = 2
                schoolWorker = schoolWorker - 1
            elif homebody > homebodyPensioner:
                state[i][1] = 0.01
                # everyday go to the shop
                state[i][3] = 2
                state[i][5] = 0
                homebody = homebody - 1
            elif factoryWorker > factoryWorkerPensioner:
                state[i][1] = 0.47
                # infect the major who works in a factory
                if beInfected:
                    state[i][2] = 1
                    state[i][4] = 5
                    beInfected = not beInfected

                factoryWorker = factoryWorker - 1
            elif hospitalWorker > hospitalWorkerPensioner:
                state[i][1] = 0.3
                # shift for hospitals
                state[i][3] = 0
                state[i][5] = 3
                hospitalWorker = hospitalWorker - 1
            else:
                state[i][1] = 0.14
                shopWorker = shopWorker - 1
        else:
            state[i][0] = 0.45
            # fill pensioners who work from the beginning
            if activePensioner > 0:
                state[i][3] = 1
                # remaining work days
                state[i][5] = 2
            else:
                state[i][3] = 0
                state[i][5] = 2
            activePensioner = activePensioner - 1
            if schoolWorker > 0:
                state[i][1] = 0.08
                # work for teachers 5/2 from the beginning
                state[i][3] = 1
                state[i][5] = 2
                schoolWorker = schoolWorker - 1
            elif homebody > 0:
                state[i][1] = 0.01
                homebody = homebody - 1
            elif factoryWorker > 0:
                state[i][1] = 0.47
                factoryWorker = factoryWorker - 1
            elif hospitalWorker > 0:
                state[i][1] = 0.3
                # shift for hospitals
                state[i][3] = 1
                state[i][5] = 1
                hospitalWorker = hospitalWorker - 1
    return state