import mesa

from econsim.distmakingmodel import DistMakingModel

range_weights = []
for price in [x / 10.0 for x in range(0, 11, 2)]:
    for quality in [x / 10.0 for x in range(0, 11, 2)]:
        for sustainabilty in [x / 10.0 for x in range(0, 11, 2)]:
            if price + quality + sustainabilty != 1:
                continue
            else:
                range_weights.append([-price, quality, sustainabilty])



# range_price_weight = [x / 10.0 for x in range(2, 6, 1)]
range_living_cost = [x / 10.0 for x in range(1, 11, 2)]
range_threshold = [x / 10.0 for x in range(1, 11, 2)]
range_competition = range(0, 5, 1)
range_resources = range(500, 10000, 500)

params = {"designers": 90, 
          "producers": 90, 
          "initial_wealth":10, 
          "weights": range_weights, 
          "living_cost": range_living_cost, 
          "threshold": range_threshold,
          "competition": range_competition,
          "resources_amount": range_resources
          }

iterations = 1
max_steps=50


results = mesa.batch_run(
    DistMakingModel,
    parameters=params,
    iterations=iterations,
    # max_steps=max_steps-1, # steps start from 0
    max_steps=max_steps,
    number_processes=1,
    data_collection_period=-1,
    display_progress=True,
)


import pandas as pd

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
    zip(*results_df.apply(lambda row : (DistMakingModel.agent_type(row['AgentID']),row.Wealth>0, *row.weights), axis=1))


ag_res_df = (
    results_df.groupby(["Step", "AgentType", "Skill", "Fee", "Sustainability", "living_cost", "price_weight", "quality_weight", "sustainability_weight", "threshold", "competition"])
    .agg({
          "Wealth": "mean", 
          "Work": "mean",
          "Alive": "mean",
         })
    .reset_index()
)

ag_glob_df = (
    results_df.groupby(["Step", "living_cost", "price_weight", "quality_weight", "sustainability_weight", "threshold", "competition"])
    .agg({
          "Gini": "mean",
         })
    .reset_index()
)

product_results_df = (
    results_df.groupby(["Step", "living_cost", "threshold", "competition"])
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


import numpy as np
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
            for c in range_competition:
                if "competition" not in stats:
                    stats["competition"] = {f"{c}": 0, f"{c}_alive": 0}
                elif f"{c}" not in stats["competition"]:
                    stats["competition"][f"{c}"] = 0
                    stats["competition"][f"{c}_alive"] = 0
                
                data=ag_res_df.loc[ (ag_res_df["price_weight"] == pw) & 
                    (ag_res_df["quality_weight"] == qw) & 
                    (ag_res_df["sustainability_weight"] == sw) & 
                    (ag_res_df["living_cost"] == lc) & 
                    (ag_res_df["threshold"] == t) &
                    (ag_res_df["competition"] == c)
                ]
                last_step = max(data["Step"])
                if last_step < max_steps:
                    print(f"{last_step} steps, weights: {pw},{qw},{sw}, living cost: {lc}, threshold: {t} and competition: {c}")
                    continue
                alive_designers = np.mean(data.loc[(data["Step"] == last_step) & (data["AgentType"] == "Designer"), "Alive"])
                alive_producers = np.mean(data.loc[(data["Step"] == last_step) & (data["AgentType"] == "Producer"), "Alive"])
                if alive_designers == 1.0 and alive_producers == 1.0:
                    print(f"All Alive, weights: {pw}, {qw},{sw}, living cost: {lc}, threshold: {t} and competition: {c}")
                    stats["price_weight"][f"{pw}_alive"] = stats["price_weight"][f"{pw}_alive"] + 1
                    stats["quality_weight"][f"{qw}_alive"] = stats["quality_weight"][f"{qw}_alive"] + 1
                    stats["sustainability_weight"][f"{sw}_alive"] = stats["sustainability_weight"][f"{sw}_alive"] + 1
                    stats["living_cost"][f"{lc}_alive"] = stats["living_cost"][f"{lc}_alive"] + 1
                    stats["threshold"][f"{t}_alive"] = stats["threshold"][f"{t}_alive"] + 1
                    stats["competition"][f"{c}_alive"] = stats["competition"][f"{c}_alive"] + 1
                    continue
                # print(f"With weight: {pw}, living cost: {lc}, threshold: {t} and competition: {c} there are {alive_designers} alive designers and {alive_producers} alive producers ")
                
                stats["price_weight"][f"{pw}"] = stats["price_weight"][f"{pw}"] + 1
                stats["quality_weight"][f"{qw}"] = stats["quality_weight"][f"{qw}"] + 1
                stats["sustainability_weight"][f"{sw}"] = stats["sustainability_weight"][f"{sw}"] + 1
                stats["living_cost"][f"{lc}"] = stats["living_cost"][f"{lc}"] + 1
                stats["threshold"][f"{t}"] = stats["threshold"][f"{t}"] + 1
                stats["competition"][f"{c}"] = stats["competition"][f"{c}"] + 1
                
                

breakpoint()
prod_df = ag_res_df.loc[(ag_res_df['AgentType'] == 'Producer') & (ag_res_df['Step'] == max_steps)]
for skill in [1,2,3]:
    for sus in [1,2,3]:
        for fee in [1,2,3]:
            for cost in range_living_cost:
                slice = prod_df.loc[(prod_df['Skill'] == skill) & (prod_df['Sustainability'] == sus) & (prod_df['Fee'] == fee) & (prod_df['living_cost'] == cost)]
            


prod_df = ag_res_df.loc[(ag_res_df['AgentType'] == 'Producer') & (ag_res_df['Skill'] == 1) & (ag_res_df['Sustainability'] == 3) & (ag_res_df['Fee'] == 1) & (ag_res_df['Step'] == max_steps)] 

ag_res_df.loc[(ag_res_df['AgentType'] == 'Producer') & (ag_res_df['Skill'] == 1) & (ag_res_df['Sustainability'] == 3) & (ag_res_df['Fee'] == 1) & (ag_res_df['Step'] == max_steps)] 