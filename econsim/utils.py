import numpy as np

# # calculate the gini coefficient of inequality
# def compute_gini(model):
#     agent_wealths = [agent.wealth for agent in model.schedule.agents]
#     x = sorted(agent_wealths)
#     N = len(model.schedule.agents)
#     if sum(x) == 0:
#         set_trace()
#     B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
#     return 1 + (1 / N) - 2 * B


def compute_gini(model)->float:
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = np.sort(agent_wealths)
    N = len(x)
    cumx = np.cumsum(x, dtype=float)
    if cumx[-1] == 0:
        # set_trace()
        return 0.0
    # Formula when all weights are equal to 1
    return (N + 1 - 2 * np.sum(cumx) / cumx[-1]) / N

def norml(x):
    # set_trace()
    if np.max(x)-np.min(x) == 0:
        # np.array(x)/2
        return np.array([0.5 for i in range(len(x))])
    else:
        den = np.max(x)-np.min(x)
        return (x-np.min(x))/den


def generate_ranges(step=1):
    range_weights = []
    for price in [x / 10.0 for x in range(0, 11, step)]:
        for quality in [x / 10.0 for x in range(0, 11, step)]:
            for sustainabilty in [x / 10.0 for x in range(0, 11, step)]:
                if price + quality + sustainabilty != 1:
                    continue
                else:
                    range_weights.append([-price, quality, sustainabilty])

    # range_price_weight = [x / 10.0 for x in range(2, 6, 1)]
    range_living_cost = [x / 10.0 for x in range(1, 11, step)]
    range_threshold = [x / 10.0 for x in range(1, 11, step)]
    range_competition = range(0, 5, step)
    range_resources = range(500, 10000, 500)

    return range_weights, range_living_cost, range_threshold, range_competition, range_resources
