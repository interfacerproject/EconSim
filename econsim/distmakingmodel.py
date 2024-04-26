import mesa
import math
import numpy as np

from .work import Work
from .designer import Designer
from .producer import Producer
from .makeragent import MakerAgent
from .serviceprovider import ServiceProvider
from .market import Market
from .utils import compute_gini, agent_type
from .resources import Resources
from .globals import get_debug, PRODUCERS_ID_OFFSET, DESIGNERS_ID_OFFSET, MAX_SUS



class DistMakingModel(mesa.Model):
    """
        A model to simulate a fair distribution between makers
        based on DIDO principles.
    """
    def __init__(self, designers=20, producers=5, initial_wealth=10, living_cost=0.1, weights=[-1/3,1/3,1/3], threshold=0.1, competition=10, resources_amount=500, quality_ratio=None, method=1):
        super().__init__()
        
        # breakpoint()
        if quality_ratio != None:
            rest = 1 - weights
            
            sustainability_weight = round(rest*(1-quality_ratio),1)
            quality_weight = round(rest*(quality_ratio),1)

            rest = 1 - (weights + quality_weight + sustainability_weight)
            quality_weight += rest/2
            sustainability_weight += rest/2
            
            weights = [-weights, quality_weight, sustainability_weight]

        # Parameters for the market
        self.market = Market(weights, threshold, competition)

        Resources.init(resources_amount, MAX_SUS)
        
        self.initial_wealth = initial_wealth
        self.living_cost = living_cost
        
        self.schedule = mesa.time.RandomActivation(self)
        width = int(math.sqrt(designers+producers))+1
        height = width
        self.grid = mesa.space.MultiGrid(width, height, torus=True)
        
        # Init the designs
        Work.init_works(self, method)
        
        # Create agents
        count = 0
        for i in range(DESIGNERS_ID_OFFSET, DESIGNERS_ID_OFFSET + designers):
            a = Designer(i, self, initial_wealth, living_cost)
            self.schedule.add(a)
            self.grid.place_agent(a, (count%width, int(count/height)))
            count = count + 1

        for i in range(PRODUCERS_ID_OFFSET, PRODUCERS_ID_OFFSET + producers):
            a = Producer(i, self, initial_wealth, living_cost)
            self.schedule.add(a)
            self.grid.place_agent(a, (count%width, int(count/height)))
            count = count + 1


        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": compute_gini,
                             "Designs in Progress": Work.get_len_designs_in_progress,
                             "Realized Designs": Work.get_len_realized_designs,
                             "Products in Progress": Work.get_len_products_in_progress,
                             "On-sale Products": Work.get_len_on_sale_products,
                             "Sold Products": Work.get_len_sold_products,
                             "Resources": Resources.get_amount_resources,
                             "Contributors" : Work.get_avrg_contr_sold_goods,
                             "Hours": Work.get_avrg_hours_sold_goods,
                             "Price": Work.get_avrg_prices_sold_goods,
                             "Quality": Work.get_avrg_quality_sold_goods,
                             "Sustainability": Work.get_avrg_sus_sold_goods,
                             "Material Cost": Work.get_avrg_mat_cost_sold_goods
                            },
            agent_reporters={"Wealth": "wealth",
                            #  "Work": "worked_hours",
                             "Skill": "quality_level",
                             "Fee": "hour_fee",
                             "Sustainability": "sustainability_level",
                            }
            )
        self.running = True
    
    def step(self):
        """Advance the model by one step."""
        self.datacollector.collect(self)
        self.schedule.step()

        self.market.step()

        if not self.alive_professionals():
            if get_debug():
                print("Professionals starved, terminating")
            self.running = False
        
        
    def alive_professionals(self):
        designers_alive = False
        producers_alive = False
        for agent in self.schedule.agents:
            if agent.wealth > 0:
                ag_typ = agent_type(agent.unique_id)
                if ag_typ == "Designer":
                    designers_alive = True
                elif ag_typ == "Producer":
                    producers_alive = True
            if (designers_alive and producers_alive):
                return True
        return(designers_alive and producers_alive)


    def find_agent(self, id):
        for agent in self.schedule.agents:
            if agent.unique_id == id:
                return agent
        return(None)

    def run_model(self, step_count=200):
        for i in range(step_count):
            self.step()
    