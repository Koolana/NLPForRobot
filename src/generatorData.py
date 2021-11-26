import re
import random
from itertools import chain
from generatorSentence import generateSent

f = open('ru.conversations.txt', 'r')
data = f.read().lower()
dataDialogs = data.split('\n\n')
# print(dataDialogs[0])

dataSec = [dialog.split('\n') for dialog in dataDialogs]
# print(dataSec[0])

dataSec = [[re.sub('\W+',' ', oneStr).strip() for oneStr in dialog] for dialog in dataSec]
# print(*dataSec[0:10], sep='\n')

filteredData = [[oneStr for oneStr in dialog if (len(oneStr.split(' ')) >= 5 and len(oneStr.split(' ')) < 10)] for dialog in dataSec]
filteredData = [oneStr for oneStr in filteredData if oneStr]
filteredData = list(chain.from_iterable(filteredData))[:160]
filteredData = [[data, 0] for data in filteredData]

sents = generateSent(len(filteredData))
print(*[i for i in sents], sep='\n')

outputData = filteredData

for sent in sents:
    outputData.append([sent[1], 1])

random.shuffle(outputData)
# print(*outputData[0:200], sep='\n')

f = open('outputdataDirty.csv', 'w')
for oneStr in outputData:
    f.write(oneStr[0] + ',' + str(oneStr[1]) + '\n')

f = open('outputdataClean.csv', 'w')
for sent in sents:
    f.write(sent[1] + ',' + sent[0] + '\n')
