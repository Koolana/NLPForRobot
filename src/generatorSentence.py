import random
import re

moveCmd = ['поезжай', 'сгоняй', 'доберись', 'дойди', 'переместись', 'приедь', 'прибудь', 'заедь', 'иди', 'съезди']
preposition = ['и', 'и затем', 'а затем', 'и потом', 'а потом', 'и после', 'а после', 'затем','потом','после','после этого','а после этого', 'и после этого']
places = ['пункт NUM', 'кабинет NUM', 'аудитория NUM', 'отдел кадров', 'медпункт', 'библиотека']
objs = ['документ', 'документация', 'чашка', 'кружка','пенал', 'работа', 'груз', 'объект', 'прибор', 'ножницы','яблоко']
actions = ['принеси', 'отнеси', 'занеси', 'возьми', 'доставь', 'отвези', 'довези', 'захвати', 'забери', 'передай']
please = ['пожалуйста', '']
be_kind = ['будь добр', '']

dirF = ['туда']
dirB = ['оттуда', 'сюда']

back = [' PRE MOVE_CMD назад', ' PRE возвращайся', ' PRE MOVE_CMD обратно', ' PRE MOVE_CMD на прежнее место']

may = ['можешь', 'можете', 'попробуй']
moveCmd_with_may = ['поехать','сгонять','добраться','переместиться','приехать','прибыть','заехать','пойти', 'дойти','съездить']
actions_with_may = ['принести', 'отнести', 'занести', 'взять', 'доставить', 'отвезти', 'довезти', 'захватить', 'забрать', 'передать']
back_with_may = [' PRE M_MOV_CMD назад', ' PRE вернуться', ' PRE M_MOV_CMD обратно', ' PRE M_MOV_CMD на прежнее место']

dictTargets = {
               'BACK' : back,
               'M_BAC' : back_with_may,
               'MAY' : may,
               'MOVE_CMD' : moveCmd,
               'M_MOV_CMD' : moveCmd_with_may,
               'PLEASE' : please,
               'BE_KIND' : be_kind,
               'PRE' : preposition,
               'PLACE_1' : places,
               'ACTION' : actions,
               'M_ACT' : actions_with_may,
               'DIR_F' : dirF,
               'DIR_B' : dirB,
               'OBJ' : objs,
               'PLACE_2' : places,
               'NUM' : [str(i) for i in range(0, 1000)]}

cmdTemplate = ['взять(OBJ) движение(PLACE_1)',
               'движение(PLACE_1) взять(OBJ) движение(обратно)',
               'взять(OBJ) движение(PLACE_1) движение(обратно)',
               'движение(PLACE_1) взять(OBJ) движение(PLACE_2)']

sentTemplate = [[0, 'BE_KIND MOVE_CMD PLEASE в PLACE_1 и ACTION DIR_F OBJ'],        # 0
                [2, 'BE_KIND MOVE_CMD PLEASE в PLACE_1 и ACTION DIR_F OBJ BACK'],   # 1
                [1, 'BE_KIND MOVE_CMD PLEASE в PLACE_1 и ACTION DIR_B OBJ'],        # 2
                [0, 'BE_KIND MOVE_CMD PLEASE в PLACE_1 и ACTION OBJ DIR_F'],        # 3
                [2, 'BE_KIND MOVE_CMD PLEASE в PLACE_1 и ACTION OBJ DIR_F BACK'],   # 4
                [1, 'BE_KIND MOVE_CMD PLEASE в PLACE_1 и ACTION OBJ DIR_B'],        # 5
                [1, 'ACTION OBJ PLEASE из PLACE_1'],                                # 6
                [1, 'PLEASE ACTION OBJ из PLACE_1'],                                # 7
                [0, 'ACTION OBJ PLEASE в PLACE_1'],                                 # 8
                [0, 'PLEASE ACTION OBJ в PLACE_1'],                                 # 9
                [0, 'ACTION OBJ в PLACE_1'],                                        # 10
                [2, 'ACTION OBJ PLEASE в PLACE_1 BACK'],                            # 11
                [2, 'PLEASE ACTION OBJ в PLACE_1 BACK'],                            # 12
                [2, 'ACTION OBJ в PLACE_1 BACK'],                                   # 13
                [0, 'MAY M_MOV_CMD PLEASE в PLACE_1 и M_ACT DIR_F OBJ'],            # 14
                [2, 'MAY M_MOV_CMD PLEASE в PLACE_1 и M_ACT DIR_F OBJ M_BAC'],      # 15
                [1, 'MAY M_MOV_CMD PLEASE в PLACE_1 и M_ACT DIR_B OBJ'],            # 16
                [0, 'MAY M_MOV_CMD PLEASE в PLACE_1 и M_ACT OBJ DIR_F'],            # 17
                [2, 'MAY M_MOV_CMD PLEASE в PLACE_1 и M_ACT OBJ DIR_F M_BAC'],      # 18
                [1, 'MAY M_MOV_CMD PLEASE в PLACE_1 и M_ACT OBJ DIR_B'],            # 19
                [1, 'MAY M_ACT OBJ PLEASE из PLACE_1'],                             # 20
                [1, 'PLEASE MAY M_ACT OBJ из PLACE_1'],                             # 21
                [0, 'MAY M_ACT OBJ PLEASE в PLACE_1'],                              # 22
                [0, 'PLEASE MAY M_ACT OBJ в PLACE_1'],                              # 23
                [0, 'MAY M_ACT OBJ в PLACE_1'],                                     # 24                       
                [2, 'MAY M_ACT OBJ PLEASE в PLACE_1 M_BAC'],                        # 25
                [2, 'PLEASE MAY M_ACT OBJ в PLACE_1 M_BAC'],                        # 26
                [2, 'MAY M_ACT OBJ в PLACE_1 M_BAC']                                # 27
                ]   

def generateSent(numSent):
    sents = []
    for i in range(numSent):
        template = sentTemplate[random.randint(0, len(sentTemplate) - 1)] # random.randint(0, len(sentTemplate) - 1)
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
