import csv
import sys

def loadCSV(file):
    return list(csv.reader(open(file)))
    
def getCol(data, qCol):
    return [row[qCol] for row in data]

class Respondent:
    def __init__(self, response, id):
        super().__init__()
        self.response = response
        self.id = id

    def getQuestion(self, qNum):
        return self.response[qNum]

class ResultsByCol:
    def __init__(self, respondants, numQs):
        super().__init__()
        self.prompt = []
        self.responses = self.sortByQ(respondants, numQs)
        self.final = []
        i = 0
        self.getPrompts()
        while i < numQs:
            self.final.append(self.getTallyPercByQ(i))
            i+=1

    def getPrompts(self):
         for val in self.responses:
            self.prompt.append(val.pop(0))

        
    def printAll(self):
        for i,q in enumerate(self.final):
            print(self.prompt[i])
            for x,y in q.items():
                print(x, '->', y * 100, '%')
            print('\n')

    def getTallyPercByQ(self, col):
        tally = {}
        for val in self.responses[col]:
            for response in val.split(';'):
                if tally.get(response) is None:
                    tally[response] = 1
                else:
                    tally[response] += 1 
        sum = 0
        for _, t in tally.items():
            sum += t

        tallyPerc = {}
        for resp, t in tally.items():
            tallyPerc[resp] = t / sum

        return tallyPerc

    def sortByQ(self, respondants, numQs):
        x = 0
        responses = []

        while x < numQs:
            responses.append([respondant.getQuestion(x) for respondant in respondants])
            x += 1
        return responses

def selectData(respondants, qNum, response):

    temp = [respondant for respondant in respondants if respondant.getQuestion(qNum) in response and respondant.getQuestion(qNum) is not '']
    temp2 = [respondants[0]] + temp

    return temp2

def main():
    data = loadCSV('results.csv')
    respondants = []

    for index, response in enumerate(data):
        respondants.append(Respondent(response, index))






    print('Enter number of questions in your survey')
    numQs = input()
    print('Do you want to filter?(y/n)')
    input1 = input()

    if input1 is "y":
        print('Select Question you wish to filter by: ')
        filterQ = int(input())
        print('Select Responses you wish to count')
        respFilter = input()
        respondants = selectData(respondants, filterQ, respFilter)
        
    res = ResultsByCol(respondants,21)
    res.printAll()





if __name__ == "__main__":
    main()
