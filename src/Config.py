import os


class InputsConfig:
    """ Input config for the module """
    random_seed = 42
    tx_limit = 10000
    tx_per_node = 50
    graph_type = "mesh"
    graph_params = {
        "n": 1000,
        "m": 8,
    }

    average_routers_per_node = float(
        os.environ.get('average_routers_per_node', 40))
    routers_tier_2 = int(os.environ.get('routers_tier_2', 40))

    fraud_node_percentage = 0.1
    tx_rate = 5
    tx_rate_fraud = 5
    tx_volume = {
        "mean": 100,
        "std": 40
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
        "mean": 1_000_000,
        "std": 0
    }
    network_failure_rate = 20
    network_recovery_rate = 5
    intermediary_failure_rate = 30
    intermediary_recovery_rate = 5
    broadcast_coverage = 0.4

    # Testing parameters
    intemediary_refund_payee_fradulent_transactions = True
    per_tx_amount_limit = 1000
    lockout_after_consolidation = False
    client_preventions = False
    collaberative_security = False
