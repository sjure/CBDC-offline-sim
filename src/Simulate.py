import logging
import json
from numpy import random
from modules.Types import NETWORK, INTERMEDIARY, USER
from Config import InputsConfig as p
from modules.Blockchain import BlockChain as bc
from EventOrganizer import EventOrganizer as eo
from Statistics import Statistics
from modules.BarabasiAlbert import BarabasiAlbert

LOGGING_FORMAT = "%(asctime)s.%(msecs)03d %(message)s"
logging.basicConfig(filename="log.log",format=LOGGING_FORMAT, level=logging.INFO,datefmt="%H:%M:%S")

logger = logging.getLogger("CBDCSimLog")

graphs = {
    "ba": BarabasiAlbert,
}

class Simulate:
    """ Simulation class """

    graph = graphs[p.graph_type](**p.graph_params)

    def run():
        logger.info("============= New run ===============")
        Simulate.add_init_balance(p.balance["mean"], p.balance["std"])
        logger.info("============= Init balances added  ===============")
        Statistics.print_all_balances(Simulate.graph)
        eo.generate_events(Simulate.graph)
        logger.info("============= Events Generated ===============")
        logger.info(f"Amount of events = {eo.event_queue.qsize()}")
        eo.event_organizer()
        Simulate.cleanup()
        logger.info(bc.blocks)
        Statistics.print_all_balances(Simulate.graph)
        Statistics.print_state()
        logger.info("============= Run End ===============")


    def add_init_balance(mean,std):
        for node in Simulate.graph.nodes():
            nodeData = Simulate.graph.get_node(node)
            logger.info(nodeData)
            if (nodeData.type in [NETWORK,INTERMEDIARY]):
                continue
            wallet_id = nodeData.account_id
            wallet_amount = int(random.normal(mean,std))
            if (wallet_amount < 0):
                wallet_amount = 0
            bc.deposit_money(wallet_id, wallet_amount)
        online_balance, offline_balance = Statistics.get_sum_of_balances(Simulate.graph)
        Statistics.online_money_init = online_balance
        Statistics.offline_money_init = offline_balance
        Statistics.total_money_before = online_balance + offline_balance
    
    def cleanup():
        online_balance, offline_balance = Statistics.get_sum_of_balances(Simulate.graph)
        Statistics.online_money_after = online_balance
        Statistics.offline_money_after = offline_balance
        Statistics.total_money_after = online_balance + offline_balance
        logger.info(f"All blocks authentic {bc.verify_block_chain()}")


if __name__ == "__main__":
    Simulate.run()
