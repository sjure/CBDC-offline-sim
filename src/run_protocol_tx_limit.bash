random_seed_list=(1 2 3)
case_number=(0 1 2 3)
per_tx_amount_limit_range=(10 100 1000 5000 7500 10000 12500 15000 17500 20000)
intermediary_recovery_rate_range=(20)

export csv_name="protocol_results_per_tx_amount_limit"
export nodes=50
export tx_per_node=50
export routers_tier_2=2
export average_routers_per_node=1.5
export intermediary_failure_rate=4
export network_failure_rate=10
export network_recovery_rate=5
export fraud_node_percentage=0.1

export header="Seed,Total Nodes,User Nodes,Barabasi interconnection rate,Average routers per node,Routers,network_recovery_rate,p.intermediary_recovery_rate,p.per_tx_amount_limit,p.lockout_after_consolidation,p.client_preventions,p.collaberative_security,Statistics.online_tx,Statistics.online_tx_volume,Statistics.offline_tx,Statistics.offline_tx_volume,Statistics.fradulent_tx_attempted_sent,Statistics.fradulent_tx_attempted_sent_volume,Statistics.fradulent_tx_sent,Statistics.fradulent_tx_sent_volume,Statistics.fradulent_tx_detected,Statistics.fradulent_tx_detected_volume,Statistics.fradulent_tx_client_online_check,Statistics.fradulent_tx_client_online_check_volume,Statistics.fradulent_tx_client_prevention_prevented,Statistics.fradulent_tx_client_prevention_prevented_volume,Statistics.fradulent_tx_server_lockout_prevented,Statistics.fradulent_tx_server_lockout_prevented_volume,"
echo "$header" > "output/$csv_name.csv"

for seed in ${random_seed_list[@]}; do
    for tx_limit in ${per_tx_amount_limit_range[@]}; do
        for recovery_rate in ${intermediary_recovery_rate_range[@]}; do
            for cn in ${case_number[@]}; do
                echo "New run with parameters: tx_limit ${tx_limit}, recovery_rate ${recovery_rate}, CASE=$cn, seed=$seed" >> proto_run_log.txt
                echo "New run with parameters: tx_limit ${tx_limit}, recovery_rate ${recovery_rate}, CASE=$cn, seed=$seed"
                export lockout_after_consolidation="0"
                export client_preventions="0"
                export collaberative_security="0"
                if [ $cn -eq 1 ]; then
                    export lockout_after_consolidation="1"
                elif [ $cn -eq 2 ]; then
                    export client_preventions="1"
                elif [ $cn -eq 3 ]; then
                    export client_preventions="1"
                    export collaberative_security="1"
                fi
		export random_seed=$seed
                export per_tx_amount_limit=$tx_limit
                export intermediary_recovery_rate=$recovery_rate
                ../venv/bin/python3 run.py >> proto_log.txt
            done
        done
    done
done
