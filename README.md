# EconSim rationale
Simulate value distribution in maker networks

## Fablab simulation experiment
The model in this repository is not validated economic model, but serves as a tool to generate thoughts.

Our world is inspired by the DIDO/Fablabs model. There are 2 types of agents:
1. Designers create designs from scratch or modify existing designs
2. Producers use a design to create a product

All designs are public so that they can be modified or used for a product

###  Designers and Producers
Designers and producers have:
- A high (2) or low (1) **skill level/quality** (influences the quality of the design/product)
- A high (2) or low (1) **sustainability** (influences the consumption of resources)
- An **hour fee** which is (quality+sustainability)/2
- An initial amount of **money**

They act at random:
- **Designers** randomly choose to generate a new design or modify an existing one
- **Producers** randomly choose a design to produce (if possible)

### Environment and market
The **environment** where the agents act has 2 properties:
- **Cost of living**: how much wealth each agent spends for each step of the simulation
- **Resources**: the amount of resources that can be used to produce a product

The **market** buys the products from the producers, subject to these properties:
- How important the price of the product is, with respect to its quality/sustainability
- Whether quality is more important than sustainability or vice versa
- How high the threshold to buy a product is

### Redistribution schemes
There are 3 redistribution schemes:
1. Only producers are rewarded (the one who sells keeps the profit)
2. Each designer involved in the design and the producer get an equal share of the profit
3. Each designer involved in the design and the producer get a share of the profit proportional to their hour fee

Depending on the redistribution scheme, the price of the product is
1. Only the fee of the producer
2. A sum of an average fee per participant
3. The sum of the actual fees of each participant

There is also a **material cost** per product that increases the more the resources are consumed.

# Installation

1. Clone this repository to a directory and cd to it.
2. Install python if not present. It is suggested to do so via virtual environment manager such as [miniconda](https://docs.anaconda.com/free/miniconda/).
3. If using conda, create an environment, e.g. `conda create -n econsim python==3.11` and activate it `conda activate econsim`.
4. Install [Jupyter notebook](https://jupyter.org/install): `pip install notebook`
5. Install various dependencies: `pip install "mesa<3" numpy pandas seaborn`
6. Run the notebook `jupyter notebook` and from the browser page that it launches open the file `faircontr_int.ipynb`, which is the main simulation
7. Run the notebook and at the last cell you can run the simulation, change the parameters, etc.

The repository also contains two other notebooks:
1. `faircontr_expl.ipynb`, run simulations as a batch and displays some graphs, work in progress
2. `money_model.ipynb` is the simulation taken from the [mesa tutorial](https://mesa.readthedocs.io/en/stable/tutorials/intro_tutorial.html) on the Boltzmann model of wealth distribution

Batch simulations can also be run with `python main.py`, have a look at the code to see what parameters can be given.




