import os
import json
from PIL import Image
import torch
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader

train_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

val_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

class CarComponentDataset(Dataset):
    def __init__(self, metadata_path, transform=None):
        with open(metadata_path, "r") as f:
            self.metadata = json.load(f)
        self.transform = transform
        self.components = ["door_front_left", "door_front_right", "door_rear_left", "door_rear_right", "hood"]

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, idx):
        item = self.metadata[idx]
        image = Image.open(item["file_path"]).convert("RGB")
        labels = [1 if item["component_states"][comp] == "open" else 0 for comp in self.components]
        if self.transform:
            image = self.transform(image)
        return image, torch.tensor(labels, dtype=torch.float32)

dataset = CarComponentDataset("dataset/metadata.json")
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

train_dataset.dataset.transform = train_transforms
val_dataset.dataset.transform = val_transforms

train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=4, shuffle=False)

print("Total data:", len(dataset))
print("Train size:", len(train_dataset))
print("Validation size:", len(val_dataset))

for images, labels in train_loader:
    print("Image batch shape:", images.shape)
    print("Label batch:\n", labels)
    break
