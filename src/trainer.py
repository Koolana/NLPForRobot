import torch
import torch.nn as nn
import torch.optim as optim

class Trainer():
    def __init__(self, model, trainIterator, valIterator, device, padId=0, learningRate=0.0005):
        self.model = model

        self.trainIterator = trainIterator
        self.valIterator = valIterator

        self.device = device

        self.model.apply(self.initialize_weights);

        self.optimizer = torch.optim.Adam(model.parameters(), lr=learningRate)
        self.criterion = nn.CrossEntropyLoss(ignore_index=padId)

    def initialize_weights(self, m):
        if hasattr(m, 'weight') and m.weight.dim() > 1:
            nn.init.xavier_uniform_(m.weight.data)

    def count_parameters(self):
        return sum(p.numel() for p in self.model.parameters() if p.requires_grad)

    def train(self, clip):
        self.model.train()

        epoch_loss = 0

        for i, batch in enumerate(self.trainIterator):
            src = batch[0].to(self.device)
            trg = batch[1].to(self.device)

            self.optimizer.zero_grad()

            output, _ = self.model(src, trg[:,:-1])

            #output = [batch size, trg len - 1, output dim]
            #trg = [batch size, trg len]

            output_dim = output.shape[-1]

            output = output.contiguous().view(-1, output_dim)
            trg = trg[:,1:].contiguous().view(-1)

            #output = [batch size * trg len - 1, output dim]
            #trg = [batch size * trg len - 1]

            loss = self.criterion(output, trg)

            loss.backward()

            torch.nn.utils.clip_grad_norm_(self.model.parameters(), clip)

            self.optimizer.step()

            epoch_loss += loss.item()

        return epoch_loss / len(self.trainIterator)

    def evaluate(self):
        self.model.eval()

        epoch_loss = 0

        with torch.no_grad():

            for i, batch in enumerate(self.valIterator):
                src = batch[0].to(self.device)
                trg = batch[1].to(self.device)

                output, _ = self.model(src, trg[:,:-1])

                #output = [batch size, trg len - 1, output dim]
                #trg = [batch size, trg len]

                output_dim = output.shape[-1]

                output = output.contiguous().view(-1, output_dim)
                trg = trg[:,1:].contiguous().view(-1)

                #output = [batch size * trg len - 1, output dim]
                #trg = [batch size * trg len - 1]

                loss = self.criterion(output, trg)

                epoch_loss += loss.item()

        return epoch_loss / len(self.valIterator)
