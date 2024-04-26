import numpy as np
import pandas as pd

from .globals import PRODUCERS_ID_OFFSET

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


def agent_type(id):
    if id < PRODUCERS_ID_OFFSET:
        return("Designer")
    elif id >= PRODUCERS_ID_OFFSET:
        return("Producer")
    else:
        raise Exception(f"Unkwown class id: {id}")

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
    price_weight = [x / 10.0 for x in range(0, 11, step)]
    quality_ratio = [x / 10.0 for x in range(0, 11, step)]
    range_living_cost = [x / 10.0 for x in range(1, 11, step)]
    range_threshold = [x / 10.0 for x in range(1, 11, step)]
    range_resources = range(500, 10000, 500)

    return range_weights, price_weight, quality_ratio, range_living_cost, range_threshold, range_resources


def process_batch_results(results):

    print(len(results))
    results_df = pd.DataFrame(results)
    
    na_cols = results_df.columns[results_df.isna().any()].tolist()
    if na_cols != []:
        print(f"NaN present in {na_cols}")
        results_df = results_df.fillna(0, inplace=True)
    print(results_df.keys())

    print(f"Head:\n{results_df.head(5)}")
    print(f"Tail:\n{results_df.tail(5)}")

    results_df["AgentType"], results_df["Alive"], results_df["price_weight"], results_df["quality_weight"], results_df["sustainability_weight"] = \
        zip(*results_df.apply(lambda row : (agent_type(row['AgentID']),row.Wealth>0, *row.weights), axis=1))


    ag_res_df = (
        results_df.groupby(["Step", "AgentType", "Skill", "Fee", "Sustainability", "living_cost", "price_weight", "quality_weight", "sustainability_weight", "threshold"])
        .agg({
            "Wealth": "mean", 
            # "Work": "mean",
            "Alive": "mean",
            })
        .reset_index()
    )

    ag_glob_df = (
        results_df.groupby(["Step", "living_cost", "price_weight", "quality_weight", "sustainability_weight", "threshold"])
        .agg({
            "Gini": "mean",
            })
        .reset_index()
    )

    product_results_df = (
        results_df.groupby(["Step", "living_cost", "threshold"])
        .agg({ 
            "Designs in Progress": "mean", 
            "Realized Designs": "mean", 
            "Products in Progress": "mean",
            "On-sale Products": "mean", 
            "Sold Products": "mean",
            })
        .reset_index()
    )

    print(f"Head agents:\n{ag_res_df.head(3)}")
    print(f"Tail agents:\n{ag_res_df.tail(3)}")
    print(f"Head global:\n{ag_glob_df.head(3)}")
    print(f"Tail global:\n{ag_glob_df.tail(3)}")
    print(f"Head products:\n{product_results_df.head(3)}")
    print(f"Tail products:\n{product_results_df.tail(3)}")

    return ag_res_df, ag_glob_df, product_results_df


def gen_stats(max_steps, range_weights, range_living_cost, range_threshold, ag_res_df):
    stats = {}
    for pw,qw,sw in range_weights:
        if "price_weight" not in stats:
            stats["price_weight"] = {f"{pw}": 0, f"{pw}_alive": 0}
        elif f"{pw}" not in stats["price_weight"]:
            stats["price_weight"][f"{pw}"] = 0
            stats["price_weight"][f"{pw}_alive"] = 0
        if "quality_weight" not in stats:
            stats["quality_weight"] = {f"{qw}": 0, f"{qw}_alive": 0}
        elif f"{qw}" not in stats["quality_weight"]:
            stats["quality_weight"][f"{qw}"] = 0
            stats["quality_weight"][f"{qw}_alive"] = 0
        if "sustainability_weight" not in stats:
            stats["sustainability_weight"] = {f"{sw}": 0, f"{sw}_alive": 0}
        elif f"{sw}" not in stats["sustainability_weight"]:
            stats["sustainability_weight"][f"{sw}"] = 0
            stats["sustainability_weight"][f"{sw}_alive"] = 0
        for lc in range_living_cost:
            if "living_cost" not in stats:
                stats["living_cost"] = {f"{lc}": 0, f"{lc}_alive": 0}
            elif f"{lc}" not in stats["living_cost"]:
                stats["living_cost"][f"{lc}"] = 0
                stats["living_cost"][f"{lc}_alive"] = 0
            for t in range_threshold:
                if "threshold" not in stats:
                    stats["threshold"] = {f"{t}": 0, f"{t}_alive": 0}
                elif f"{t}" not in stats["threshold"]:
                    stats["threshold"][f"{t}"] = 0
                    stats["threshold"][f"{t}_alive"] = 0
                    
                data=ag_res_df.loc[ (ag_res_df["price_weight"] == pw) & 
                    (ag_res_df["quality_weight"] == qw) & 
                    (ag_res_df["sustainability_weight"] == sw) & 
                    (ag_res_df["living_cost"] == lc) & 
                    (ag_res_df["threshold"] == t)
                ]
                last_step = max(data["Step"])
                if last_step < max_steps:
                    print(f"{last_step} steps, weights: {pw},{qw},{sw}, living cost: {lc}, threshold: {t}")
                    continue
                alive_designers = np.mean(data.loc[(data["Step"] == last_step) & (data["AgentType"] == "Designer"), "Alive"])
                alive_producers = np.mean(data.loc[(data["Step"] == last_step) & (data["AgentType"] == "Producer"), "Alive"])
                if alive_designers == 1.0 and alive_producers == 1.0:
                    print(f"All Alive, weights: {pw}, {qw},{sw}, living cost: {lc}, threshold: {t}")
                    stats["price_weight"][f"{pw}_alive"] = stats["price_weight"][f"{pw}_alive"] + 1
                    stats["quality_weight"][f"{qw}_alive"] = stats["quality_weight"][f"{qw}_alive"] + 1
                    stats["sustainability_weight"][f"{sw}_alive"] = stats["sustainability_weight"][f"{sw}_alive"] + 1
                    stats["living_cost"][f"{lc}_alive"] = stats["living_cost"][f"{lc}_alive"] + 1
                    stats["threshold"][f"{t}_alive"] = stats["threshold"][f"{t}_alive"] + 1
                    continue
                # print(f"With weight: {pw}, living cost: {lc}, threshold: {t} there are {alive_designers} alive designers and {alive_producers} alive producers ")
                
                stats["price_weight"][f"{pw}"] = stats["price_weight"][f"{pw}"] + 1
                stats["quality_weight"][f"{qw}"] = stats["quality_weight"][f"{qw}"] + 1
                stats["sustainability_weight"][f"{sw}"] = stats["sustainability_weight"][f"{sw}"] + 1
                stats["living_cost"][f"{lc}"] = stats["living_cost"][f"{lc}"] + 1
                stats["threshold"][f"{t}"] = stats["threshold"][f"{t}"] + 1
    return stats
                    
                
