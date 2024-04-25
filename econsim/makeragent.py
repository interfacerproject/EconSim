import mesa
import numpy as np


class MakerAgent(mesa.Agent):
    """An agent in the FabLabs ecosystem"""
    MIN_QUALITY = 1
    MAX_QUALITY = 2
    MIN_FEE = 1
    MAX_FEE = 2
    MIN_SUS = 1
    MAX_SUS = 2



    def __init__(self, unique_id, model, initial_wealth, living_cost):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model)

        # 
        self.wealth = initial_wealth
        self.living_cost = living_cost

        self.is_busy = False
        self.worked_hours = 0
        self.working_on_id = None

        self.quality_level = np.random.randint(MakerAgent.MIN_QUALITY,MakerAgent.MAX_QUALITY+1)
        self.sustainability_level = np.random.randint(MakerAgent.MIN_SUS,MakerAgent.MAX_SUS+1)
        # self.hour_fee = min(max(self.quality_level+delta_fee,MakerAgent.MIN_FEE),MakerAgent.MAX_FEE)
        
        self.hour_fee = min(max(np.mean([self.quality_level, self.sustainability_level]),MakerAgent.MIN_FEE),MakerAgent.MAX_FEE)


   
    def step(self):
        if self.wealth <= 0:
            # agent is starved, no activity
            # until possibly getting money from a sale
            return

        # TODO: Does the cost of living go on also for starved agents?
        self.wealth = self.wealth - self.living_cost
        if self.is_busy:
            self.worked_hours += 1
            if self.work_is_done():
                self.finish_work()
        else:
            self.work()
