################### Задача seg2seg предложений содержащих команду ###################

# датасет в файле outputdataClean.csv формата: str(sentence),str(robot_sentence)

from transformers import RobertaTokenizer
from decoderTokenizer import DecoderTokenizer
from dataProcessing import DataCreater

from lemmDataFromFile import extractDataAndLemmatization

class WrapperRobertaTokenizer():
    def __init__(self, tokeniser):
        self.tokeniser = tokeniser

    def convertTokenToIds(self, token):
        return self.tokeniser(token)['input_ids'][1:-1]

    def convertSentToIds(self, sent):
        return [1] + [item for sublist in sent.split() for item in self.convertTokenToIds(sublist)] + [2]

    def convertIdsToSent(self, ids):
        return self.tokeniser.convert_ids_to_tokens(ids[i])

if __name__ == '__main__':
    tokenizerRoberta = RobertaTokenizer.from_pretrained('../models/ruRoberta-large')
    tokenizerEnc = WrapperRobertaTokenizer(tokenizerRoberta)
    tokenizerDec = DecoderTokenizer(tokenizerEnc)

    dataCreater = DataCreater(tokenizerEnc.convertSentToIds, tokenizerDec.convertSentToIds)
    # print(dataCreater.dataSource[0], dataCreater.idsSource[0])
    # print(dataCreater.dataTarget[0], dataCreater.idsTarget[0])
    trainDataLoader, valDataLoader = dataCreater.getDataLoaders()

    # data = extractDataAndLemmatization('../datasets/outputdataClean.csv')
    #
    # ### Некоторые действия на data ###
    # print(*data[:10], sep='\n')
