import mesa
import numpy as np

from .globals import MIN_QUALITY, MAX_QUALITY, MIN_SUS, MAX_SUS, MIN_FEE, MAX_FEE
class MakerAgent(mesa.Agent):
    """An agent in the FabLabs ecosystem"""

    def __init__(self, model, initial_wealth, living_cost):
        # Pass the parameters to the parent class.
        super().__init__(model)

        # 
        self.wealth = initial_wealth
        self.living_cost = living_cost

        self.is_busy = False
        self.worked_hours = 0
        self.working_on_id = None

        self.quality_level = np.random.randint(MIN_QUALITY,MAX_QUALITY+1)
        self.sustainability_level = np.random.randint(MIN_SUS,MAX_SUS+1)
        # self.hour_fee = min(max(self.quality_level+delta_fee,MIN_FEE),MAX_FEE)
        
        self.hour_fee = min(max(np.mean([self.quality_level, self.sustainability_level]),MIN_FEE),MAX_FEE)


   
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
