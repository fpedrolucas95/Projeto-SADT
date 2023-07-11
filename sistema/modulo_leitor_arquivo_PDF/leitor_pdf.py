import os
import torch
from flask_socketio import emit
from torchvision import models, transforms
from PIL import Image
from PyPDF2 import PdfReader
import pdf2image
import torch.nn as nn

# Configurações
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_path = "modelo/modelo_guia_SADT.pth"
temp_folder = "/tmp/"
os.makedirs(temp_folder, exist_ok=True)

# Carregar modelo
model = models.resnet50(weights=None)  # Mudança aqui
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 2)
model.load_state_dict(torch.load(model_path, map_location=device))
model = model.to(device)
model.eval()

# Função de transformação
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

# Função para analisar PDF e identificar guias SADT
def analisar_pdf(pdf_path, callback):
    pdf_file = PdfReader(pdf_path)
    num_pages = len(pdf_file.pages)
    guias_sadt_pages = []

    for i in range(num_pages):
        # Calcular e imprimir a porcentagem de conclusão
        completion_percentage = (i / num_pages) * 100
        callback(completion_percentage)

        image_path = f"{temp_folder}{i}.png"
        image = pdf2image.convert_from_path(
            pdf_path, dpi=300, first_page=i+1, last_page=i+1, fmt='png')[0]
        image.save(image_path, "PNG")

        image = Image.open(image_path).convert("RGB")
        image = transform(image).unsqueeze(0).to(device)

        outputs = model(image)
        _, predicted = torch.max(outputs.data, 1)

        if predicted.item() == 0:
            guias_sadt_pages.append(i+1)

        os.remove(image_path)

    return guias_sadt_pages