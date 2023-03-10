'''
The following is a fully connected network that learns how to predict a specific mnist number
'''
from __future__ import division

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable
import numpy as np



'''Global variables'''
batch_sz = 64
epochs = 100
learning_rate = .0001
input_shape = 784
output_shape = 10
hidden_neurons = [250, 75, output_shape] #Depending on the number of layers in your nueral network this is the number of neurons for hidden layer x


'''Data loader for MNIST'''
kwargs = {'num_workers': 2, 'pin_memory': True} if torch.cuda.is_available() else {}

train_loader = torch.utils.data.DataLoader(
    datasets.MNIST('../data', train=True, download=True,
                   transform=transforms.Compose([
                       transforms.ToTensor()
                   ])),
    batch_size=batch_sz, shuffle=True, drop_last=True, **kwargs)

test_loader = torch.utils.data.DataLoader(
    datasets.MNIST('../data', train=False, transform=transforms.Compose([
                       transforms.ToTensor(),
                   ])),
    batch_size=batch_sz, shuffle=True, drop_last=True, **kwargs)

############################################# FOR STUDENTS #####################################
'''Model creation'''
class FullyConnectedNetwork(nn.Module):
    def __init__(self, input_dim, num_hidden_neurons):
        ###### Define Layers Of The Neural Network Here ######


    def forward(self, x):
        ###### Define Forward Method ######

model = #Initialize model
optimizer = #Initialize optimizer
#################################################################################################

print("\n")
print(model)
print("\n\n")


'''Train'''
def train(epoch):
    global model
    global optimizer

    model.train() #Set mode to be training mode for the model (affects batchnorm, dropout ect.)
    optimizer.zero_grad() #Zero all gradients
    train_loss = 0
    train_step_counter = 0

    for batch_idx, (data, target) in enumerate(train_loader):
        #Flatten the image data (64, 1, 28, 28) -> (64, 784)
        data = data.view(-1, input_shape)
        #Make tensor cuda tensor if cuda is available
        if torch.cuda.is_available():
            data, target = data.cuda(), target.cuda()
        #Make data and target Variable tensors
        data, target = Variable(data), Variable(target)

        output = model(data)
        loss = F.cross_entropy(output, target)
        train_loss+=loss.data
        train_step_counter +=1

        loss.backward() #Calculate dloss/dx
        optimizer.step() #Update weights of neural network based on gradients

    print('Train Epoch: {} \tLoss: {:.6f}'.format(
        epoch, train_loss.cpu().numpy()/train_step_counter))


'''Test'''
def test():
    global model
    global batch_sz
    model.eval()

    test_loss = 0
    correct = 0
    test_steps = 0

    for data, target in test_loader:
        data = data.view(-1, input_shape)

        if torch.cuda.is_available():
            data, target = data.cuda(), target.cuda()
        data, target = Variable(data), Variable(target)

        output = model(data)
        test_loss += F.cross_entropy(output, target).item() # Sum up batch loss
        pred = output.data.max(1, keepdim=True)[1] #Get the index of the max log-probability
        correct += pred.eq(target.data.view_as(pred)).sum()
        test_steps+=1

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.4f}%)'.format(
        test_loss/test_steps, correct, test_steps * batch_sz,
        100. * correct / (test_steps * batch_sz)))


'''Create model'''
if torch.cuda.is_available():
    model.cuda()
    print("Using GPU Acceleration")
else:
    print("Not Using GPU Acceleration")


'''Train and test our model'''
for epoch in range(epochs):
    train(epoch)
    if epoch % 2 == 0 and epoch != 0:
        with torch.no_grad():
            test()

with torch.no_grad():
    test()
