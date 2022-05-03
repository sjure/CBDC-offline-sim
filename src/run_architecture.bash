AVERAGE_ROUTERS_PER_NODE=(1 1.5 2 3 4 5 6 7 8 9 10)
random_seed_list=(1 2 3 42 5 6 7 8 9 10)


export nodes=50
export tx_per_node=200
export csv_name="architecture_results"
export per_tx_amount_limit=3000
export lockout_after_consolidation="0"
export client_preventions="0"
export collaberative_security="0"
export intermediary_recovery_rate=5
export intermediary_failure_rate=100
export network_failure_rate=20
export fraud_node_percentage=0
export routers_tier_2=10
export network_recovery_rate=10

export header="Seed,Total Nodes,User Nodes,Barabasi interconnection rate,Average routers per node,Routers,network_recovery_rate,p.intermediary_recovery_rate,p.per_tx_amount_limit,p.lockout_after_consolidation,p.client_preventions,p.collaberative_security,Statistics.online_tx,Statistics.online_tx_volume,Statistics.offline_tx,Statistics.offline_tx_volume,Statistics.fradulent_tx_attempted_sent,Statistics.fradulent_tx_attempted_sent_volume,Statistics.fradulent_tx_sent,Statistics.fradulent_tx_sent_volume,Statistics.fradulent_tx_detected,Statistics.fradulent_tx_detected_volume,Statistics.fradulent_tx_client_online_check,Statistics.fradulent_tx_client_online_check_volume,Statistics.fradulent_tx_client_prevention_prevented,Statistics.fradulent_tx_client_prevention_prevented_volume,Statistics.fradulent_tx_server_lockout_prevented,Statistics.fradulent_tx_server_lockout_prevented_volume,"

echo "$header" > "output/$csv_name.csv"

for seed in ${random_seed_list[@]}; do
    for router_per_node in ${AVERAGE_ROUTERS_PER_NODE[@]}; do
        echo "Running with $router_per_node routers per node and total routers seed rate $seed"
        export random_seed=$seed
        export average_routers_per_node=$router_per_node
        ../venv/bin/python3 run.py
    done
done
