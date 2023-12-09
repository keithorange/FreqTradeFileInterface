import json
import os


from file_communicator import FileCommunicator


class FreqtradeHandler(FileCommunicator):

    def __init__(self):
        # Ensure files are in default states
        self.reset_files()

    def reset_files(self):
        """
        Reset all files to their default states.
        """
        self._write_to_file(self.COMMUNICATION_FILE, {
                            "action": None, "crypto_list": []})
        self._write_to_file(
            self.ORDER_FILE, {"action": None, "symbol": None, "amount": None})

    def write_data_request(self, crypto_list):
        """
        Signal the strategy to write data to file.
        """
        data = {
            "action": "write_data",
            "crypto_list": crypto_list,
        }
        self._write_to_file(self.COMMUNICATION_FILE, data)

    def read_data(self, pair):
        """
        Read the data written by the strategy for a given pair.
        """
        formatted_file = self.DATA_FILE.format(pair=pair.replace("/", "-"))
        return self._read_from_file(formatted_file)

    def place_order(self, action, symbol, amount):
        """
        Signal the strategy to place an order.
        """
        self._write_to_file(
            self.ORDER_FILE, {"action": action, "symbol": symbol, "amount": amount})

    def read_order(self):
        """
        Read the order signal.
        """
        return self._read_from_file(self.ORDER_FILE)
