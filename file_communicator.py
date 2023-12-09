import json
import os

"""
NOTE: DUPLICATE FILES MUST EXIST IN:
    - ./file_communicator.py
    - ./freqtrade_wrapper/user_data/strategies/file_communicator.py
"""


class FileCommunicator:

    # make this absolute file path!!
    COMM_DIR = "/Users/vdyagilev/Code/FreqTradeFileCommunicatorStrategy/freqtrade_wrapper/freqtrade_comm/"
    FILE_PREFIX = COMM_DIR + "freqtrade_"
    DATA_FILE = FILE_PREFIX + "data_{pair}.json"
    COMMUNICATION_FILE = FILE_PREFIX + "communication.json"
    ORDER_FILE = FILE_PREFIX + "order.json"

    def _write_to_file(self, filename, data):
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as file:
            json.dump(data, file)

    def _read_from_file(self, filename):
        # Check if file exists, if not, create it with default data
        if not os.path.exists(filename):
            default_data = {}
            self._write_to_file(filename, default_data)
        with open(filename, 'r') as file:
            return json.load(file)
