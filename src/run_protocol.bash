lockout_after_consolidation_range=(0 1)
client_preventions_range=(0 1)
collaberative_security_range=(0 1)
per_tx_amount_limit_range=(4000)
intermediary_recovery_rate_range=(5 10 20 40 100)

export csv_name="protocol_results"
export nodes=50
export tx_per_node=20
export routers_tier_2=2
export average_routers_per_node=1.5
export intermediary_failure_rate=4
export network_failure_rate=10
export network_recovery_rate=5
export fraud_node_percentage=0.1
export random_seed=42

export header="Seed,Total Nodes,User Nodes,Barabasi interconnection rate,Average routers per node,Routers,network_recovery_rate,p.intermediary_recovery_rate,p.per_tx_amount_limit,p.lockout_after_consolidation,p.client_preventions,p.collaberative_security,Statistics.online_tx,Statistics.online_tx_volume,Statistics.offline_tx,Statistics.offline_tx_volume,Statistics.fradulent_tx_attempted_sent,Statistics.fradulent_tx_attempted_sent_volume,Statistics.fradulent_tx_sent,Statistics.fradulent_tx_sent_volume,Statistics.fradulent_tx_detected,Statistics.fradulent_tx_detected_volume,Statistics.fradulent_tx_client_online_check,Statistics.fradulent_tx_client_online_check_volume,Statistics.fradulent_tx_client_prevention_prevented,Statistics.fradulent_tx_client_prevention_prevented_volume,Statistics.fradulent_tx_server_lockout_prevented,Statistics.fradulent_tx_server_lockout_prevented_volume,"
echo "$header" > "output/$csv_name.csv"
echo "" > proto_run_log.txt
echo "" > proto_log.txt

for tx_limit in ${per_tx_amount_limit_range[@]}; do
    for recovery_rate in ${intermediary_recovery_rate_range[@]}; do
        for cs in ${collaberative_security_range[@]}; do
            for cp in ${client_preventions_range[@]}; do
                for lc in ${lockout_after_consolidation_range[@]}; do
                    echo "New run with parameters: tx_limit ${tx_limit}, recovery_rate ${recovery_rate}, cs ${cs}, cp ${cp}, lc ${lc}" >> proto_run_log.txt
                    echo "New run with parameters: tx_limit ${tx_limit}, recovery_rate ${recovery_rate}, cs ${cs}, cp ${cp}, lc ${lc}"
                    export lockout_after_consolidation=$lc
                    export client_preventions=$cp
                    export collaberative_security=$cs
                    export per_tx_amount_limit=$tx_limit
                    export intermediary_recovery_rate=$recovery_rate
                    ../venv/bin/python3 run.py >> proto_log.txt
                done
            done
        done
    done
done
