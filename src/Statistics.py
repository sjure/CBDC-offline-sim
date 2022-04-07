from Config import InputsConfig as p
from modules.Blockchain import BlockChain as bc
from modules.Types import FRAUD_USER, NETWORK, INTERMEDIARY, USER


def str_ljust(data_point: int, spacing=15):
    return str(data_point).ljust(spacing)


class Statistics:
    # TX data
    online_tx = 0
    online_tx_volume = 0
    offline_tx = 0
    offline_tx_volume = 0

    # Fraud tx data
    fradulent_tx_detected = 0
    fradulent_tx_detected_volume = 0
    fradulent_tx_sent = 0
    fradulent_tx_sent_volume = 0
    fradulent_tx_attempted_sent = 0
    fradulent_tx_attempted_sent_volume = 0
    fradulent_tx_client_prevention_prevented = 0
    fradulent_tx_client_prevention_prevented_volume = 0
    fradulent_tx_server_lockout_prevented = 0
    fradulent_tx_server_lockout_prevented_volume = 0
    fradulent_tx_client_online_check = 0
    fradulent_tx_client_online_check_volume = 0

    fraud_users = {}

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

    def print_fradulent_user_balances():
        if (len(Statistics.fraud_users)):
            print("Detected fraudulent user".ljust(40) + "Balance".ljust(40))
            sum = 0
            for user_account in Statistics.fraud_users.keys():
                sum += Statistics.fraud_users[user_account]
                print(str_ljust(user_account, spacing=40) +
                      str_ljust(Statistics.fraud_users[user_account], spacing=40))
            print(str_ljust("Sum", spacing=40) + str_ljust(sum, spacing=40))
        print()

    def print_offline_online():
        per_square = 15
        print("Online".ljust(per_square*2) + "Offline".ljust(per_square*2))
        print("Tx".ljust(per_square) + "Volume".ljust(per_square) +
              "Tx".ljust(per_square) + "Volume".ljust(per_square))
        print(str_ljust(Statistics.online_tx) + str_ljust(Statistics.online_tx_volume) +
              str_ljust(Statistics.offline_tx) + str_ljust(Statistics.offline_tx_volume))
        print()

    def print_fraud():
        per_square = 15
        print("Fraud Attempt".ljust(per_square*2) +
              "Fraud Success".ljust(per_square*2) +
              "Success Fraud Detected".ljust(per_square*2))
        print("Tx".ljust(per_square) + "Volume".ljust(per_square) +
              "Tx".ljust(per_square) + "Volume".ljust(per_square) +
              "Tx".ljust(per_square) + "Volume".ljust(per_square))
        print(str_ljust(Statistics.fradulent_tx_attempted_sent) + str_ljust(Statistics.fradulent_tx_attempted_sent_volume) +
              str_ljust(Statistics.fradulent_tx_sent) + str_ljust(Statistics.fradulent_tx_sent_volume) +
              str_ljust(Statistics.fradulent_tx_detected) + str_ljust(Statistics.fradulent_tx_detected_volume))
        print()
        print("Client Prevention".ljust(per_square*2) +
              "Server Ban list".ljust(per_square*2) +
              "Client online check prevented".ljust(per_square*2))
        print("Tx".ljust(per_square) + "Volume".ljust(per_square) +
              "Tx".ljust(per_square) + "Volume".ljust(per_square) +
              "Tx".ljust(per_square) + "Volume".ljust(per_square))
        print(str_ljust(Statistics.fradulent_tx_client_prevention_prevented) +
              str_ljust(Statistics.fradulent_tx_client_prevention_prevented_volume) +
              str_ljust(Statistics.fradulent_tx_server_lockout_prevented) +
              str_ljust(Statistics.fradulent_tx_server_lockout_prevented_volume) +
              str_ljust(Statistics.fradulent_tx_client_online_check) +
              str_ljust(Statistics.fradulent_tx_client_online_check_volume))
        print()

    def print_money_supply():
        print("".ljust(20) + "Value Before".ljust(20) +
              "Value After ".ljust(20) + "Diff ".ljust(20))
        print("Online".ljust(20) + str_ljust(Statistics.online_money_init) + str_ljust(Statistics.online_money_after) +
              str_ljust(Statistics.online_money_after - Statistics.online_money_init))
        print("Offline".ljust(20) + str_ljust(Statistics.offline_money_init) + str_ljust(Statistics.offline_money_after) +
              str_ljust(Statistics.offline_money_after - Statistics.offline_money_init))
        print("Sum".ljust(20) + str_ljust(Statistics.total_money_before) + str_ljust(Statistics.total_money_after) +
              str_ljust(Statistics.total_money_after - Statistics.total_money_before))
        print()

    def get_sum_of_balances(graph):
        sum_of_online = 0
        sum_of_offline = 0
        for node_id in graph.nodes():
            node = graph.get_node(node_id)
            online_balance = bc.balance_of(node.account_id)
            sum_of_online += online_balance
            if node.type in [USER, FRAUD_USER]:
                offline_bal = bc.balance_of(node.get_offline_address())
                sum_of_offline += offline_bal
        return sum_of_online, sum_of_offline

    def print_fradulent_users(graph):
        print("Node".ljust(5) + "Type".ljust(15) +
              "Offline account id".ljust(25))
        for node_id in graph.nodes():
            node = graph.get_node(node_id)
            if node.type == FRAUD_USER:
                print(str(node.type).ljust(15) +
                      str(node.get_offline_address()).ljust(25))
        print()

    def print_all_balances(graph):
        print("Node".ljust(5) + "Type".ljust(15) +
              "Active balance".ljust(25) + "Offline balance".ljust(15))
        for node_id in graph.nodes():
            node = graph.get_node(node_id)
            online_balance = bc.balance_of(node.account_id)
            if node.type in [USER, FRAUD_USER]:
                offline_bal = bc.balance_of(node.get_offline_address())
                print(str(node_id).ljust(5) + str(node.type).ljust(15) +
                      str(online_balance).ljust(25) + str(offline_bal).ljust(15))
        print()

    def print_state():
        Statistics.print_offline_online()
        Statistics.print_fraud()
        Statistics.print_money_supply()


if __name__ == "__main__":
    Statistics.print_state()
