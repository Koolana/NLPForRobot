from transformers import RobertaTokenizer
from wrapperRobertaTokenizer import WrapperRobertaTokenizer
from decoderTokenizer import DecoderTokenizer
from dataProcessing import DataCreater
from model import createModel
from trainer import Trainer

import torch
import time
import math
import pickle
from tqdm import tqdm

if __name__ == '__main__':
    pathToRoberta = '../models/ruRoberta-large'
    pathToDataset = '../datasets/outputdataClean.csv'
    pathToOutputModel = '../models/robot-brain-v2.pt'
    numData = 50000
    numEpochs = 10
    clip = 1

    tokenizerRoberta = RobertaTokenizer.from_pretrained(pathToRoberta)
    tokenizerEnc = WrapperRobertaTokenizer(tokenizerRoberta)
    tokenizerDec = DecoderTokenizer(tokenizerEnc)

    dataCreater = DataCreater(tokenizerEnc.convertSentToIds,
                              tokenizerDec.convertSentToIds,
                              path=pathToDataset,
                              numData=numData)

    trainDataLoader, valDataLoader = dataCreater.getDataLoaders()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Используется:', device)

    model = createModel(device)
    trainer = Trainer(model, trainDataLoader, valDataLoader, device)

    print(f'The model has {trainer.count_parameters():,} trainable parameters')

    best_valid_loss = float('inf')
    bestModel = None

    for epoch in tqdm(range(numEpochs)):

        start_time = time.time()

        train_loss = trainer.train(clip)
        valid_loss = trainer.evaluate()

        end_time = time.time()

        if valid_loss < best_valid_loss:
            best_valid_loss = valid_loss
            bestModel = pickle.loads(pickle.dumps(model))

        print(f'\tTrain Loss: {train_loss:.3f} | Train PPL: {math.exp(train_loss):7.3f}')
        print(f'\t Val. Loss: {valid_loss:.3f} |  Val. PPL: {math.exp(valid_loss):7.3f}')

    torch.save(bestModel.state_dict(), pathToOutputModel)
    print('Training has been finished!')
    print('Saved to', pathToOutputModel)
