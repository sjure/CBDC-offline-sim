from Config import InputsConfig as p
from modules.network.NorGraph import NorGraph
from modules.network.MeshGraph import MeshGraph
from modules.network.BarabasiAlbert import BarabasiAlbert
from Statistics import Statistics
from EventOrganizer import EventOrganizer as eo
from modules.Blockchain import BlockChain as bc
import os
import logging
from numpy import random
from modules.Types import NETWORK, INTERMEDIARY, USER

filename = os.environ.get('csv_name', "test")
LOGGING_FORMAT = "%(asctime)s.%(msecs)03d %(message)s"
logging.basicConfig(filename=f"{filename}.log", format=LOGGING_FORMAT,
                    level=logging.INFO, datefmt="%H:%M:%S", filemode='w',)

random.seed(p.random_seed)

logger = logging.getLogger("CBDCSimLog")

graphs = {
    "ba": BarabasiAlbert,
    "no": NorGraph,
    "mesh": MeshGraph
}


class Simulate:
    """ Simulation class """

    graph = graphs[p.graph_type](**p.graph_params, random=p.random_seed)

    def run():
        Simulate.graph = graphs[p.graph_type](
            **p.graph_params, random=p.random_seed)
        print(p.graph_type, p.graph_params, len(Simulate.graph.nodes()))
        print("tx_per_node", p.tx_per_node,
              "\nper_tx_amount_limit", p.per_tx_amount_limit)
        print("lockout_after_consolidation", p.lockout_after_consolidation,
              "\nclient_preventions", p.client_preventions,
              "\ncollaberative_security", p.collaberative_security)
        logger.info("============= New run ===============")
        Simulate.add_init_balance(p.balance["mean"], p.balance["std"])
        logger.info("============= Init balances added  ===============")
        # Statistics.print_fradulent_users(Simulate.graph)
        # Statistics.print_all_balances(Simulate.graph)
        eo.generate_events(Simulate.graph)
        logger.info("============= Events Generated ===============")
        logger.info(f"Amount of events = {eo.event_queue.qsize()}")
        eo.event_organizer()
        Simulate.cleanup()
        logger.info(bc.blocks)
        # Statistics.print_all_balances(Simulate.graph)
        # Statistics.print_fradulent_user_balances()
        # Statistics.print_fradulent_users_sent_bal(Simulate.graph)
        Statistics.print_state()
        logger.info("============= Run End ===============")

    def add_init_balance(mean, std):
        for node in Simulate.graph.nodes():
            nodeData = Simulate.graph.get_node(node)
            logger.info(nodeData)
            if (nodeData.type in [NETWORK, INTERMEDIARY]):
                continue
            wallet_id = nodeData.account_id
            wallet_amount = int(random.normal(mean, std))
            if (wallet_amount < 0):
                wallet_amount = 0
            bc.deposit_money(wallet_id, wallet_amount)
        online_balance, offline_balance = Statistics.get_sum_of_balances(
            Simulate.graph)
        Statistics.online_money_init = online_balance
        Statistics.offline_money_init = offline_balance
        Statistics.total_money_before = online_balance + offline_balance

    def log_results():
        results = [
            len(Simulate.graph.nodes()),
            p.graph_params["n"],
            p.graph_params["m"],
            p.average_routers_per_node,
            p.routers_tier_2,
            p.network_recovery_rate,
            p.intermediary_recovery_rate,
            p.per_tx_amount_limit,
            p.lockout_after_consolidation,
            p.client_preventions,
            p.collaberative_security,
            Statistics.online_tx,
            Statistics.online_tx_volume,
            Statistics.offline_tx,
            Statistics.offline_tx_volume,
            Statistics.fradulent_tx_attempted_sent,
            Statistics.fradulent_tx_attempted_sent_volume,
            Statistics.fradulent_tx_sent,
            Statistics.fradulent_tx_sent_volume,
            Statistics.fradulent_tx_detected,
            Statistics.fradulent_tx_detected_volume,
            Statistics.fradulent_tx_client_online_check,
            Statistics.fradulent_tx_client_online_check_volume,
            Statistics.fradulent_tx_client_prevention_prevented,
            Statistics.fradulent_tx_client_prevention_prevented_volume,
            Statistics.fradulent_tx_server_lockout_prevented,
            Statistics.fradulent_tx_server_lockout_prevented_volume,
        ]
        header = """
Total Nodes,
User Nodes,
Barabasi interconnection rate,
Average routers per node,
Routers,
network_recovery_rate,
p.intermediary_recovery_rate,
p.per_tx_amount_limit,
p.lockout_after_consolidation,
p.client_preventions,
p.collaberative_security,
Statistics.online_tx,
Statistics.online_tx_volume,
Statistics.offline_tx,
Statistics.offline_tx_volume,
Statistics.fradulent_tx_attempted_sent,
Statistics.fradulent_tx_attempted_sent_volume,
Statistics.fradulent_tx_sent,
Statistics.fradulent_tx_sent_volume,
Statistics.fradulent_tx_detected,
Statistics.fradulent_tx_detected_volume,
Statistics.fradulent_tx_client_online_check,
Statistics.fradulent_tx_client_online_check_volume,
Statistics.fradulent_tx_client_prevention_prevented,
Statistics.fradulent_tx_client_prevention_prevented_volume,
Statistics.fradulent_tx_server_lockout_prevented,
Statistics.fradulent_tx_server_lockout_prevented_volume,
            """
        result_csv = ", ".join([str(i) for i in results]) + "\n"
        filename = os.environ.get('csv_name', "results")
        with open("output/" + filename + ".csv", "a") as f:
            f.write(result_csv)

    def cleanup():
        online_balance, offline_balance = Statistics.get_sum_of_balances(
            Simulate.graph)
        Statistics.online_money_after = online_balance
        Statistics.offline_money_after = offline_balance
        Statistics.total_money_after = online_balance + offline_balance
        logger.info(f"All blocks authentic {bc.verify_block_chain()}")


if __name__ == "__main__":
    Simulate.run()
