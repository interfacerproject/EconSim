
from .globals import get_debug

class Resources():
    initial_amount = 0
    current_amount = 0
    max_sustainability = 0

    @classmethod
    def init(cls, initial_amount, max_sustainability):
        # breakpoint()
        cls.initial_amount = initial_amount
        cls.current_amount = cls.initial_amount
        cls.max_sustainability = max_sustainability

    @classmethod
    def get_amount_resources(cls):
        return cls.current_amount
    

    @classmethod
    def calculate_depletion(cls, design_sustainability, product_sustainability):
        # breakpoint()
        comsumption = cls.max_sustainability -(design_sustainability+product_sustainability)/2
        cost = comsumption / (cls.current_amount/cls.initial_amount)
        cls.current_amount = max(cls.current_amount - comsumption,0)
        if get_debug():
                print(f"Cost depletion: {cost}")
        if cost < 0:
             raise Exception(f"Material cost is negative, should not happen")
        return cost


    @classmethod
    def resourses_available(cls):
        if cls.current_amount <= 0:
            # breakpoint()
            if get_debug():
                print("Resources depleted")
            return False
        return True

        

