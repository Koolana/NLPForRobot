from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER,
    NamesExtractor,
    DatesExtractor,
    MoneyExtractor,
    AddrExtractor,

    Doc
)

import re

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)
dates_extractor = DatesExtractor(morph_vocab)
money_extractor = MoneyExtractor(morph_vocab)
addr_extractor = AddrExtractor(morph_vocab)

def sentsLemmatization(text):
    # Сегментация предложений
    doc = Doc(text)
    doc.segment(segmenter)

    # проведем лемматизацию
    doc.tag_morph(morph_tagger)
    for token in doc.tokens:
        token.lemmatize(morph_vocab)

    listLemma = [i.lemma for i in doc.tokens]

    listLemmaSent = []
    tempSent = []
    for i in listLemma:
        if i == '.':
            listLemmaSent.append(tempSent)
            tempSent = []
        else:
            tempSent.append(i)

    return listLemmaSent

# Формат выходного list:
# data
#   |----sentence
#   |        |----lemma words
#   |----label

def extractDataAndLemmatization(pathToFile=''):
    f = open(pathToFile, 'r')
    data = f.read()
    data = [i.split(',') for i in data.split('\n') if i != '']

    toLemma = '. '.join([i[0][0].upper() + i[0][1:] for i in data]) + '.'
    lemmaSent = sentsLemmatization(toLemma)

    for i in range(len(data)):
        data[i][0] = lemmaSent[i]

    return data

if __name__ == '__main__':
    # Вывод предложений после лемматизации для задачи нахождения предложений содержащих комнаду
    print(*extractDataAndLemmatization('outputdataDirty.csv')[:10], sep='\n')

    # Вывод предложений после лемматизации для задачи seg2seg предложений содержащих команду
    print(extractDataAndLemmatization('outputdataClean.csv')[:10], sep='\n')
