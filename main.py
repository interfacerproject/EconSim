import gc
import mesa

from econsim.distmakingmodel import DistMakingModel
from econsim.utils import generate_ranges, results_to_df, process_batch_results, gen_stats
from econsim.globals import set_debug

def main(iterations, max_steps, step, method):

    range_weights, range_living_cost, range_threshold, range_resources = generate_ranges(weight_array=True)


    params = {
            "method": method,
            "designers": 60, 
            "producers": 40, 
            "initial_wealth":10,
            "living_cost": range_living_cost,
            "resources_amount": range_resources,
            "weights": range_weights,
            "threshold": range_threshold,
            }

    # breakpoint()

    results = mesa.batch_run(
        DistMakingModel,
        parameters=params,
        iterations=iterations,
        # max_steps=max_steps-1, # steps start from 0
        max_steps=max_steps,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )

    results_df = results_to_df(results)

    del results
    gc.collect()
    
    score_df = process_batch_results(results_df, "Score")
    print(f"Min score: {min(score_df['Max Score']['min'])}, max score: {max(score_df['Max Score']['max'])}")
    
    price_weights = set([price_weight for price_weight, _quality_weight, _sustainability_weight in range_weights])
    for resources_amount in range_resources:
        for price_weight in price_weights:
            slice = score_df.loc[
                                    (score_df['resources_amount'] == resources_amount) &
                                    (score_df['price_weight'] == price_weight)
                                    ]
            if len(slice) == 0:
                continue
            print(f"For resources_amount: {resources_amount}, price_weight: {price_weight}")
            print(f"Min: {min(slice['Max Score']['min'])}, max: {max(slice['Max Score']['max'])}")
    
    # breakpoint()
    del score_df
    gc.collect()
    
    
    ag_res_df = process_batch_results(results_df,slice="Agents")

    gen_stats(max_steps, range_weights, range_living_cost, range_threshold, ag_res_df)


    # breakpoint()
    end_df = ag_res_df.loc[(ag_res_df['Step'] == max_steps)]
    for ag in ['Producer', 'Designer']:
        a_df = end_df.loc[(ag_res_df['AgentType'] == ag)]
        print(f"Agent type: {ag}")
        for skill in [1,2]:
            for sus in [1,2]:
                slice = a_df.loc[(a_df['Skill'] == skill) & (a_df['Sustainability'] == sus)]
                if len(slice) == 0:
                    print(f"No survivors for skill: {skill}, Sustenaibility: {sus}")
                    continue  
                mw = max(slice['Wealth'])
                print(f"Skill: {skill}, Sustenaibility: {sus}")
                print(slice.loc[(slice['Wealth'] >= mw*.9)])

    # breakpoint()




if __name__ == "__main__":
    import argparse
    from six import text_type    

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        '-c', '--compensation',
        dest='compensation',
        type=int,
        nargs='?',
        default=1,
        help='specifies the method to share profits',
    )

    parser.add_argument(
        '-d', '--debug',
        dest='debug',
        action='store_true',
        default=False,
        help='specifies whether to print debug statements',
    )

    parser.add_argument(
        '-i', '--iterations',
        dest='iterations',
        type=int,
        nargs='?',
        default=1,
        help='specifies the number of iterations',
    )

    parser.add_argument(
        '-m', '--max_steps',
        dest='max_steps',
        type=int,
        nargs='?',
        default=1,
        help='specifies the max numer of steps per iteration',
    )

    parser.add_argument(
        '-s', '--step',
        dest='step',
        type=int,
        nargs='?',
        default=1,
        help='specifies the step size in range of parameters',
    )

    args, unknown = parser.parse_known_args()

    if args.debug:
        set_debug()

    main(
            args.iterations, args.max_steps, args.step, args.compensation
        )
