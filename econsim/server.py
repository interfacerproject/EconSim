import mesa
from econsim.designer import Designer
from econsim.producer import Producer
from econsim.serviceprovider import ServiceProvider
from econsim.resources import Resources

from econsim.distmakingmodel import DistMakingModel


def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Designer:
        portrayal["Shape"] = "econsim/resources/icons8-designer-64.png"
        # https://icons8.com/icon/9APE8Mw8ziYC/designer icon by https://icons8.com
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Producer:
        portrayal["Shape"] = "econsim/resources/icons8-producer-64.png"
        # https://icons8.com/icon/YdrIWceHZShx/producer icon by https://icons8.com
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.wealth, 1)
        portrayal["text_color"] = "White"

    elif type(agent) is ServiceProvider:
        if agent.fully_grown:
            portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
        else:
            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = mesa.visualization.CanvasGrid(agent_portrayal, 15, 15, 500, 500)
product_chart = mesa.visualization.ChartModule(
    [
        {"Label": "Designs in Progress", "Color": "#0000a2"},
        {"Label": "Realized Designs", "Color": "#bc272d"},
        {"Label": "Products in Progress", "Color": "#e9c716"},
        {"Label": "On-sale Products", "Color": "#50ad9f"},
        {"Label": "Sold Products", "Color": "#2b83ba"},
    ]
)
resources_chart = mesa.visualization.ChartModule(
    [
        {"Label": "Resources", "Color": "#0000a2"},
        # {"Label": "Realized Designs", "Color": "#bc272d"},
        # {"Label": "Products in Progress", "Color": "#e9c716"},
        # {"Label": "On-sale Products", "Color": "#50ad9f"},
        # {"Label": "Sold Products", "Color": "#2b83ba"},
    ]
)
agent_chart = mesa.visualization.BarChartModule(
    scope="agent",
    fields = [
        {"Label": "Wealth", "Color": "#0000a2"},
        # {"Label": "Realized Designs", "Color": "#bc272d"},
        # {"Label": "Products in Progress", "Color": "#e9c716"},
        # {"Label": "On-sale Products", "Color": "#50ad9f"},
        # {"Label": "Sold Products", "Color": "#2b83ba"},
    ]
)
import solara
from matplotlib.figure import Figure

def wealth_histogram(model):
    # Note: you must initialize a figure using this method instead of
    # plt.figure(), for thread safety purpose
    fig = Figure()
    ax = fig.subplots()
    wealth_vals = [agent.wealth for agent in model.schedule.agents]
    # Note: you have to use Matplotlib's OOP API instead of plt.hist
    # because plt.hist is not thread-safe.
    ax.hist(wealth_vals, bins=10)
    solara.FigureMatplotlib(fig)


price_weight = [x / 10.0 for x in range(0, 11, 2)]
quality_ratio = [x / 10.0 for x in range(0, 11, 2)]


# range_price_weight = [x / 10.0 for x in range(2, 6, 1)]
range_living_cost = [x / 10.0 for x in range(1, 11, 2)]
range_threshold = [x / 10.0 for x in range(1, 11, 2)]
range_competition = range(0, 5, 1)
range_resources = range(500, 10000, 500)


model_params = {
    "title": mesa.visualization.StaticText("Parameters:"),
    # "grass": mesa.visualization.Checkbox("Grass Enabled", True),
    "designers": mesa.visualization.Slider("Designers", 20, 0, 100, 1 ),
    "producers": mesa.visualization.Slider("Producers", 5, 0, 100, 1),
    "initial_wealth": mesa.visualization.Slider("Initial Wealth", 10, 0, 100, 1),
    "resources_amount": mesa.visualization.Slider("Resources", min(range_resources),min(range_resources),max(range_resources),100),
    "weights": mesa.visualization.Slider("Weight of price", min(price_weight),min(price_weight),max(price_weight),0.1),
    "quality_ratio": mesa.visualization.Slider("Ratio quality/sustainability", min(quality_ratio), min(quality_ratio),max(quality_ratio),0.1),
    "living_cost": mesa.visualization.Slider("Cost of Living", min(range_living_cost), min(range_living_cost),max(range_living_cost),0.1),
    "threshold": mesa.visualization.Slider("Threshold to buy",min(range_threshold),min(range_threshold),max(range_threshold),0.1),
    "competition": mesa.visualization.Slider("Min products on sale", 1,0,5,1),    
}

server = mesa.visualization.ModularServer(
    DistMakingModel, [product_chart, resources_chart, agent_chart, canvas_element], "Fair Distribution", model_params
    
)
server.port = 8522


