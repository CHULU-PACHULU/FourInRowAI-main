import math
import random
from typing import Any
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

# Parameters
input_size = 43  # state: board = 6*7 + action 1
layer1 = 128
layer2 = 64
output_size = 1  # Q(s,a)
gamma = 0.99
MSELoss = nn.MSELoss()

class DQN(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        if torch.cuda.is_available():
            self.device = torch.device('cuda')  # use 'cuda' if available
        else:
            self.device = torch.device('cpu')
        
        # Convolutional layers to process the board (e.g., 6x7)
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)  # 32 filters, 3x3 kernel
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)  # 64 filters, 3x3 kernel
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)  # 128 filters, 3x3 kernel
        
        # Fully connected layers after convolution
        self.fc1 = nn.Linear(128 * 6 * 7 + 1, layer1)  # Adjusted input size to 5377 (128 * 6 * 7 + 1 for the action)
        self.fc2 = nn.Linear(layer1, layer2)
        self.output = nn.Linear(layer2, output_size)
    
    def forward(self, x):
        # Apply convolutional layers
        x = F.relu(self.conv1(x))  # Apply ReLU after each Conv layer
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        
        # Flatten the output from Conv layers to feed into FC layers
        x = x.view(x.size(0), -1)  # Flatten the output (batch_size, channels, height, width) -> (batch_size, channels*height*width)
        
        return x  # This will return the flattened convolutional output

    def load_params(self, path):
        self.load_state_dict(torch.load(path))

    def save_params(self, path):
        torch.save(self.state_dict(), path)

    def copy(self):
        new_DQN = DQN()
        new_DQN.load_state_dict(self.state_dict())
        return new_DQN
    
    def loss(self, Q_value, rewards, Q_next_Values, Dones):
        Q_new = rewards + gamma * Q_next_Values * (1 - Dones)
        return MSELoss(Q_value, Q_new)

    def __call__(self, states, actions):
        # Ensure the batch_size is correctly extracted
        batch_size = states.size(0)  # Get the batch size
        
        # Separate the board and the action
        board = states
        action = actions.unsqueeze(1)  # Reshaping action to ensure it has the shape (batch_size, 1)

        # Debugging: Check the shape of the board
        
        # Reshape the board into a 6x7 grid
        board = board.view(batch_size, 1, 6, 7)  # Reshape the board part into shape (batch_size, 1, 6, 7)

        # Apply convolutional layers and flatten the output
        x = self.forward(board)
        
        # Now, we need to concatenate the action with the output
        # Ensure that action tensor is reshaped to have the same number of dimensions as x before concatenating
        action = action.view(batch_size, 1)  # (batch_size, 1)
        
        # Concatenate the flattened output with the action (which is of shape (batch_size, 1))
        x = torch.cat((x, action), dim=1)  # Concatenate along the second dimension

        # Now, pass the concatenated result through the fully connected layers
        x = F.relu(self.fc1(x))  # Feed the flattened output and action
        x = F.relu(self.fc2(x))
        x = self.output(x)

        return x
