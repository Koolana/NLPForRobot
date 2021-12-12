class WrapperRobertaTokenizer():
    def __init__(self, tokeniser):
        self.tokeniser = tokeniser

    def convertTokenToIds(self, token):
        return self.tokeniser(token)['input_ids'][1:-1]

    def convertSentToIds(self, sent):
        return [1] + [item for sublist in sent.split() for item in self.convertTokenToIds(sublist)] + [2]

    def convertIdsToSent(self, ids):
        return self.tokeniser.convert_ids_to_tokens(ids)
