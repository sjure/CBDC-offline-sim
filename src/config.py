class InputsConfig:
    """ Input config for the module """
    tx_limit = 1000
    graph_type = "ba"
    graph_params = {
        "n":10,
        "m":3,
    }
    tx_per_node= 10
    tx_rate= 0.5
    tx_volume={ 
        "mean": 10,
        "std": 10
    }
    balance = {
        "mean": 100,
        "std":20
    }