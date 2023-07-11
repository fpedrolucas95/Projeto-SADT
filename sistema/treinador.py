# Ele considera que você terá uma pasta principal e dentro dela duas subpastas, com imagens JPG
# Uma chamada "guia SADT" onde você deve colocar o maior número de guias possível, de todas as operadoras de saúde de preferência
# E outra chamada "não guia SADT", coloque todo tipo de documento, principalmente pedidos médicos, escaners de documentos, etc.

import torch
import torchvision
from torchvision import datasets, models, transforms
import torch.nn as nn
from torch.utils.data import DataLoader

# Configurações do treino
device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # Funciona melhor com uma GPU NVIDIA, na CPU é bem demorado.
num_epochs = 20
batch_size = 4
learning_rate = 0.001

# Transformação dos dados
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Carregar o dataset
dataset = datasets.ImageFolder(root='/CAMINHO_PARA_AS IMAGENS', transform=transform) #substitua o CAMINHO_PARA_AS IMAGENS pelo caminho da pasta onde está salva as imagens, deve estar divididas em duas pastas, "guia SADT" e "não guia SADT"
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Carregar modelo pré-treinado
model = models.resnet50(weights=models.resnet.ResNet50_Weights.IMAGENET1K_V1)

# Alterar a última camada
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 2) # Para reconhecer as imagens das duas pastas, sabendo que em uma há guias e em outra não
model = model.to(device)

# Definindo a função de perda e o otimizador
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

# Loop de treinamento
for epoch in range(num_epochs):
    for i, (inputs, labels) in enumerate(dataloader):
        inputs = inputs.to(device)
        labels = labels.to(device)

        # Propagação para frente
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # Propagação para trás e otimização
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (i+1) % 100 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{len(dataloader)}], Loss: {loss.item()}')

# Salvando o modelo treinado
torch.save(model.state_dict(), '/ONDE_VAI_SALVAR_O_ARQUIVO') # Substitua /ONDE_VAI_SALVAR_O_ARQUIVO pelo caminho onde vai salvar o modelo
print('Treinamento completo.')
