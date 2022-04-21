AVERAGE_ROUTERS_PER_NODE=(1 1.5 3 5)
ROUTERS_TIER_2=(1 2 3 5 10 20 50 100 250 500 1000)
router_recovery_rate_range=(1 5 10 20 40 50)

export csv_name="architecture_results"

for recovery_rate in ${router_recovery_rate_range[@]}; do
    for router_per_node in ${AVERAGE_ROUTERS_PER_NODE[@]}; do
        for routers_total in ${ROUTERS_TIER_2[@]}; do
            echo "Running with $router_per_node routers per node and $routers_total total routers"
            export network_recovery_rate=$recovery_rate
            export routers_tier_2=$routers_total
            export average_routers_per_node=$router_per_node
            ../venv/bin/python3 run.py
        done
    done
done