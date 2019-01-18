import torch
import torch.nn as nn
from utils.config import Config

config = Config('./config')


class DQNUnit(nn.Module):

    def __init__(self):
        super(DQNUnit, self).__init__()

        n_actions = 7 if config.env.world_3D else 5
        self.n_agents = config.agents.number_preys + config.agents.number_predators
        n_obstacles = 2 * len(config.env.obstacles)
        self.fc = nn.Sequential(
            nn.Linear(self.n_agents * 3 + n_obstacles, 128),
            nn.ReLU(),
            nn.Linear(128, 16),
            nn.ReLU(),
            nn.Linear(16, n_actions),
        )

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        return self.fc(x)


class DQNCritic(nn.Module):
    def __init__(self):
        super(DQNCritic, self).__init__()

        # action_dim = 7 if config.env.world_3D else 5
        n_agents = config.agents.number_preys + config.agents.number_predators
        n_obstacles = 2 * len(config.env.obstacles)
        state_dim = n_agents * 3 + n_obstacles
        self.fc = nn.Sequential(
            nn.Linear(state_dim + n_agents, 128),
            nn.ReLU(),
            nn.Linear(128, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )

    def forward(self, x, actions):
        """
        Args:
            x: (batch_size, state_size)
            actions: [(batch_size, action_size)] list size n_agents
        Returns:
        """
        x = torch.cat([x, *actions], dim=1)
        return self.fc(x)


class DQNActor(nn.Module):
    def __init__(self):
        super(DQNActor, self).__init__()

        action_dim = 7 if config.env.world_3D else 5
        n_agents = config.agents.number_preys + config.agents.number_predators
        n_obstacles = 2 * len(config.env.obstacles)
        state_dim = n_agents * 3 + n_obstacles
        self.fc = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 32),
            nn.ReLU(),
            nn.Linear(32, action_dim),
            nn.Softmax(dim=1)
        )

    def forward(self, x):
        return self.fc(x)
