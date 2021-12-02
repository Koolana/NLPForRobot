################### Задача seg2seg предложений содержащих команду ###################

# датасет в файле outputdataClean.csv формата: str(sentence),str(robot_sentence)

from lemmDataFromFile import extractDataAndLemmatization

if __name__ == '__main__':
    data = extractDataAndLemmatization('../datasets/outputdataClean.csv')

    ### Некоторые действия на data ###
    print(*data[:10], sep='\n')
    print('Hello')
