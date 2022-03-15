class InputsConfig:
    """ Input config for the module """
    tx_limit = 20
    graph_type = "ba"
    graph_params = {
        "n":10,
        "m":3,
    }
    fraud_node_percentage = 0.1
    tx_per_node = 20
    tx_rate = 5
    tx_rate_fraud = 2
    tx_volume={ 
        "mean": 10,
        "std": 10
    }
    balance = {
        "mean": 5000,
        "std": 2000
    }
    offline_balance_preferance = {
        "mean": 1500,
        "std": 500
    }
    fraud_user_balance_preferance = {
        "mean": 10e12,
        "std": 0
    }
    network_failure_rate = 10
    network_recovery_rate = 5
    intermediary_failure_rate = 20
    intermediary_recovery_rate = 5
