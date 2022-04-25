lockout_after_consolidation_range=(0 1)
client_preventions_range=(0 1)
collaberative_security_range=(0 1)
per_tx_amount_limit_range=(500 1000 2000 5000 10000 20000 50000 100000 200000 500000 1000000)
intermediary_recovery_rate_range=(1 5 10 20 40 50)

export csv_name="protocol_results"
export routers_tier_2=15
export average_routers_per_node=2

for recovery_rate in ${intermediary_recovery_rate_range[@]}; do
    for tx_limit in ${per_tx_amount_limit_range[@]}; do
        for cs in ${collaberative_security_range[@]}; do
            for cp in ${client_preventions_range[@]}; do
                for lc in ${lockout_after_consolidation_range[@]}; do
                    echo "New run with parameters: recovery_rate ${recovery_rate}, tx_limit ${tx_limit}, cs ${cs}, cp ${cp}, lc ${lc}" >> proto_run_log.txt
                    echo "New run with parameters: recovery_rate ${recovery_rate}, tx_limit ${tx_limit}, cs ${cs}, cp ${cp}, lc ${lc}"
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
