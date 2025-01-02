
from blockchainETL.etl import BlockchainETL


def test_connection():
    url = 'https://eth-mainnet.g.alchemy.com/v2/oY_DEIcIgmoHz6sN1dFBCXGDUdgIltnb'
    etl = BlockchainETL(chain="ethereum", rpc_url=url)
    assert etl.web3.isConnected()
    print(etl.web3.isConnected())





#   rpc_url = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
#     etl = BlockchainETL(chain="ethereum", rpc_url=rpc_url)

#     # Extract data
#     raw_data = etl.extract(start_block=17000000, end_block=17000002)

#     # Transform data
#     filtered_data = etl.transform(raw_data, filters={"value_gt": 0.1})

#     # Load data to CSV
#     etl.load_to_csv(filtered_data, "blockchain_data.csv")

#     # Load data to PostgreSQL
#     connection_string = "postgresql://username:password@localhost:5432/blockchain"
#     etl.load_to_postgresql(filtered_data, connection_string)