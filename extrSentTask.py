################### Задача нахождения предложений содержащих комнаду ###################

# датасет в файле outputdataDirty.csv формата: str(sentence),int(label)

from lemmDataFromFile import extractDataAndLemmatization

if __name__ == '__main__':
    data = extractDataAndLemmatization('outputdataDirty.csv')
    data = [[i[0], int(i[1])] for i in data]

    ### Некоторые действия на data ###
    print(*data[:10], sep='\n')
