import os
import torch
from torchvision import models, transforms
from PIL import Image
from PyPDF2 import PdfReader
import pdf2image
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from .extrator import extrair_dados_raw

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_path = "modelo/modelo_guia_SADT.pth"
temp_folder = "./temp/"
os.makedirs(temp_folder, exist_ok=True)

def load_model(model_path, device):
    model = models.resnet50(weights=None)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 2)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()
    return model

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

class PDFImagesDataset(Dataset):
    def __init__(self, pdf_path, dpi=300, transform=None):
        self.pdf_path = pdf_path
        self.dpi = dpi
        self.transform = transform
        self.pdf_file = PdfReader(pdf_path)
        self.num_pages = len(self.pdf_file.pages)

    def __len__(self):
        return self.num_pages

    def __getitem__(self, idx):
        image = pdf2image.convert_from_path(self.pdf_path, dpi=self.dpi, first_page=idx+1, last_page=idx+1, fmt='png')[0]
        if self.transform:
            image = self.transform(image)
        return image

def analisar_pdf(pdf_path, callback):
    model = load_model(model_path, device)
    dataset = PDFImagesDataset(pdf_path, transform=transform)
    dataloader = DataLoader(dataset, batch_size=32, num_workers=4)
    guias_sadt_pages = []

    for i, batch in enumerate(dataloader):
        batch = batch.to(device)
        outputs = model(batch)
        _, predicted = torch.max(outputs.data, 1)

        for j, prediction in enumerate(predicted):
            page_num = i * dataloader.batch_size + j + 1
            completion_percentage = page_num / len(dataset) * 100
            callback(completion_percentage)
            if prediction.item() == 0:
                image = pdf2image.convert_from_path(pdf_path, dpi=300, first_page=page_num, last_page=page_num, fmt='png')[0]
                image_path = os.path.join(temp_folder, f'pagina_{page_num}.png')
                image.save(image_path)
                dados_pagina = extrair_dados_raw(image_path)
                guias_sadt_pages.append(dados_pagina)
    
    return guias_sadt_pages
