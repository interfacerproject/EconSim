from .makeragent import MakerAgent

class ServiceProvider(MakerAgent):
    """Create a product from open designs in the FabLabs ecosystem"""
    def __init__(self, unique_id, model, initial_wealth, living_cost):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model, initial_wealth, living_cost)

    def work(self):
        self.provide_service()

    def provide_service(self):
        # search whether a service can be provided
        pass
