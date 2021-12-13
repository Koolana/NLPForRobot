from transformers import RobertaTokenizer
from wrapperRobertaTokenizer import WrapperRobertaTokenizer
from decoderTokenizer import DecoderTokenizer
from dataProcessing import DataCreater
from model import createModel
from trainer import Trainer
from utils import getConsoleArgs

import torch
import time
import math
import pickle
from tqdm import tqdm

if __name__ == '__main__':
    pathToRoberta = None
    pathToDataset = None
    pathToOutputModel = None

    numData = 10000
    numEpochs = 10
    clip = 1

    inputArgv = getConsoleArgs()

    if 'data' in inputArgv and inputArgv['data'] is not None:
        pathToDataset = inputArgv['data']
    else:
        print('Invalid parameter \'data\'')
        exit()

    if 'roberta' in inputArgv and inputArgv['roberta'] is not None:
        pathToRoberta = inputArgv['roberta']
    else:
        print('Invalid parameter \'roberta\'')
        exit()

    if 'model' in inputArgv and inputArgv['model'] is not None:
        pathToOutputModel = inputArgv['model']
    else:
        print('Invalid parameters \'model\'')
        exit()

    if 'num' in inputArgv and inputArgv['num'] is not None:
        numData = int(inputArgv['num'])

    if 'epoch' in inputArgv and inputArgv['epoch'] is not None:
        numEpochs = int(inputArgv['epoch'])

    tokenizerRoberta = RobertaTokenizer.from_pretrained(pathToRoberta)
    tokenizerEnc = WrapperRobertaTokenizer(tokenizerRoberta)
    tokenizerDec = DecoderTokenizer(tokenizerEnc)

    dataCreater = DataCreater(tokenizerEnc.convertSentToIds,
                              tokenizerDec.convertSentToIds,
                              path=pathToDataset,
                              numData=numData)

    trainDataLoader, valDataLoader = dataCreater.getDataLoaders()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Use:', device)

    model = createModel(device)
    trainer = Trainer(model, trainDataLoader, valDataLoader, device)

    print(f'The model has {trainer.count_parameters():,} trainable parameters')

    print('Start training...')
    print('\tNumber of data for training:', numData)
    print('\tNumber of epochs:', numEpochs)

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

        print(f'\n\tTrain Loss: {train_loss:.3f} | Train PPL: {math.exp(train_loss):7.3f}')
        print(f'\t Val. Loss: {valid_loss:.3f} |  Val. PPL: {math.exp(valid_loss):7.3f}')

    torch.save(bestModel.state_dict(), pathToOutputModel)
    print('Training has been finished!')
    print('Saved to', pathToOutputModel)
