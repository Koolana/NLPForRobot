from torch.utils.data import Dataset, DataLoader

import csv

class TextDataset(Dataset):
    def __init__(self, idsTokenizedSource, idsTokenizedTarget, sentLen=50, padValue=0):
        self.idsTokenizedSource = idsTokenizedSource
        self.idsTokenizedTarget = idsTokenizedTarget
        self.sentLen = sentLen

    def __getitem__(self, item):
        return torch.tensor(self.ensureLength(self.idsTokenizedSource[item])), \
               torch.tensor(self.ensureLength(self.idsTokenizedTarget[item]))

    def __len__(self):
        return len(self.idsTokenizedSource)

    def ensureLength(self, txt):
        if len(txt) < self.sentLen:
            txt = list(txt) + [pad_value] * (self.sentLen - len(txt))
        else:
            txt = txt[:self.sentLen]
        return txt

class DataCreater():
    def __init__(self, tokenizerSource, tokenizerTarget, path='../datasets/outputdataClean.csv', numData=2000):
        self.numData = numData
        self.tokenizerSource = tokenizerSource
        self.tokenizerTarget = tokenizerTarget
        self.dataSource, self.dataTarget = self.readFromCSV(path)

        self.idsSource, self.idsTarget = self.createIdsTokens()

    def readFromCSV(self, path):
        dataText = []
        dataLabel = []
        with open(path, newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', )
            next(reader)
            for row in reader:
                text, label = row
                if label is not None and len(label):
                    dataText.append(text)
                    dataLabel.append(label)

        return dataText, dataLabel

    def createIdsTokens(self):
        idsSource = [self.tokenizerSource(t) for t in self.dataSource[:self.numData]]
        idsTarget = [self.tokenizerTarget(t, refT) for t,refT in zip(self.dataTarget[:self.numData], idsSource)]

        return idsSource, idsTarget

    def getDataLoaders(self, splitValue=0.8, batchSize=32):
        trainDataset = TextDataset(self.idsSource[:int(len(self.idsSource)*splitValue)],
                                   self.idsTarget[:int(len(self.idsTarget)*splitValue)])
        valDataset = TextDataset(self.idsSource[int(len(self.idsSource)*splitValue):],
                                 self.idsTarget[int(len(self.idsTarget)*splitValue):])

        trainDataloader = DataLoader(trainDataset,
                                      batch_size=batchSize,
                                      shuffle=True
                                     )
        valDataloader = DataLoader(valDataset,
                                    batch_size=batchSize,
                                    shuffle=False
                                   )
        return trainDataloader, valDataloader
