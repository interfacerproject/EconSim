import mesa

from econsim.distmakingmodel import DistMakingModel
from econsim.utils import generate_ranges, process_batch_results, gen_stats, set_debug

def main(iterations, max_steps, step):
    range_weights, _price_weight, _quality_ratio, range_living_cost, range_threshold, range_resources = generate_ranges(step)


    params = {"designers": 90, 
            "producers": 90, 
            "initial_wealth":10, 
            "weights": range_weights, 
            "living_cost": range_living_cost, 
            "threshold": range_threshold,
            "resources_amount": range_resources
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


    ag_res_df, ag_glob_df, product_results_df = process_batch_results(results, DistMakingModel.agent_type)

    stats = gen_stats(max_steps, range_weights, range_living_cost, range_threshold, ag_res_df)

    print(f"The param statistics:\n{stats}")

    breakpoint()
    prod_df = ag_res_df.loc[(ag_res_df['AgentType'] == 'Producer') & (ag_res_df['Step'] == max_steps)]
    for skill in [1,2,3]:
        for sus in [1,2,3]:
            for fee in [1,2,3]:
                for cost in range_living_cost:
                    slice = prod_df.loc[(prod_df['Skill'] == skill) & (prod_df['Sustainability'] == sus) & (prod_df['Fee'] == fee) & (prod_df['living_cost'] == cost)]
                


    prod_df = ag_res_df.loc[(ag_res_df['AgentType'] == 'Producer') & (ag_res_df['Skill'] == 1) & (ag_res_df['Sustainability'] == 3) & (ag_res_df['Fee'] == 1) & (ag_res_df['Step'] == max_steps)] 

    ag_res_df.loc[(ag_res_df['AgentType'] == 'Producer') & (ag_res_df['Skill'] == 1) & (ag_res_df['Sustainability'] == 3) & (ag_res_df['Fee'] == 1) & (ag_res_df['Step'] == max_steps)] 




if __name__ == "__main__":
    import argparse
    from six import text_type    

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
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
            args.iterations, args.max_steps, args.step
        )
