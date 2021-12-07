import random
import re

moveCmd = ['поезжай', 'сгоняй', 'следуй','доберись', 'дойди', 'переместись', 'приедь', 'прибудь', 'заедь', 'иди','пойди','зайди','сходи', 'съезди']
preposition = ['и', 'и затем', 'а затем', 'и потом', 'а потом', 'и после', 'а после', 'затем','потом','после','после этого','а после этого', 'и после этого','после чего','а после чего', 'и после чего']
places = ['пункт NUM', 'кабинет NUM', 'аудитория NUM', 'отдел кадров', 'медпункт', 'библиотека', 'пост охраны']
objs = ['документ','тетрадь','блокнот', 'документация', 'чашка', 'кружка','пенал', 'работа', 'груз','весы', 'объект', 'прибор', 'ножницы','яблоко','пицца']
actions = ['принеси', 'отнеси', 'занеси', 'возьми', 'доставь', 'отвези', 'довези', 'захвати', 'забери', 'передай']
please = ['пожалуйста',''] # 'бога ради', 
be_kind = ['будь добр','будь так добр','друг','дружок','будь бругом','прошу', 'сделай одолжение','добрый день','добрый вечер','доброе утро','']

dirF = ['туда','для них', 'коллегам', 'им']
dirB = ['оттуда', 'сюда', 'для нас','для меня','нам','мне']

back = ['PRE COPY_MOVE_C назад','PRE возвращайся обратно', 'PRE возвращайся', 'PRE вернись', 'PRE COPY_MOVE_C обратно', 'PRE COPY_MOVE_C на прежнее место', 'PRE COPY_MOVE_C в исходную точку', 'PRE COPY_MOVE_C в начальную точку']

may = ['можешь', 'можете', 'попробуй', 'потрудитесь', 'потрудись','изволь', 'извольте', 'не откажи в любезности','не откажите в любезности', 'не сочти за труд','не сочтите за труд']
moveCmd_with_may = ['поехать','сгонять','добраться','переместиться','приехать','прибыть','заехать','пойти','идти','зайти','сходить', 'дойти','съездить']
actions_with_may = ['принести', 'отнести', 'занести', 'взять', 'доставить', 'отвезти', 'довезти', 'захватить', 'забрать', 'передать']
back_with_may = ['PRE COPY_MOV_CMD назад', 'PRE вернуться', 'PRE COPY_MOV_CMD обратно', 'PRE COPY_MOV_CMD на прежнее место','PRE COPY_MOV_CMD в исходную точку', 'PRE COPY_MOV_CMD в начальную точку']

dictTargets = {
               'BACK' : back,
               'M_BAC' : back_with_may,
               'MAY' : may,
               'MOVE_CMD' : moveCmd,
               'COPY_MOVE_C': moveCmd,
               'M_MOV_CMD' : moveCmd_with_may,
               'COPY_MOV_CMD': moveCmd_with_may,
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

sentTemplate = [[0, 'BE_KIND MOVE_CMD в PLACE_1 и ACTION DIR_F OBJ'],           # 0
                [0, 'MOVE_CMD PLEASE в PLACE_1 и ACTION DIR_F OBJ'],            # 1
                [2, 'BE_KIND MOVE_CMD в PLACE_1 и ACTION DIR_F OBJ BACK'],      # 2  
                [2, 'MOVE_CMD PLEASE в PLACE_1 и ACTION DIR_F OBJ BACK'],       # 3
                [1, 'BE_KIND MOVE_CMD в PLACE_1 и ACTION DIR_B OBJ'],           # 4 
                [1, 'MOVE_CMD PLEASE в PLACE_1 и ACTION DIR_B OBJ'],            # 5
                [0, 'BE_KIND MOVE_CMD в PLACE_1 и ACTION OBJ DIR_F'],           # 6 
                [0, 'MOVE_CMD PLEASE в PLACE_1 и ACTION OBJ DIR_F'],            # 7
                [2, 'BE_KIND MOVE_CMD в PLACE_1 и ACTION OBJ DIR_F BACK'],      # 8 
                [2, 'MOVE_CMD PLEASE в PLACE_1 и ACTION OBJ DIR_F BACK'],       # 9
                [1, 'BE_KIND MOVE_CMD в PLACE_1 и ACTION OBJ DIR_B'],           # 10 
                [1, 'MOVE_CMD PLEASE в PLACE_1 и ACTION OBJ DIR_B'],            # 11
                [1, 'BE_KIND ACTION OBJ из PLACE_1'],                           # 12        
                [1, 'ACTION OBJ PLEASE из PLACE_1'],                            # 13        
                [1, 'BE_KIND ACTION OBJ из PLACE_1'],                           # 14         
                [1, 'PLEASE ACTION OBJ из PLACE_1'],                            # 15
                [0, 'BE_KIND ACTION OBJ в PLACE_1'],                            # 16         
                [0, 'ACTION OBJ PLEASE в PLACE_1'],                             # 17
                [0, 'BE_KIND ACTION OBJ в PLACE_1'],                            # 18         
                [0, 'PLEASE ACTION OBJ в PLACE_1'],                             # 19
                [0, 'BE_KIND ACTION OBJ в PLACE_1'],                            # 20                
                [2, 'BE_KIND ACTION OBJ в PLACE_1 BACK'],                       # 21         
                [2, 'ACTION OBJ PLEASE в PLACE_1 BACK'],                        # 22
                [2, 'BE_KIND ACTION OBJ в PLACE_1 BACK'],                       # 23         
                [2, 'PLEASE ACTION OBJ в PLACE_1 BACK'],                        # 24
                [2, 'BE_KIND ACTION OBJ в PLACE_1 BACK'],                       # 25            
                [0, 'MAY M_MOV_CMD PLEASE в PLACE_1 и M_ACT DIR_F OBJ'],        # 26    
                [2, 'MAY M_MOV_CMD PLEASE в PLACE_1 и M_ACT DIR_F OBJ M_BAC'],  # 27    
                [1, 'MAY M_MOV_CMD PLEASE в PLACE_1 и M_ACT DIR_B OBJ'],        # 28
                [0, 'MAY M_MOV_CMD PLEASE в PLACE_1 и M_ACT OBJ DIR_F'],        # 29
                [2, 'MAY M_MOV_CMD PLEASE в PLACE_1 и M_ACT OBJ DIR_F M_BAC'],  # 30
                [1, 'MAY M_MOV_CMD PLEASE в PLACE_1 и M_ACT OBJ DIR_B'],        # 31
                [1, 'MAY M_ACT OBJ PLEASE из PLACE_1'],                         # 32
                [1, 'PLEASE MAY M_ACT OBJ из PLACE_1'],                         # 33
                [0, 'MAY M_ACT OBJ PLEASE в PLACE_1'],                          # 34
                [0, 'PLEASE MAY M_ACT OBJ в PLACE_1'],                          # 35
                [0, 'MAY M_ACT OBJ в PLACE_1'],                                 # 36                      
                [2, 'MAY M_ACT OBJ PLEASE в PLACE_1 M_BAC'],                    # 37
                [2, 'PLEASE MAY M_ACT OBJ в PLACE_1 M_BAC'],                    # 38
                [2, 'MAY M_ACT OBJ в PLACE_1 M_BAC'],                           # 39
                [1, 'ACTION OBJ из PLACE_1 PLEASE'],                            # 40
                [2, 'ACTION OBJ в PLACE_1 BACK PLEASE']                         # 41
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
