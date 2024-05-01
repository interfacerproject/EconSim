import numpy as np
import pandas as pd
import gc

from .globals import get_debug

from .globals import PRODUCERS_ID_OFFSET

# calculate the gini coefficient of inequality
def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = len(model.schedule.agents)
    if sum(x) == 0:
        if get_debug():
            print("Sum of agents Wealth is zero")
        return 0
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))

    res = max(0, min(1,1 + (1 / N) - 2 * B))
    return res

# def compute_gini(model)->float:
#     agent_wealths = [agent.wealth for agent in model.schedule.agents]
#     x = np.sort(agent_wealths)
#     N = len(x)
#     cumx = np.cumsum(x, dtype=float)
#     if cumx[-1] == 0:
#         # set_trace()
#         return 0.0
#     # Formula when all weights are equal to 1
#     res = max(0, min(1,(N + 1 - 2 * np.sum(cumx) / cumx[-1]) / N))
#     return res

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
        return "Designer"
    elif id >= PRODUCERS_ID_OFFSET:
        return "Producer"
    else:
        raise Exception(f"Unkwown class id: {id}")

def gen_range(minv, maxv, nr_steps):
    step = int((maxv+1-minv)/nr_steps)
    return range(minv, maxv+1, step)


def generate_ranges(weight_array=True):

    range_living_cost = [x / 10.0 for x in gen_range(1,10,5)]
    range_threshold = [x / 10.0 for x in gen_range(-40, 40, 8)]
    # range_threshold = [1]
    range_resources = gen_range(500, 4000, 5)
    
    if weight_array:
        range_weights = []
        for price in [x / 10.0 for x in gen_range(1, 10, 3)]:
            for quality in [x / 10.0 for x in range(0, 11)]:
                for sustainabilty in [x / 10.0 for x in range(0, 11)]:
                    if price + quality + sustainabilty != 1:
                        continue
                    else:
                        range_weights.append([-price, quality, sustainabilty])
        # breakpoint()
        print(f"Parameters Combinations: {len(range_living_cost)*len(range_threshold)*len(range_resources)*len(range_weights)}")
        return range_weights, range_living_cost, range_threshold, range_resources

    # breakpoint()
    else:
        price_weight = [x / 10.0 for x in range(1, 11)]
        quality_ratio = [x / 10.0 for x in range(0, 11)]

        # print(f"Parameters Combinations: {len(range_living_cost)*len(range_threshold)*len(range_resources)*len(price_weight)*len(quality_ratio)}")
        return price_weight, quality_ratio, range_living_cost, range_threshold, range_resources


def gen_weights(price_weight, quality_ratio):
    rest = 1 - price_weight
            
    sustainability_weight = round(rest*(1-quality_ratio),1)
    quality_weight = round(rest*(quality_ratio),1)

    rest = 1 - (price_weight + quality_weight + sustainability_weight)
    quality_weight += rest/2
    sustainability_weight += rest/2
    
    weights = [-price_weight, quality_weight, sustainability_weight]
    return weights

def results_to_df(results):

    print(f"Nr rows in results: {len(results)}")
    results_df = pd.DataFrame(results)
    
    na_cols = results_df.columns[results_df.isna().any()].tolist()
    if na_cols != []:
        print(f"NaN present in {na_cols}")
        results_df = results_df.fillna(0, inplace=True)
    
    # make esplicit some parameters
    results_df["AgentType"], results_df["Alive"], results_df["price_weight"], results_df["quality_weight"], results_df["sustainability_weight"] = \
    zip(*results_df.apply(lambda row : (agent_type(row['AgentID']),row.Wealth>0, *row.weights), axis=1))

    print(f"Keys in results: {results_df.keys()}")

    print(f"Head:\n{results_df.head(5)}")
    print(f"Tail:\n{results_df.tail(5)}")

    return results_df

def process_batch_results(results_df, slice):

    # we do not consider 'method', 'initial_wealth', designers', 'producers' as these parameters
    # are not varied during the simulations 
    if slice == "Agents":
        ag_df = (
            results_df.groupby(["Step", "AgentType", "Skill", "Fee", "Sustainability", "living_cost", "resources_amount", "price_weight", "quality_weight", "sustainability_weight", "threshold"])
            .agg({
                "Wealth": "mean", 
                # "Work": "mean",
                "Alive": "mean",
                "Resources": "mean",
                })
            .reset_index()
        )

    elif slice == "Gini":
        ag_df = (
            results_df.groupby(["Step", "living_cost", "resources_amount", "price_weight", "quality_weight", "sustainability_weight", "threshold"])
            .agg({
                "Gini": "mean",
                })
            .reset_index()
        )
    elif slice == "Score":
        ag_df = (
            results_df.groupby(["Step", "resources_amount", "price_weight", "quality_weight", "sustainability_weight"])
            .agg({
                "Max Score": ["min", "max"],
                })
            .reset_index()
        )

    elif slice == "Products":
        ag_df = (
            results_df.groupby(["Step", "living_cost", "resources_amount", "price_weight", "quality_weight", "sustainability_weight","threshold"])
            .agg({ 
                "Designs in Progress": "mean", 
                "Realized Designs": "mean", 
                "Products in Progress": "mean",
                "On-sale Products": "mean", 
                "Sold Products": "mean",
                "Resources": "mean",
                })
            .reset_index()
        )

    print(f"For slice {slice}:\n")
    print(f"Head agents:\n{ag_df.head(3)}")
    print(f"Tail agents:\n{ag_df.tail(3)}")

    return ag_df


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
    
    print(f"The param statistics:\n{stats}")
    return stats
                    
                
