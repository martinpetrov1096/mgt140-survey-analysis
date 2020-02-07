import csv

def loadCSV(file):
    return list(csv.reader(open(file)))
    
def getCol(data, qCol):
    return [row[qCol] for row in data]

# Tally up the number of times each response to a question occurred


class QResult:
    def __init__(self, col):
        self.q = ""
        self.sum = 0
        self.responseTally = {}
        self.respTallyPerc = {}
        self.setRespTally(col)

    def setRespTally(self, col):
        self.q = col.pop(0)
       
        for val in col:
            for response in val.split(';'):
                if self.responseTally.get(response) is None:
                    self.responseTally[response] = 1
                else:
                    self.responseTally[response] += 1

    def sumResponses(self):
        for _, tally in self.responseTally.items():
            self.sum += tally

    def toPercent(self):
        for response, tally in self.responseTally.items():
            self.respTallyPerc[response] = tally / self.sum

    def print(self):
        print(self.q)
        for response,percent in self.respTallyPerc.items():
            print(response, '->', percent * 100, '%')
        print('\n')


class Respondent:
    def __init__(self, response, id):
        super().__init__()
        self.response = response
        self.id = id
    
    def getQuestion(self, qNum):
        return self.response[qNum]

    def crossTab(self, qNum1, rNum1, qNum2):
        temp = {}
        temp[self.getQuestion(qNum1)] = self.getQuestion(qNum2)
        return temp


def crossAnalyze(respondants, qNum1, response, qNum2):
    ids = []
    
    for respondant in respondants:
        if respondant.response[qNum1] in response:
            ids.append(respondant.id)


    data2 = []
    for Id in ids:
        data2.append(respondants[Id].response)

    cols2 = []
    j = 0
    while j < 21:
        cols2.append(getCol(data2,j))
        j+=1
    qResults2 = []
    for col in cols2:
        qResults2.append(QResult(col))

    for q in qResults2:
        q.sumResponses()
        q.toPercent()
        q.print()


def main():
    data = loadCSV('results.csv')
    respondants = []
    qResults = []


    # Cols contains the responses to each question
    cols = []
    i = 0
    while i < 21:
        cols.append(getCol(data,i))
        i+=1
 
    # Tally up the responses for each column
    
    for col in cols:
        qResults.append(QResult(col))

    for q in qResults:
        q.sumResponses()
        q.toPercent()
        #q.print()
    
    
    x = 0
    for response in data:
        respondants.append(Respondent(response, x))
        x+=1
        
    ids = crossAnalyze(respondants, 2, 'Senior', 3)
    
    
    

if __name__ == "__main__":
    main()