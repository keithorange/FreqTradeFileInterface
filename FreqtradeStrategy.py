from freqtrade.strategy import IStrategy
import pandas as pd
import json
import os

# duplicate import
from file_communicator import FileCommunicator


class CustomFreqtradeStrategy(IStrategy, FileCommunicator):
    """
    FreqTrade Strategy linked with ARVTrading. It does two things:
        - Write price data for selected cryptos to file
        - Make orders (buy, sell) when told in file
    """
    startup_candle_count = 1  # requires no candles since it only writes current price

    # Define the minimal ROI for the strategy
    minimal_roi = {
        "0": 1
    }
    start_prices = {}  # Dict to keep track of starting prices

    trading_cryptos_list = []
    # Method to populate indicators. This is also utilized to write required data to a file

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        # First, load the user-specified crypto_symbols from file into cache
        communication_data = self._read_from_file(self.COMMUNICATION_FILE)
        # the symbols we're considering out of all available
        self.trading_cryptos_list = communication_data["crypto_list"]

        current_symbol = metadata["pair"]

        print(current_symbol, self.trading_cryptos_list)

        if current_symbol in self.trading_cryptos_list:

            # If this is the first time we are seeing this symbol in the session, store its starting price
            if current_symbol not in self.start_prices:
                self.start_prices[current_symbol] = dataframe.iloc[0]['open']

            # Calculate the growth from start price to current price
            current_price = dataframe.iloc[-1]['close']
            growth = (
                current_price - self.start_prices[current_symbol]) / self.start_prices[current_symbol]

            # Prepare data to be saved
            data_to_save = {
                'start_price': self.start_prices[current_symbol],
                'end_price': current_price,
                'growth': growth
            }

            # Save the data
            self._write_to_file(self.DATA_FILE.format(
                pair=current_symbol.replace("/", "-")), data_to_save)

        return dataframe

    # Method to generate buy signals

    # Method to generate buy signals

    def populate_buy_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        current_symbol = metadata["pair"]
        # Initially set no buy signals
        dataframe['enter_long'] = 0
        if current_symbol in self.trading_cryptos_list:

            # Check the order file to see if a buy order is signaled
            order_data = self._read_from_file(self.ORDER_FILE)

            # If buy action is required for the current pair, set the buy signal
            if order_data['action'] == 'buy' and order_data['symbol'] == metadata["pair"]:
                dataframe.loc[dataframe.index[-1], 'enter_long'] = 1
                # Reset the action in the order file to prevent repetitive orders
                order_data['action'] = None
                self._write_to_file(self.ORDER_FILE, order_data)

        return dataframe

    # Method to generate sell signals

    def populate_sell_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        current_symbol = metadata["pair"]
        # Initially set no sell signals
        dataframe['exit_long'] = 0
        if current_symbol in self.trading_cryptos_list:

            # Check the order file to see if a sell order is signaled
            order_data = self._read_from_file(self.ORDER_FILE)

            # If sell action is required for the current pair, set the sell signal
            if order_data['action'] == 'sell' and order_data['symbol'] == metadata["pair"]:
                dataframe.loc[dataframe.index[-1], 'exit_long'] = 1
                # Reset the action in the order file to prevent repetitive orders
                order_data['action'] = None
                self._write_to_file(self.ORDER_FILE, order_data)

        return dataframe
