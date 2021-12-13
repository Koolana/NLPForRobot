################### Задача seg2seg предложений содержащих команду ###################

# датасет в файле outputdataClean.csv формата: str(sentence),str(robot_sentence)

import re
import sys
import torch
from torchtext.data.metrics import bleu_score

import numpy
import sklearn.metrics

from transformers import RobertaTokenizer
from wrapperRobertaTokenizer import WrapperRobertaTokenizer
from decoderTokenizer import DecoderTokenizer
from dataProcessing import ensureLength
from model import createModel
from dataProcessing import DataCreater

from lemmDataFromFile import sentsLemmatization

def getConsoleArgs():
    """
    Returns a dictionary of arguments passed to through the CLI.
    """

    args = {}

    for arg in sys.argv[1:]:
        var = re.search('\-\-([A-Za-z]*)', arg) # optional value assignment
        var = var.group(1)
        value = re.search('\=(.*)', arg)
        value = value.group(1) if value else None
        args[var] = value

    return args

def calculateMetrics(pathToRoberta, pathToModel, pathToData, device):
    tokenizerRoberta = RobertaTokenizer.from_pretrained(pathToRoberta)
    tokenizerEnc = WrapperRobertaTokenizer(tokenizerRoberta)
    tokenizerDec = DecoderTokenizer(tokenizerEnc)

    model = createModel(device)
    model.load_state_dict(torch.load(pathToModel))

    dataCreater = DataCreater(tokenizerEnc.convertSentToIds,
                              tokenizerDec.convertSentToIds,
                              path=pathToData,
                              numData=100)

    testDataLoader, _ = dataCreater.getDataLoaders(splitValue=1, batchSize=1)

    trgs = []
    pred_trgs = []
    accs = []

    for datum in testDataLoader:
        src = datum[0][0].tolist()
        trg = datum[1][0].tolist()

        trgTokens = tokenizerDec.convertIdsToSent(trg, src)

        predTrg, _ = translate_sentence(src, 0, 0, model, device, 50)
        predTrg = ensureLength(predTrg)

        r = sklearn.metrics.confusion_matrix(trg, predTrg)
        r = numpy.flip(r)

        acc = (r[0][0] + r[-1][-1]) / numpy.sum(r)
        accs.append(acc)

        predTokens = tokenizerDec.convertIdsToSent(ensureLength(predTrg), src)

        trgs.append([trgTokens])
        pred_trgs.append(predTokens)

    return bleu_score(pred_trgs, trgs), sum(accs) / len(accs)

def translate_sentence(inputIds, src_field, trg_field, model, device, max_len=50):
    model.eval()

    src_tensor = torch.LongTensor(inputIds).unsqueeze(0).to(device)

    src_mask = model.make_src_mask(src_tensor)

    with torch.no_grad():
        enc_src = model.encoder(src_tensor, src_mask)

    trg_indexes = [1]

    for i in range(max_len):
        trg_tensor = torch.LongTensor(trg_indexes).unsqueeze(0).to(device)

        trg_mask = model.make_trg_mask(trg_tensor)

        with torch.no_grad():
            output, attention = model.decoder(trg_tensor, enc_src, trg_mask, src_mask, src_tensor)

        pred_token = output.argmax(2)[:, -1].item()

        trg_indexes.append(pred_token)

        if pred_token == 2:
            break

    return trg_indexes, attention

class Translater():
    def __init__(self, pathToRoberta, pathToModel, device):
        self.pathToRoberta = pathToRoberta
        self.pathToModel = pathToModel
        self.device = device

        self.tokenizerRoberta = RobertaTokenizer.from_pretrained(self.pathToRoberta)
        self.tokenizerEnc = WrapperRobertaTokenizer(self.tokenizerRoberta)
        self.tokenizerDec = DecoderTokenizer(self.tokenizerEnc)

        self.model = createModel(self.device)
        self.model.load_state_dict(torch.load(self.pathToModel))

    def recognizeCmd(self, inputSent):
        # inputSent = ' '.join(*sentsLemmatization(inputSent))  # лемматизация
        src = ensureLength(self.tokenizerEnc.convertSentToIds(inputSent), 50, 0)

        translation, attention = translate_sentence(src, 0, 0, self.model, self.device)

        textTarget = self.tokenizerDec.convertIdsToSent(translation, src)

        return textTarget

if __name__ == '__main__':
    pathToRoberta = None
    pathToModel = None
    pathToData = None

    inputArgv = getConsoleArgs()

    if 'metric' in inputArgv and inputArgv['metric'] is not None:
        pathToData = inputArgv['metric']

    if 'roberta' in inputArgv and inputArgv['roberta'] is not None:
        pathToRoberta = inputArgv['roberta']
    else:
        print('Invalid parameter \'roberta\'')
        exit()

    if 'model' in inputArgv and inputArgv['model'] is not None:
        pathToModel = inputArgv['model']
    else:
        print('Invalid parameters \'model\'')
        exit()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Используется:', device)

    if pathToData is not None:
        print('On metric mode')
        print('BLUE score: {0:.3}, accuracy: {1:.3}'.format(*calculateMetrics(pathToRoberta, pathToModel, pathToData, device)))
    else:
        print('On recognition mode')
        translater = Translater(pathToRoberta, pathToModel, device)

        while True:
            inputSent = input('Введите предложение: ')
            print('Ввод:', inputSent)

            cdmSent = translater.recognizeCmd(inputSent)
            cdmSent = ' '.join(cdmSent)
            cdmSent = re.sub('(\d+)([а-яА-Яa-zA-Z])', r'\1 \2', cdmSent)
            cdmSent = re.sub('([а-яА-Яa-zA-Z])(\d+)', r'\1 \2', cdmSent)
            cdmSent = re.sub('\s+', r' ', cdmSent).strip()
            print('Вывод:', cdmSent)
