AVERAGE_ROUTERS_PER_NODE=(1 1.5 2 5)
ROUTERS_TIER_2=(1 2 3 5 8 10 20 50) # Up to amount of routers
router_recovery_rate_range=(1 5 10 20 50)

export nodes=50
export tx_per_node=20
export csv_name="architecture_results"
export per_tx_amount_limit=3000
export lockout_after_consolidation="0"
export client_preventions="0"
export collaberative_security="0"
export intermediary_recovery_rate=5
export intermediary_failure_rate=100
export network_failure_rate=20
export fraud_node_percentage=0

export header="Total Nodes,User Nodes,Barabasi interconnection rate,Average routers per node,Routers,network_recovery_rate,p.intermediary_recovery_rate,p.per_tx_amount_limit,p.lockout_after_consolidation,p.client_preventions,p.collaberative_security,Statistics.online_tx,Statistics.online_tx_volume,Statistics.offline_tx,Statistics.offline_tx_volume,Statistics.fradulent_tx_attempted_sent,Statistics.fradulent_tx_attempted_sent_volume,Statistics.fradulent_tx_sent,Statistics.fradulent_tx_sent_volume,Statistics.fradulent_tx_detected,Statistics.fradulent_tx_detected_volume,Statistics.fradulent_tx_client_online_check,Statistics.fradulent_tx_client_online_check_volume,Statistics.fradulent_tx_client_prevention_prevented,Statistics.fradulent_tx_client_prevention_prevented_volume,Statistics.fradulent_tx_server_lockout_prevented,Statistics.fradulent_tx_server_lockout_prevented_volume,"

echo "$header" > "output/$csv_name.csv"


for recovery_rate in ${router_recovery_rate_range[@]}; do
    for router_per_node in ${AVERAGE_ROUTERS_PER_NODE[@]}; do
        for routers_total in ${ROUTERS_TIER_2[@]}; do
            echo "Running with $router_per_node routers per node and $routers_total total routers recovery rate $recovery_rate"
            export network_recovery_rate=$recovery_rate
            export routers_tier_2=$routers_total
            export average_routers_per_node=$router_per_node
            ../venv/bin/python3 run.py
        done
    done
done
