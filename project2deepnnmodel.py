import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

input_size = 784
hidden_size1 = 512
hidden_size2 = 256
hidden_size3 = 128

num_classes = 10
num_epochs = 20
batch_size = 128
learning_rate = 0.001

train_dataset = torchvision.datasets.FashionMNIST(
     root = './data/FashionMNIST',
     train = True,
     download = True,
     transform = transforms.Compose([
                                     transforms.ToTensor(),transforms.Normalize((0.485,),(0.229,))
                                     ])
     
     )
test_dataset = torchvision.datasets.FashionMNIST(
     root = './data/FashionMNIST',
     train = False,
     download = True,
     transform = transforms.Compose([
                                     transforms.ToTensor(),transforms.Normalize((0.485,),(0.229,))
                                     ])
     
     )
# Data loader
train_loader = torch.utils.data.DataLoader(dataset=train_dataset, 
                                           batch_size=batch_size, 
                                           shuffle=True)

test_loader = torch.utils.data.DataLoader(dataset=test_dataset, 
                                          batch_size=len(test_dataset) ,
                                          shuffle=False)

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size1,hidden_size2,hidden_size3, num_classes):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size1) 
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size1, hidden_size2)  
        self.relu = nn.ReLU()
        self.fc3 = nn.Linear(hidden_size2, hidden_size3) 
        self.relu = nn.ReLU()
        self.fc4 = nn.Linear(hidden_size3, num_classes) 

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.relu(out)
        out = self.fc3(out)
        out = self.relu(out)
        out = self.fc4(out)
        return out

model = NeuralNet(input_size,hidden_size1,hidden_size2,hidden_size3, num_classes)
#model1 = ConvNet(num_classes)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)  
#optimizer1 = torch.optim.Adam(model1.parameters(), lr=learning_rate)

#Training of neural network

total_step = len(train_loader)
for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(train_loader):  
        # Move tensors to the configured device
        images = images.reshape(-1, 28*28)
        labels = labels
        
        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (i+1) % 100 == 0:
            print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}' 
                   .format(epoch+1, num_epochs, i+1, total_step, loss.item()))

model.eval()
with torch.no_grad():
    correct = 0
    total = 0
    for images, labels in test_loader:
        images = images.reshape(-1, 28*28)
        labels = labels
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    print('Accuracy of the network on the 10000 test images: {} %'.format(100 * correct / total))

stacked = torch.stack(
    (
        labels
        ,predicted
    )
    , dim=1
)
print(labels)
print(predicted)

cmt = torch.zeros(10,10, dtype=torch.int64)
#cmt1 = torch.zeros(10,10, dtype=torch.int64)

for p in stacked:
    tl, pl = p.tolist()
    cmt[tl, pl] = cmt[tl, pl] + 1

#for p in stacked1:
    # tl, pl = p.tolist()
    # cmt1[tl, pl] = cmt1[tl, pl] + 1

cmt

import itertools
import numpy as np
import matplotlib.pyplot as plt

def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt), horizontalalignment="center", color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

names = (
    'T-shirt/top'
    ,'Trouser'
    ,'Pullover'
    ,'Dress'
    ,'Coat'
    ,'Sandal'
    ,'Shirt'
    ,'Sneaker'
    ,'Bag'
    ,'Ankle boot'
)
 plt.figure(figsize=(10,10))
 plot_confusion_matrix(cmt, names)
#  plt.figure(figsize=(10,10))
#  plot_confusion_matrix(cmt1, names)
from google.colab import files
plt.savefig("CM_NN1.png")
files.download("CM_NN1.png")
# plt.figure(figsize=(10,10))
 #plot_confusion_matrix(cmt1, names)
 
#from google.colab import files
#plt.savefig("CM_CNN1.png")
#iles.download("CM_CNN1.png")

predicted[0:20]

img, label = test_dataset[20]

import matplotlib.pyplot as plt
plt.imshow(img.reshape(28,28))

names[0]

names[predicted[-1]]

f = open("multi-layer-net.txt", "w")
i=0
for _,_ in test_dataset:
  f.write(names[predicted[i]] + '\n')
  i = i+1


f.close()

# f = open("convolution-neural-net.txt", "w")
# i=0
# for _,_ in test_dataset:
#   f.write(names[predicted1[i]] + '\n')
#   i = i+1


# f.close()

f = open("multi-layer-net.txt", "w")
i=0
for _,_ in test_dataset:
  f.write(names[predicted[i]] + '\n')
  i = i+1


f.close()

# f = open("convolution-neural-net.txt", "w")
# i=0
# for _,_ in test_dataset:
#   f.write(names[predicted1[i]] + '\n')
#   i = i+1


# f.close()

from google.colab import drive
drive.mount('/content/gdrive')

!ls /content/gdrive

model_save_name = 'basicnnfmnistmodel1.pt'
path = F"/content/gdrive/My Drive/{model_save_name}" 
torch.save(model.state_dict(), path)

