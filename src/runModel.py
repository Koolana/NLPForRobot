################### Задача seg2seg предложений содержащих команду ###################

# датасет в файле outputdataClean.csv формата: str(sentence),str(robot_sentence)

import torch

from transformers import RobertaTokenizer
from wrapperRobertaTokenizer import WrapperRobertaTokenizer
from decoderTokenizer import DecoderTokenizer
from dataProcessing import ensureLength
from model import createModel

from lemmDataFromFile import sentsLemmatization

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
    pathToRoberta = '../models/ruRoberta-large'
    pathToModel = '../models/robot-brain-v2.pt'

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Используется:', device)

    translater = Translater(pathToRoberta, pathToModel, device)

    inputSent = input('Введите предложение: ')
    print('Ввод:', inputSent)
    print('Вывод:', translater.recognizeCmd(inputSent))
