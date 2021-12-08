import random
import re

countries = ['Африка','Бразилия','Евразия','Антарктида','Южная Америка','Северная Америка']
moveCmd = ['поезжай', 'сгоняй', 'следуй','доберись', 'дойди', 'переместись', 'приедь', 'прибудь', 'заедь', 'иди','пойди','зайди','сходи', 'съезди','телепортируйся','сбегай']
preposition = ['и','и затем','а затем','и потом', 'а потом', 'и после', 'а после', 'затем','потом','после','после этого','а после этого', 'и после этого','после чего','а после чего', 'и после чего', 'и только тогда', 'и только после этого', 'и только потом', 'и вот только тогда']
places = ['кампус COUNTRY','пункт NUM', 'кабинет NUM', 'аудитория NUM', 'отдел кадров', 'медпункт', 'библиотека', 'пост охраны']
objs = ['аптечка','документ','инструмент','тетрадь','печать','блокнот','телефон','зонтик','документация','чашка','кружка','пенал','работа','груз','весы','объект','прибор','ножницы','яблоко','пицца']
actions = ['принеси','привези', 'отнеси','увези','отдай', 'занеси', 'возьми', 'доставь', 'отвези', 'довези', 'захвати','прихвати', 'забери', 'передай']

action_there = ['принеси','привези', 'отнеси','увези','отдай','отвези','занеси','возьми','доставь','довези','захвати','прихвати', 'забери', 'передай']
action_here = ['принеси','привези','занеси','возьми','доставь','захвати','прихвати', 'забери', 'передай']
please = ['пожалуйста',''] # 'бога ради', 
be_kind = ['будь добр','будь так добр','друг','дружок','будь другом','прошу', 'сделай одолжение','добрый день','добрый вечер','доброе утро','привет','сделай доброе дело','']
hello = ['добрый день','добрый вечер','доброе утро','привет',''] 

clarification = ['именно','вот','только','']
dirF = ['туда','для них', 'коллегам', 'им']
dirB = ['оттуда', 'сюда', 'для нас','для меня','нам','мне']
dir_only_here = ['CLALIFICAT сюда', 'для нас CLALIFICAT','для меня CLALIFICAT','нам CLALIFICAT','мне CLALIFICAT']

back = ['PRE COPY_MOVE_C назад','PRE возвращайся обратно', 'PRE возвращайся', 'PRE вернись', 'PRE COPY_MOVE_C обратно', 'PRE COPY_MOVE_C на прежнее место', 'PRE COPY_MOVE_C в исходную точку', 'PRE COPY_MOVE_C в начальную точку']

may = ['можешь', 'можете', 'попробуй', 'попробуйте', 'потрудитесь', 'потрудись','изволь', 'извольте', 'не откажи в любезности','не откажите в любезности', 'не сочти за труд','не сочтите за труд']
moveCmd_with_may = ['поехать','сгонять','добраться','переместиться','приехать','прибыть','заехать','пойти','идти','зайти','сходить', 'дойти','съездить','телепортироваться','сбегать']
actions_with_may = ['принести','привезти', 'отнести', 'занести', 'взять', 'доставить', 'отвезти', 'довезти', 'захватить','прихватить', 'забрать', 'передать']
back_with_may = ['PRE COPY_MOV_CMD назад', 'PRE вернуться', 'PRE COPY_MOV_CMD обратно', 'PRE COPY_MOV_CMD на прежнее место','PRE COPY_MOV_CMD в исходную точку', 'PRE COPY_MOV_CMD в начальную точку']

Names_1 = ['Николай','Сергей Александрович','Алексей Вячеславович','Полина','Ксения','Настя']
Names_2 = ['Николаю','Сергею Александровичу','Алексею Вячеславовичу','Полине','Ксении','Насте']
Names_3 = ['Николай и Ксения','Полина и Настя','Полина и Ксения']
I = ['я','']
He = ['он', 'она', 'коллега','команда', 'коллектив', 'NAME_1']
We = ['мы','']
They = ['они','коллеги', 'руководители', 'NAME_3']
Me = ['мне','ему','ей','нам', 'им', 'коллегам','команде', 'руководителям', 'коллективу', 'NAME_2','']

I_want = ['хочу','желаю','прошу','требую','жажду']
He_want = ['хочет','желает','просит','требует','жаждет']
We_want = ['хотим','желаем','просим','требуем','жаждим']
They_want = ['хотят','желают','просят', 'требуют','жаждят']
Me_want = ['хочется','охота']
action_there_want = ['принес','привез', 'отнес','отвез','отдал','увез','занес','взял','доставил','довез','захватил','прихватил', 'забрал', 'передал']
action_here_want = ['принес','привез','занес','взял','доставил','захватил','прихватил', 'забрал', 'передал']
moveCmd_want = ['поехал', 'сгонял', 'следовал','добрался','шел', 'дошел', 'переместился', 'приехал', 'прибыл', 'заехал','пошел','зашел','сходил', 'съездил','телепортировался','сбегал']
back_want = ['PRE WANT_COM_MOVE назад', 'PRE вернулся', 'PRE WANT_COM_MOVE обратно', 'PRE WANT_COM_MOVE на прежнее место','PRE WANT_COM_MOVE в исходную точку', 'PRE WANT_COM_MOVE в начальную точку']

# act_with_may_here = ['принести','привезти']


dictTargets = {
               
               'BACK' : back,
               'M_BAC' : back_with_may,
               'MAY' : may,
               'MOVE_CMD' : moveCmd,
               'WANT_BAC': back_want,
               'WANT_COM_MOVE': moveCmd_want,
               'WANT_HEREACT': action_here_want,
               'WANT_THEREACT': action_there_want,
               'COPY_MOVE_C': moveCmd,
               'M_MOV_CMD' : moveCmd_with_may,
               'COPY_MOV_CMD': moveCmd_with_may,
               'PLEASE' : please,
               'BE_KIND' : be_kind,
               'COM_I' : I,
               'COM_HE' : He,
               'COM_WE' : We,
               'COM_THEY' : They,
               'COM_ME' : Me,
               'WANT_I' : I_want,
               'WANT_HE' : He_want,
               'WANT_WE' : We_want,
               'WANT_THEY' : They_want,
               'WANT_ME' : Me_want,
               'PRE' : preposition,
               'PLACE_1' : places,
               'ACTION' : actions,
               'TH_ACT': action_there,
               'ACT_H': action_here,
               'M_ACT' : actions_with_may,
               'DIR_F' : dirF,
               'DIR_B' : dirB,
               'ONLY_HERE': dir_only_here,
               'OBJ' : objs,
               'PLACE_2' : places,
               'COUNTRY' : countries,
               'HI': hello,
               'CLALIFICAT' : clarification,
               'NAME_1' : Names_1,
               'NAME_2' : Names_2,
               'NAME_3' : Names_3,
               'NUM' : [str(i) for i in range(0, 1000)]}

cmdTemplate = ['взять(OBJ) движение(PLACE_1)',
               'движение(PLACE_1) взять(OBJ) движение(обратно)',
               'взять(OBJ) движение(PLACE_1) движение(обратно)',
               'движение(PLACE_1) взять(OBJ) движение(PLACE_2)']

sentTemplate = [[0, 'BE_KIND MOVE_CMD в PLACE_1 и TH_ACT DIR_F OBJ'],           # 0
                [0, 'MOVE_CMD PLEASE в PLACE_1 и TH_ACT DIR_F OBJ'],            # 1
                [2, 'BE_KIND MOVE_CMD в PLACE_1 и TH_ACT DIR_F OBJ BACK'],      # 2  
                [2, 'MOVE_CMD PLEASE в PLACE_1 и TH_ACT DIR_F OBJ BACK'],       # 3
                [1, 'BE_KIND MOVE_CMD в PLACE_1 и TH_ACT DIR_B OBJ'],           # 4 
                [1, 'MOVE_CMD PLEASE в PLACE_1 и TH_ACT DIR_B OBJ'],            # 5
                [0, 'BE_KIND MOVE_CMD в PLACE_1 и TH_ACT OBJ DIR_F'],           # 6 
                [0, 'MOVE_CMD PLEASE в PLACE_1 и TH_ACT OBJ DIR_F'],            # 7
                [2, 'BE_KIND MOVE_CMD в PLACE_1 и TH_ACT OBJ DIR_F BACK'],      # 8 
                [2, 'MOVE_CMD PLEASE в PLACE_1 и TH_ACT OBJ DIR_F BACK'],       # 9
                [1, 'BE_KIND MOVE_CMD в PLACE_1 и TH_ACT OBJ DIR_B'],           # 10 
                [1, 'MOVE_CMD PLEASE в PLACE_1 и TH_ACT OBJ DIR_B'],            # 11
                [1, 'BE_KIND ACT_H OBJ из PLACE_1'],                            # 12        
                [1, 'ACT_H OBJ PLEASE из PLACE_1'],                             # 13        
                [1, 'BE_KIND ACT_H OBJ из PLACE_1'],                            # 14         
                [1, 'PLEASE ACT_H OBJ из PLACE_1'],                             # 15
                [0, 'BE_KIND TH_ACT OBJ в PLACE_1'],                            # 16         
                [0, 'TH_ACT OBJ PLEASE в PLACE_1'],                             # 17
                [0, 'BE_KIND TH_ACT OBJ в PLACE_1'],                            # 18         
                [0, 'PLEASE TH_ACT OBJ в PLACE_1'],                             # 19
                [0, 'BE_KIND TH_ACT OBJ в PLACE_1'],                            # 20                
                [2, 'BE_KIND TH_ACT OBJ в PLACE_1 BACK'],                       # 21         
                [2, 'TH_ACT OBJ PLEASE в PLACE_1 BACK'],                        # 22
                [2, 'BE_KIND TH_ACT OBJ в PLACE_1 BACK'],                       # 23         
                [2, 'PLEASE TH_ACT OBJ в PLACE_1 BACK'],                        # 24
                [2, 'BE_KIND TH_ACT OBJ в PLACE_1 BACK'],                       # 25            
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
                [1, 'ACT_H OBJ из PLACE_1 PLEASE'],                             # 40
                [2, 'TH_ACT OBJ в PLACE_1 BACK PLEASE'],                        # 41
                [1, 'MAY M_ACT OBJ из PLACE_1 PLEASE'],                         # 42
                [0, 'MAY M_ACT OBJ в PLACE_1 PLEASE'],                          # 43
                [1, 'BE_KIND ACTION ONLY_HERE OBJ из PLACE_1'],                 # 44        
                [1, 'ACTION ONLY_HERE OBJ PLEASE из PLACE_1'],                  # 45        
                [1, 'BE_KIND ACTION ONLY_HERE OBJ из PLACE_1'],                 # 46         
                [1, 'PLEASE ACTION ONLY_HERE OBJ из PLACE_1'],                  # 47                
                [1, 'MAY M_ACT ONLY_HERE OBJ PLEASE из PLACE_1'],               # 48
                [1, 'PLEASE MAY ONLY_HERE M_ACT OBJ из PLACE_1'],               # 49               
                [1, 'ACTION ONLY_HERE OBJ из PLACE_1 PLEASE'],                  # 50
                [1, 'BE_KIND ACTION OBJ ONLY_HERE из PLACE_1'],                 # 51
                [1, 'ACTION OBJ PLEASE ONLY_HERE из PLACE_1'],                  # 52
                [1, 'MAY M_ACT OBJ PLEASE ONLY_HERE из PLACE_1'],               # 53
                [1, 'PLEASE MAY M_ACT OBJ ONLY_HERE из PLACE_1'],               # 54
                [1, 'ACTION OBJ из PLACE_1 ONLY_HERE PLEASE'],                  # 55
                [1, 'HI COM_I WANT_I чтобы ты WANT_COM_MOVE в PLACE_1 и WANT_THEREACT OBJ ONLY_HERE'],         # 56
                [0, 'HI COM_I WANT_I чтобы ты WANT_THEREACT OBJ в PLACE_1'],                                   # 57
                [2, 'HI COM_I WANT_I чтобы ты WANT_THEREACT OBJ в PLACE_1 WANT_BAC'],                          # 58
                [1, 'HI COM_HE WANT_HE чтобы ты WANT_COM_MOVE в PLACE_1 и WANT_THEREACT OBJ ONLY_HERE'],       # 59
                [0, 'HI COM_HE WANT_HE чтобы ты WANT_THEREACT OBJ в PLACE_1'],                                 # 60 
                [2, 'HI COM_HE WANT_HE чтобы ты WANT_THEREACT OBJ в PLACE_1 WANT_BAC'],                        # 61 
                [1, 'HI COM_WE WANT_WE чтобы ты WANT_COM_MOVE в PLACE_1 и WANT_THEREACT OBJ ONLY_HERE'],       # 62
                [0, 'HI COM_WE WANT_WE чтобы ты WANT_THEREACT OBJ в PLACE_1'],                                 # 63 
                [2, 'HI COM_WE WANT_WE чтобы ты WANT_THEREACT OBJ в PLACE_1 WANT_BAC'],                        # 64 
                [1, 'HI COM_ME WANT_ME чтобы ты WANT_COM_MOVE в PLACE_1 и WANT_THEREACT OBJ ONLY_HERE'],       # 65
                [0, 'HI COM_ME WANT_ME чтобы ты WANT_THEREACT OBJ в PLACE_1'],                                 # 66 
                [2, 'HI COM_ME WANT_ME чтобы ты WANT_THEREACT OBJ в PLACE_1 WANT_BAC'],                        # 67
                [1, 'HI COM_THEY WANT_THEY чтобы ты WANT_COM_MOVE в PLACE_1 и WANT_THEREACT OBJ ONLY_HERE'],   # 68
                [0, 'HI COM_THEY WANT_THEY чтобы ты WANT_THEREACT OBJ в PLACE_1'],                             # 69 
                [2, 'HI COM_THEY WANT_THEY чтобы ты WANT_THEREACT OBJ в PLACE_1 WANT_BAC'],                    # 70
                [1, 'HI COM_I WANT_I чтобы ты WANT_THEREACT OBJ ONLY_HERE из PLACE_1'],                        # 71
                [1, 'HI COM_HE WANT_HE чтобы ты WANT_THEREACT OBJ ONLY_HERE из PLACE_1'],                      # 72
                [1, 'HI COM_WE WANT_WE чтобы ты WANT_THEREACT OBJ ONLY_HERE из PLACE_1'],                      # 73
                [1, 'HI COM_ME WANT_ME чтобы ты WANT_THEREACT OBJ ONLY_HERE из PLACE_1'],                      # 74
                [1, 'HI COM_THEY WANT_THEY чтобы ты WANT_THEREACT OBJ ONLY_HERE из PLACE_1'],                  # 75
                [1, 'HI COM_I WANT_I чтобы ты WANT_HEREACT OBJ из PLACE_1'],                                   # 76
                [1, 'HI COM_HE WANT_HE чтобы ты WANT_HEREACT OBJ из PLACE_1'],                                 # 77
                [1, 'HI COM_WE WANT_WE чтобы ты WANT_HEREACT OBJ из PLACE_1'],                                 # 78
                [1, 'HI COM_ME WANT_ME чтобы ты WANT_HEREACT OBJ из PLACE_1'],                                 # 79
                [1, 'HI COM_THEY WANT_THEY чтобы ты WANT_HEREACT OBJ из PLACE_1'],                             # 80
                [2, 'HI COM_I WANT_I чтобы ты в PLACE_1 WANT_THEREACT OBJ WANT_BAC'],                          # 81
                [2, 'HI COM_HE WANT_HE чтобы ты в PLACE_1 WANT_THEREACT OBJ WANT_BAC'],                        # 82 
                [2, 'HI COM_WE WANT_WE чтобы ты в PLACE_1 WANT_THEREACT OBJ WANT_BAC'],                        # 83 
                [2, 'HI COM_ME WANT_ME чтобы ты в PLACE_1 WANT_THEREACT OBJ WANT_BAC'],                        # 84 
                [2, 'HI COM_THEY WANT_THEY чтобы ты в PLACE_1 WANT_THEREACT OBJ WANT_BAC']                     # 85 
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
