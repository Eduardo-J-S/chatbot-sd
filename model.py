import torch
import torch.nn as nn

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        """
        Inicialização da Rede Neural.

        Parâmetros:
        - input_size: Tamanho da camada de entrada.
        - hidden_size: Tamanho da camada oculta.
        - num_classes: Número de classes de saída.
        """
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        """
        Método forward da Rede Neural.

        Parâmetros:
        - x: Dados de entrada.

        Retorna:
        - out: Saída da rede neural.
        """
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        # Sem ativação e sem softmax (para CrossEntropyLoss)
        return out
