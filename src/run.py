import os
from Simulate import Simulate

average_routers_per_node = float(
    os.environ.get('average_routers_per_node', "Not set"))
routers_tier_2 = int(os.environ.get('routers_tier_2', "Not set"))

print(average_routers_per_node, routers_tier_2)
Simulate.run()
Simulate.log_results()
