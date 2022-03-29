class InputsConfig:
    """ Input config for the module """
    tx_limit = 10000
    tx_per_node = 20
    graph_type = "ba"
    graph_params = {
        "n":100,
        "m":3,
    }
    fraud_node_percentage = 0.1
    tx_rate = 5
    tx_rate_fraud = 5
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
    network_failure_rate = 20
    network_recovery_rate = 5
    intermediary_failure_rate = 20
    intermediary_recovery_rate = 5
    
    client_preventions = False
    lockout_after_consolidation = False
    intemediary_refund_payee_fradulent_transactions = False
    per_tx_volume_limit = float("inf")
    collaberative_security = False
