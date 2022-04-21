import os


class InputsConfig:
    """ Input config for the module """
    random_seed = 42
    tx_limit = 10000000
    tx_per_node = 10
    graph_type = "mesh"
    graph_params = {
        "n": 1000,
        "m": 20,
    }

    fraud_node_percentage = 0.1
    tx_rate = 5
    tx_rate_fraud = 5
    tx_volume = {
        "mean": 100,
        "std": 40
    }
    balance = {
        "mean": 10000,
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
    intermediary_failure_rate = 30
    intermediary_recovery_rate = 5
    broadcast_coverage = 0.2
    intemediary_refund_payee_fradulent_transactions = True

    # Testing parameters
    network_recovery_rate = int(
        os.environ.get('network_recovery_rate', 10))
    intermediary_recovery_rate = int(
        os.environ.get('intermediary_recovery_rate', 5))

    per_tx_amount_limit = int(os.environ.get('per_tx_amount_limit', 1000))
    lockout_after_consolidation = bool(
        int(os.environ.get('lockout_after_consolidation', False)))
    client_preventions = bool(
        int(os.environ.get('client_preventions', False)))
    collaberative_security = bool(
        int(os.environ.get('collaberative_security', False)))

    average_routers_per_node = float(
        os.environ.get('average_routers_per_node', 1.5))
    routers_tier_2 = int(os.environ.get('routers_tier_2', 3))
