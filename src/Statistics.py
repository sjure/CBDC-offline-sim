from Config import InputsConfig as p


class Statistics:
    # TX data
    online_tx = 0
    online_tx_volume = 0
    offline_tx = 0
    offline_tx_volume = 0

    # Fraud tx data
    fradulent_tx_successes = 0
    fradulent_tx_failures = 0
    fradulent_tx_success_volume = 0
    fradulent_tx_failures_volume = 0

    # HW failures
    network_failures = 0
    intermediary_failures = 0
