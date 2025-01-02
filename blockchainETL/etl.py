import requests
import csv
import json
from web3 import Web3
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

class BlockchainETL:
    def __init__(self, chain, rpc_url):
        self.chain = chain.lower()
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))

        if not self.web3.isConnected():
            raise Exception(f"Unable to connect to {self.chain} via {rpc_url}")

    def extract(self, start_block, end_block):
        """Extract blocks and transactions."""
        data = []
        for block_num in range(start_block, end_block + 1):
            block = self.web3.eth.getBlock(block_num, full_transactions=True)
            block_data = {
                "block_number": block.number,
                "block_hash": block.hash.hex(),
                "timestamp": block.timestamp,
                "transactions": []
            }
            for tx in block.transactions:
                tx_data = {
                    "tx_hash": tx.hash.hex(),
                    "from": tx['from'],
                    "to": tx['to'],
                    "value": self.web3.fromWei(tx.value, 'ether'),
                    "gas": tx.gas,
                    "gas_price": self.web3.fromWei(tx.gasPrice, 'gwei'),
                }
                block_data["transactions"].append(tx_data)
            data.append(block_data)
        return data

    def transform(self, data, filters=None):
        """Transform data based on filters."""
        if not filters:
            return data

        filtered_data = []
        for block in data:
            filtered_transactions = []
            for tx in block['transactions']:
                if "value_gt" in filters and tx["value"] <= filters["value_gt"]:
                    continue
                if "from" in filters and tx["from"] != filters["from"]:
                    continue
                if "to" in filters and tx["to"] != filters["to"]:
                    continue
                filtered_transactions.append(tx)

            if filtered_transactions:
                block["transactions"] = filtered_transactions
                filtered_data.append(block)

        return filtered_data

    def load_to_csv(self, data, file_path):
        """Load data into a CSV file."""
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["block_number", "block_hash", "timestamp", "tx_hash", "from", "to", "value", "gas", "gas_price"])
            for block in data:
                for tx in block['transactions']:
                    writer.writerow([
                        block['block_number'],
                        block['block_hash'],
                        block['timestamp'],
                        tx['tx_hash'],
                        tx['from'],
                        tx['to'],
                        tx['value'],
                        tx['gas'],
                        tx['gas_price']
                    ])

    def load_to_postgresql(self, data, connection_string):
        """Load data into a PostgreSQL database."""
        engine = create_engine(connection_string)
        metadata = MetaData()
        transactions_table = Table('transactions', metadata,
            Column('block_number', Integer),
            Column('block_hash', String),
            Column('timestamp', Integer),
            Column('tx_hash', String, primary_key=True),
            Column('from_address', String),
            Column('to_address', String),
            Column('value', String),
            Column('gas', Integer),
            Column('gas_price', String),
        )
        metadata.create_all(engine)

        with engine.connect() as conn:
            for block in data:
                for tx in block['transactions']:
                    conn.execute(transactions_table.insert(), {
                        "block_number": block['block_number'],
                        "block_hash": block['block_hash'],
                        "timestamp": block['timestamp'],
                        "tx_hash": tx['tx_hash'],
                        "from_address": tx['from'],
                        "to_address": tx['to'],
                        "value": tx['value'],
                        "gas": tx['gas'],
                        "gas_price": tx['gas_price'],
                    })

