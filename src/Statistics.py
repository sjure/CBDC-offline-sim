from Config import InputsConfig as p
from modules.Blockchain import BlockChain as bc
from modules.Types import NETWORK, INTERMEDIARY, USER


def str_ljust(data_point :int,spacing = 20):
    return str(data_point).ljust(spacing)

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
    network_repairs = 0
    intermediary_failures = 0
    intermediary_repairs = 0

    # Money Supply
    online_money_init = 0
    online_money_after = 0
    offline_money_init = 0
    offline_money_after = 0
    total_money_before = 0
    total_money_after = 0

    def print_offline_online():
        print("Online".ljust(40) + "Offline".ljust(40))
        print("Tx".ljust(20) + "Volume".ljust(20) + "Tx".ljust(20) + "Volume".ljust(20))
        print(str_ljust(Statistics.online_tx) + str_ljust(Statistics.online_tx_volume) + 
            str_ljust(Statistics.offline_tx) + str_ljust(Statistics.offline_tx_volume))

    def print_fraud():
        print("Fraud Success".ljust(40) + "Fraud Failure".ljust(40))
        print("Tx".ljust(20) + "Volume".ljust(20) + "Tx".ljust(20) + "Volume".ljust(20))
        print(str_ljust(Statistics.fradulent_tx_successes) + str_ljust(Statistics.fradulent_tx_success_volume) + 
            str_ljust(Statistics.fradulent_tx_failures) + str_ljust(Statistics.fradulent_tx_failures_volume))


    def print_money_supply():
        print("".ljust(20) + "Value Before".ljust(10) + "Value After ".ljust(10))
        print("Online".ljust(20) + str_ljust(Statistics.online_money_init,spacing=10) + str_ljust(Statistics.online_money_after,spacing=10))
        print("Offline".ljust(20) + str_ljust(Statistics.offline_money_init,spacing=10) + str_ljust(Statistics.offline_money_after,spacing=10))
        print("Sum".ljust(20) + str_ljust(Statistics.total_money_before,spacing=10) + str_ljust(Statistics.total_money_after,spacing=10))

    def print_all_balances(graph):
        sum_of_balances = 0
        sum_of_offline = 0
        print("Node".ljust(5) + "Active balance".ljust(25) + "Offline balance".ljust(15))
        for node_id in graph.nodes():
            node = graph.get_node(node_id)
            online_balance = bc.balance_of(node.account_id)
            sum_of_balances += online_balance
            if node.type == USER:
                offline_bal = bc.balance_of(node.get_offline_address())
                sum_of_offline += offline_bal
                print(str(node_id).ljust(5) + str(online_balance).ljust(25) + str(offline_bal).ljust(15))

    def print_state():
        Statistics.print_offline_online()
        print()
        Statistics.print_fraud()
        print()
        Statistics.print_money_supply()


if __name__ == "__main__":
    Statistics.print_state()