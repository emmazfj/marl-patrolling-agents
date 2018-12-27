from utils import get_distance_between, distance_enemies_around


def sparse_reward(agents):
    """
    Gives a sparse reward at the end:
        - 0 for officers if target is alone and 1 for target
        - 1 for officer if target is surrounded and 0 for target
    Args:
        agents:
    Returns: list of rewards for every agent
    """
    rewards = []
    officer_won = False
    # Check who won
    for agent in agents:
        if agent.type == "target":
            num_officers_around = len(distance_enemies_around(agent, agents, max_distance=1))
            if num_officers_around >= 2:
                officer_won = True
    # Define reward for all agents
    for agent in agents:
        if agent.type == 'officer':
            if officer_won:
                rewards.append(1)
            else:
                rewards.append(0)
        else:
            if officer_won:
                rewards.append(0)
            else:
                rewards.append(1)
    return rewards


def full_reward(agents):
    """
    Gives a reward at each step:
    Args:
        agents:
    Returns: list of rewards for every agent
    """
    rewards = []
    for agent in agents:
        distances = distance_enemies_around(agent, agents)
        if agent.type == "target":
            reward = sum(distances) - len(distances) * agent.view_radius
        else:
            reward = - sum(distances)
        rewards.append(reward)
    return rewards