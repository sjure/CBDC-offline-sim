import os
from Simulate import Simulate

# Node network connectivity
average_routers_per_node = float(
    os.environ.get('average_routers_per_node', 2))

# Routers to connect to
routers_tier_2 = int(os.environ.get('routers_tier_2', 2))

# Offline length
intermediary_recovery_rate = int(
    os.environ.get('intermediary_recovery_rate', -5))

# Amount limits
per_tx_amount_limit = int(
    os.environ.get('per_tx_amount_limit', -1))

# Protocol enhancements
lockout_after_consolidation = bool(
    int(os.environ.get('lockout_after_consolidation', 0)))
client_preventions = bool(
    int(os.environ.get('client_preventions',  0)))
collaberative_security = bool(
    int(os.environ.get('collaberative_security',  0)))

Simulate.run()
Simulate.log_results()
