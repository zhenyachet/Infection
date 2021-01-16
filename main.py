# generate random floating point values
import random
from initialization import initialization
from matplotlib import pyplot as plt


# noinspection PyTypeChecker

def plotsMaker(listOfInfectedPeople, averageReproductionList, hospitalWorkloadList):
    a = [i for i in range(0, 100)]

    plt.plot(a, listOfInfectedPeople, label='listOfInfectedPeople')
    plt.xlabel('Days')
    plt.ylabel('The number of infected people')
    plt.title('Infected people during the period of 100 days')
    plt.show()
    plt.plot(a, averageReproductionList, label='averageReproductionList')
    plt.xlabel('Days')
    plt.ylabel('Average reproduction per day')
    plt.title('Average reproduction number per day of 100 days')
    plt.show()
    plt.plot(a, hospitalWorkloadList, label='hospitalWorkloadList')
    plt.xlabel('Days')
    plt.ylabel('Hospital capacity')
    plt.title('Hospital capacity per day of 100 days')
    plt.show()


def checking(stringForChecking, minValue, maxValue, coefficient):
    while True:
        try:
            print('Please input ' + stringForChecking + ': ')
            value = int(input())
            if value < minValue or value > maxValue:
                raise NameError
            break
        except NameError:
            print('Number can be between ' + str(minValue) + ' and ' + str(maxValue))
        except ValueError:
            print('Input integer value please')
    if not coefficient:
        return value
    return value / 100


def infectionProcess(state, numberOfPeople, coefficientOfAntibodies, coefficientOfCapacity, numberOfSimulations):
    simulationListOfInfectedPeople = []
    simulationHospitalWorkloadList = []
    simulationAverageReproductionList = []

    for l in range(numberOfSimulations):
        averageReproductionList = []
        hospitalWorkloadList = []
        listOfInfectedPeople = []
        hospitalWorkload = 0
        for k in range(100):
            numberOfPeopleInfectedWithVirus = 0
            infectionList = []
            infectionListForVacationers = []
            reproductionNumberList = []

            for i in range(numberOfPeople):
                # change health condition
                # infection among workers
                if (state[i][2] == 1) and (
                        state[i][4] > 0) and (state[i][3] > 0) and (i not in infectionList):

                    workingIndicator = state[i][1]
                    infectionList.append(i)
                    infectionProducingContacts = 0
                    # reduce incubation period
                    state[i][4] = state[i][4] - 1
                    for j in range(numberOfPeople):
                        if (state[j][1] == workingIndicator) and (state[j][3] > 0) and (state[j][2] == 0) and (
                                state[j][6] == 0) and (j not in infectionList):
                            probabilityBeenInfected = state[j][0] * state[j][1]
                            randomValue = random.random()
                            if randomValue <= probabilityBeenInfected:
                                state[j][2] = 1
                                state[j][4] = 5
                                infectionList.append(j)
                                infectionProducingContacts = infectionProducingContacts + 1

                        # for people without work
                        if (state[i][1]) == 0.14 and (state[i][3] == 1) and (state[j][3] == 2) and \
                                (state[j][2] == 0) and (
                                state[j][6] == 0) and (j not in infectionList):
                            probabilityBeenInfected = state[j][0] * state[j][1]
                            randomValue = random.random()
                            if randomValue <= probabilityBeenInfected:
                                state[j][2] = 1
                                state[j][4] = 5
                                infectionList.append(j)
                                infectionProducingContacts = infectionProducingContacts + 1
                    reproductionNumberList.append(infectionProducingContacts)

                # infection among people who have a rest
                if (state[i][2] == 1) and (
                        state[i][4] > 0) and ((state[i][3] == 0) or
                                              (state[i][3] == 2)) and (i not in infectionListForVacationers):

                    # reduce incubation period
                    state[i][4] = state[i][4] - 1
                    infectionProducingContacts = 0
                    infectionListForVacationers.append(i)
                    for j in range(numberOfPeople):
                        if (state[j][3] == 0) and (state[j][6] == 0) and (
                                state[j][2] == 0) and j not in infectionListForVacationers:
                            probabilityBeenInfected = state[j][0] * 0.03
                            randomValue = random.random()
                            if randomValue <= probabilityBeenInfected:
                                print(str(i) + ' infect ' + str(j))
                                state[j][2] = 1
                                state[j][4] = 5
                                infectionListForVacationers.append(j)
                                infectionProducingContacts = infectionProducingContacts + 1

                        # shop workers
                        if (state[i][1]) == 0.01 and (state[j][3] == 1) and \
                                (state[j][2] == 0) and (
                                state[j][6] == 0) and (j not in infectionList):
                            probabilityBeenInfected = state[j][0] * state[j][1]
                            randomValue = random.random()
                            if randomValue <= probabilityBeenInfected:
                                print(str(i) + ' infect ' + str(j))
                                state[j][2] = 1
                                state[j][4] = 5
                                infectionList.append(j)
                                infectionProducingContacts = infectionProducingContacts + 1
                    reproductionNumberList.append(infectionProducingContacts)
                # change from hospital to work again or reduce number of days in hospital
                if state[i][6] == 1:
                    state[i][6] = 0
                    # change health condition after hospital
                    state[i][2] = 0
                    state[i][0] = state[i][0] * coefficientOfAntibodies
                    hospitalWorkload = hospitalWorkload - 1
                elif state[i][6] > 1:
                    state[i][6] = state[i][6] - 1
                # change from incubation period to hospital form 1 to 2
                if (state[i][4] == 0) and (state[i][2] == 1) \
                        and (hospitalWorkload < numberOfPeople * coefficientOfCapacity):
                    state[i][2] = 2
                    state[i][6] = 7
                    hospitalWorkload = hospitalWorkload + 1
                elif (state[i][4] == 0) and (state[i][2] == 1) \
                        and (hospitalWorkload >= numberOfPeople * coefficientOfCapacity):
                    state[i][4] = state[i][4] + 1
                # change shift at work
                if (state[i][3] == 1) and (state[i][5] > 1):
                    state[i][5] = state[i][5] - 1
                # change shift for hospitals and schoolWorkers
                elif (state[i][3] == 1) and (state[i][5] == 1) \
                        and ((state[i][1] == 0.3) or (state[i][1] == 0.08)):
                    state[i][3] = 0
                    state[i][5] = 3
                elif (state[i][3] == 1) and (state[i][5] == 1):
                    state[i][3] = 0
                    state[i][5] = 2
                elif (state[i][3] == 0) and (state[i][5] > 1):
                    state[i][5] = state[i][5] - 1
                # change shift at work for schoolWorkers
                elif (state[i][3] == 0) and (state[i][5] == 1) and (state[i][1] == 0.08):
                    state[i][3] = 1
                    state[i][5] = 4
                # change shift for hospitals
                elif (state[i][3] == 0) and (state[i][5] == 1) and (state[i][1] == 0.3):
                    state[i][3] = 1
                    state[i][5] = 3
                elif (state[i][3] == 0) and (state[i][5] == 1):
                    state[i][3] = 1
                    state[i][5] = 2

            hospitalWorkloadList.append(hospitalWorkload)
            print(hospitalWorkloadList)
            # calculate average reproduction number per day
            if len(reproductionNumberList) > 0:
                averageReproductionList.append(round(sum(reproductionNumberList) / len(reproductionNumberList), 2))
            else:
                averageReproductionList.append(0.00)

            for i in range(numberOfPeople):
                if state[i][2] == 1:
                    numberOfPeopleInfectedWithVirus = numberOfPeopleInfectedWithVirus + 1
                if i == numberOfPeople - 1:
                    listOfInfectedPeople.append(numberOfPeopleInfectedWithVirus)

        simulationListOfInfectedPeople.append(listOfInfectedPeople)
        simulationHospitalWorkloadList.append(hospitalWorkloadList)
        simulationAverageReproductionList.append(averageReproductionList)

    return simulationAverageReproductionList, simulationHospitalWorkloadList, simulationListOfInfectedPeople


def calculateAverage(simulationAverageReproductionList,
                     simulationHospitalWorkloadList,
                     simulationListOfInfectedPeople):
    averageSimulationListOfInfectedPeople = []
    averageSimulationHospitalWorkloadList = []
    averageSimulationAverageReproductionList = []
    for i in range(100):
        summaInfected = 0
        summaWorkload = 0
        summaReproductionList = 0
        for j in range(len(simulationListOfInfectedPeople)):
            summaInfected += simulationListOfInfectedPeople[j][i]
            summaWorkload += simulationHospitalWorkloadList[j][i]
            summaReproductionList += simulationAverageReproductionList[j][i]
            if j == len(simulationListOfInfectedPeople) - 1:
                averageSimulationListOfInfectedPeople.append(
                    (summaInfected / len(simulationListOfInfectedPeople)))
                averageSimulationHospitalWorkloadList.append(
                    (summaWorkload / len(simulationHospitalWorkloadList)))
                averageSimulationAverageReproductionList.append(
                    (summaReproductionList / len(simulationAverageReproductionList)))
    return averageSimulationListOfInfectedPeople, averageSimulationAverageReproductionList, averageSimulationHospitalWorkloadList


def infection():
    # input data
    numberOfSimulations = checking('number of simulations', 1, 20, False)
    numberOfPeople = checking('number of people', 100, 1000, False)
    coefficientOfCapacity = checking('hospital capacity (percentage of all people)', 20, 60, True)
    coefficientOfAntibodies = checking('probability been infected after hospital (antibodies effectiveness)',
                                       60, 100, True)

    # initialization
    state = initialization(numberOfPeople)

    # change state
    simulationAverageReproductionList, simulationHospitalWorkloadList, simulationListOfInfectedPeople = \
        infectionProcess(state, numberOfPeople, coefficientOfAntibodies, coefficientOfCapacity, numberOfSimulations)

    # calculating average data
    avSimulationListOfInfectedPeople, avSimulationAverageReproductionList, avSimulationHospitalWorkloadList = calculateAverage(
        simulationAverageReproductionList,
        simulationHospitalWorkloadList,
        simulationListOfInfectedPeople)

    # making plots
    plotsMaker(avSimulationListOfInfectedPeople,
               avSimulationAverageReproductionList,
               avSimulationHospitalWorkloadList)


if __name__ == '__main__':
    infection()
