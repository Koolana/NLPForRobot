import random
import re

moveCmd = ['поезжай', 'сгоняй', 'доберись', 'переместись', 'приедь', 'прибудь', 'заедь', 'иди', 'съезди']
places = ['пункт NUM', 'кабинет NUM', 'аудитория NUM', 'отдел кадров', 'медпункт', 'библиотека']
objs = ['документ', 'чашка', 'работа', 'груз', 'объект', 'прибор']
actions = ['принеси', 'возьми', 'доставь', 'отвези', 'захвати', 'забери']
please = ['пожалуйста', '', 'будь добр']
dirF = ['туда']
dirB = ['оттуда', 'сюда']
back = ['и MOVE_CMD назад', 'и возвращайся', 'и MOVE_CMD обратно']

dictTargets = {'BACK' : back,
               'MOVE_CMD' : moveCmd,
               'PLEASE' : please,
               'PLACE_1' : places,
               'ACTION' : actions,
               'DIR_F' : dirF,
               'DIR_B' : dirB,
               'OBJ' : objs,
               'PLACE_2' : places,
               'NUM' : [str(i) for i in range(0, 1000)]}

cmdTemplate = ['взять(OBJ) движение(PLACE_1)',
               'движение(PLACE_1) взять(OBJ) движение(обратно)',
               'взять(OBJ) движение(PLACE_1) движение(обратно)',
               'движение(PLACE_1) взять(OBJ) движение(PLACE_2)']

sentTemplate = [[0, 'MOVE_CMD PLEASE в PLACE_1 и ACTION DIR_F OBJ'],
                [2, 'MOVE_CMD PLEASE в PLACE_1 и ACTION DIR_F OBJ BACK'],
                [1, 'MOVE_CMD PLEASE в PLACE_1 и ACTION DIR_B OBJ'],
                [0, 'MOVE_CMD PLEASE в PLACE_1 и ACTION OBJ DIR_F'],
                [2, 'MOVE_CMD PLEASE в PLACE_1 и ACTION OBJ DIR_F BACK'],
                [1, 'MOVE_CMD PLEASE в PLACE_1 и ACTION OBJ DIR_B'],
                [1, 'ACTION OBJ PLEASE из PLACE_1'],
                [1, 'PLEASE ACTION OBJ из PLACE_1'],
                [0, 'ACTION OBJ PLEASE в PLACE_1'],
                [0, 'PLEASE ACTION OBJ в PLACE_1'],
                [0, 'ACTION OBJ в PLACE_1'],
                [2, 'ACTION OBJ PLEASE в PLACE_1 BACK'],
                [2, 'PLEASE ACTION OBJ в PLACE_1 BACK'],
                [2, 'ACTION OBJ в PLACE_1 BACK']]

def generateSent(numSent):
    sents = []
    for i in range(numSent):
        template = sentTemplate[random.randint(0, len(sentTemplate) - 1)]
        # template = sentTemplate[11]

        sent = template[1]
        cmd = cmdTemplate[template[0]]
        for target in dictTargets.keys():
            objFromLabel = dictTargets[target][random.randint(0, len(dictTargets[target]) - 1)]
            sent = sent.replace(target, objFromLabel)
            cmd = cmd.replace(target, objFromLabel)

        sent = re.sub(r'\s+', ' ', sent)
        sents.append([cmd, sent])

    return sents
