import logging
from numpy import random
from modules.Types import NETWORK, INTERMEDIARY, USER
from Config import InputsConfig as p
from modules.Blockchain import BlockChain as bc
from EventOrganizer import EventOrganizer as eo
from Statistics import Statistics
from modules.BarabasiAlbert import BarabasiAlbert


LOGGING_FORMAT = "%(asctime)s: %(message)s"
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO,datefmt="%H:%M:%S")

graphs = {
    "ba": BarabasiAlbert,
}

class Simulate:
    """ Simulation class """

    graph = graphs[p.graph_type](**p.graph_params)

    def run():
        Simulate.add_init_balance(p.balance["mean"], p.balance["std"])
        Statistics.print_all_balances(Simulate.graph)
        eo.generate_events(Simulate.graph)
        print("events", eo.event_queue.qsize())
        eo.event_organizer()
        print("All blocks authentic", bc.verify_block_chain())
        Statistics.print_all_balances(Simulate.graph)
        Statistics.print_state()

    def add_init_balance(mean,std):
        for node in Simulate.graph.nodes():
            nodeData = Simulate.graph.get_node(node)
            if (nodeData.type in [NETWORK,INTERMEDIARY]):
                continue
            wallet_id = nodeData.account_id
            wallet_amount = random.normal(mean,std)
            if (wallet_amount < 0):
                wallet_amount = 0
            bc.deposit_money(wallet_id, wallet_amount)


if __name__ == "__main__":
    Simulate.run()
