import pandas as pd
from freqtrade_handler import FreqtradeHandler


class CryptoHandler:
    def __init__(self, stake_currency: str,  freqtrade_handler: FreqtradeHandler):
        """
        Initialize the CryptoHandler.

        :param stake_currency: The currency used for staking (e.g. 'USDT').
        :param all_trading_pairs: All available trading pairs.
        :param freqtrade_handler: An instance of the FreqtradeHandler.
        """
        self.stake_currency = stake_currency
        self.freqtrade_handler = freqtrade_handler
        self.bought_crypto = None
        # init in start_session
        self.crypto_pairs = None

    def start_session(self, crypto_pairs: list[str],):
        self.crypto_pairs = crypto_pairs
        # Signal Freqtrade to write data for these sampled cryptos
        self.freqtrade_handler.write_data_request(self.crypto_pairs)

    def reset_session(self):
        # reset freqtradehandler and its communication messages
        self.freqtrade_handler.reset_files()

    def _calculate_growth(self, data):
        """
        Calculate growth rate for a given crypto data.

        :param data: Dictionary containing start_price, end_price, and growth.
        :return: Growth rate for the crypto.
        """
        if not data or 'growth' not in data:
            print("_calculate_growth: Insufficient data!")
            return 0  # Return 0 for insufficient data

        return data['growth']

    def get_latest_data(self):
        """
        Fetch the latest data for the trading pairs.

        :return: Dictionary with trading pairs as keys.
        """
        data_dict = {}
        for pair in self.crypto_pairs:
            data = self.freqtrade_handler.read_data(pair)
            if not data or 'growth' not in data:
                print(f"Missing data for pair: {pair}")
            data_dict[pair] = data
        return data_dict

    def get_top_performing_crypto(self):
        """
        Identify the top-performing crypto based on recent growth.

        :return: Tuple of top-performing crypto symbol and its growth rate.
        """
        dataframes = self.get_latest_data()
        growth_rates = {pair: self._calculate_growth(
            df) for pair, df in dataframes.items()}
        top_crypto = max(growth_rates, key=growth_rates.get)
        return top_crypto, growth_rates[top_crypto]

    def place_buy_order(self, crypto_symbol, amount):
        """
        Buy the specified crypto based on growth.

        :param crypto_symbol: The symbol of the cryptocurrency to buy.
        :param amount: Amount of crypto to purchase
        :return: The symbol of the bought crypto.
        """
        self.freqtrade_handler.place_order('buy', crypto_symbol, amount)
        self.bought_crypto = crypto_symbol
        return crypto_symbol

    def place_sell_order(self, crypto_symbol, amount):
        """
        Sell the specified crypto. Does nothing if no crypto was specified.

        :param crypto_symbol: The symbol of the cryptocurrency to sell.
        :param amount: Amount of crypto to purchase
        """
        if crypto_symbol:
            self.freqtrade_handler.place_order(
                'sell', crypto_symbol, amount)
            if self.bought_crypto == crypto_symbol:
                self.bought_crypto = None  # Reset after selling
