

class Resources():
    amount = 0
    max_sustainability = 0

    @classmethod
    def init(cls, initial_amount, max_sustainability):
        # breakpoint()
        cls.initial_amount = initial_amount
        cls.current_amount = cls.initial_amount
        cls.max_sustainability = max_sustainability

    @classmethod
    def get_amount_resources(cls):
        return cls.amount
    

    @classmethod
    def calculate_depletion(cls, design_sustainability, product_sustainability):
        # breakpoint()
        comsumption = cls.max_sustainability -(design_sustainability+product_sustainability)/2
        cost = comsumption / (cls.current_amount/cls.initial_amount)
        cls.current_amount = cls.current_amount - comsumption
        return cost


    @classmethod
    def resourses_available(cls):
        if cls.amount < 0:
            # breakpoint()
            print("Resources depleted")
            return False
        return True

        

