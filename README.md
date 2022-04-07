# CBDC-offline-sim

Offline simulation framework for CBDC in a Norwegian context with architecture and node failure.

### Installaltion with pip
`pip install -r requirements.txt`

### Run the simulation
`python Simulate.py`


Features:
* Simulation of graph [x]
* Graph simulates Norway [x]
* Blockchain for transactions [x]
* Logging [x]
    * Online vs offline tx, amount + volume [x]
    * Fradulent transactions success [x]
* Offline scenarioes simulation [x]
    * Intermediary/ network nodes go offline [x]
* Consolidations when network becomes online [x]
* Malicous actors and double spending attacks [x]
* Offline protocol implementation [x]
    * Offline tx amount limit [x]
    * Lockout mechanisms [x]
    * Offline Wallet log of users and counters with check for each tx [x]
    * Collaberative sync of logs [x]
* Dynamic system and network architecture [x]
    * Amount of intermediary nodes [x]
    * Random variation in generation of network [x]
