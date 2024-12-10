<p align="center">
  <img src="./images/lnmarkets-logo.svg" alt="LN Markets" width="200" />
</p>

<h1 align="center">LN Markets Python SDK</h1>

<p align="center">
  <a href="https://lnmarkets.com">
    Website
  </a>
  -
  <a href="https://docs.lnmarkets.com/api/">
    API Reference
  </a>
</p>

## Installation

Install the SDK using pip:

```bash
pip install lnmarkets-sdk
```

or using poetry:

```bash
poetry add lnmarkets-sdk
```

## Usage

The SDK is fully typed so you can use it with your IDE's autocompletion and should be fairly easy to use.

Here is an example of the most simple usage of the SDK.

```python
from datetime import datetime
from lnmarkets import LNMClient

# Import a topic module entirely
from lnmarkets import user
# or a specific function
from lnmarkets.futures import get_trades

# Initialize the client
client = LNMClient(options={
  'network': 'testnet', # 'mainnet' by default, or LNM_API_NETWORK environment variable
  'key': 'api key', # LNMARKETS_API_KEY environment variable by default
  'secret': 'api secret', # LNM_API_SECRET environment variable by default
  'passphrase': 'passphrase', # LNM_API_PASSPHRASE environment variable by default
})

# Use the imported module
user_info = user.get_user(client)

print(user_info['uid'])
print(user_info['username'])

# Use a specific function
trades = get_trades(client, {
  'type': 'open',
  'from_ts': int(datetime.now().timestamp() - 1_000_000),
  'to': int(datetime.now().timestamp()),
  'limit': 100,
})

print(trades)
```

## Function List

| Function | Method | Route | Documentation |
| --- | --- | --- | --- |
| futures.add_margin | POST | /futures/add-margin | [Reference](https://docs.lnmarkets.com/api/operations/futuresaddmargin) |
| futures.cancel_all_trades | DELETE | /futures/all/cancel | [Reference](https://docs.lnmarkets.com/api/operations/futurescancelalltrades) |
| futures.cancel_trade | POST | /futures/cancel | [Reference](https://docs.lnmarkets.com/api/operations/futurescanceltrade) |
| futures.cash_in | POST | /futures/cash-in | [Reference](https://docs.lnmarkets.com/api/operations/futurescashin) |
| futures.close_all_trades | DELETE | /futures/all/close | [Reference](https://docs.lnmarkets.com/api/operations/futuresclosealltrades) |
| futures.close_trade | DELETE | /futures | [Reference](https://docs.lnmarkets.com/api/operations/futuresclosetrade) |
| futures.get_carry_fees_history | GET | /futures/carry-fees | [Reference](https://docs.lnmarkets.com/api/operations/futuresgetcarryfees) |
| futures.get_fixing_history | GET | /futures/history/fixing | [Reference](https://docs.lnmarkets.com/api/operations/futuresgetfixinghistory) |
| futures.get_index_history | GET | /futures/history/index | [Reference](https://docs.lnmarkets.com/api/operations/futuresgetindexhistory) |
| futures.get_leaderboard | GET | /futures/leaderboard | [Reference](https://docs.lnmarkets.com/api/operations/futuresgetleaderboard) |
| futures.get_market_details | GET | /futures/market | [Reference](https://docs.lnmarkets.com/api/operations/futuresgetmarketdetails) |
| futures.get_ohlc_history | GET | /futures/ohlcs | [Reference](https://docs.lnmarkets.com/api/operations/futuresgetohlcs) |
| futures.get_price_history | GET | /futures/history/price | [Reference](https://docs.lnmarkets.com/api/operations/futuresgetpricehistory) |
| futures.get_ticker | GET | /futures/ticker | [Reference](https://docs.lnmarkets.com/api/operations/futuresgetticker) |
| futures.get_trade | GET | /futures/trades/:id | [Reference](https://docs.lnmarkets.com/api/operations/futuresgettrade) |
| futures.get_trades | GET | /futures | [Reference](https://docs.lnmarkets.com/api/operations/futuresgettrades) |
| futures.new_trade | POST | /futures | [Reference](https://docs.lnmarkets.com/api/operations/futuresnewtrade) |
| futures.update_trade | PUT | /futures | [Reference](https://docs.lnmarkets.com/api/operations/futuresupdatetrade) |
| notifications.get_all_notifications | GET | /notifications | [Reference](https://docs.lnmarkets.com/api/operations/notificationsfetchnotifications) |
| notifications.mark_all_as_read | DELETE | /notifications/all | [Reference](https://docs.lnmarkets.com/api/operations/notificationsmarkallnotificationsasread) |
| options.close_all_trades | DELETE | /options/all/close | [Reference](https://docs.lnmarkets.com/api/operations/optionsclosealltrades) |
| options.close_trade | DELETE | /options | [Reference](https://docs.lnmarkets.com/api/operations/optionsclosetrade) |
| options.get_instrument | GET | /options/instrument | [Reference](https://docs.lnmarkets.com/api/operations/optionsgetinstrument) |
| options.get_instruments | GET | /options/instruments | [Reference](https://docs.lnmarkets.com/api/operations/optionsgetinstruments) |
| options.get_market_details | GET | /options | [Reference](https://docs.lnmarkets.com/api/operations/optionsgetoptionsmarket) |
| options.get_trade | GET | /options/trades/:id | [Reference](https://docs.lnmarkets.com/api/operations/optionsgettrade) |
| options.get_trades | GET | /options/trades | [Reference](https://docs.lnmarkets.com/api/operations/optionsgettrades) |
| options.new_trade | POST | /options | [Reference](https://docs.lnmarkets.com/api/operations/optionsnewtrade) |
| options.update_trade | PUT | /options | [Reference](https://docs.lnmarkets.com/api/operations/optionsupdatetrade) |
| oracle.get_last_price | GET | /oracle/last-price | [Reference](https://docs.lnmarkets.com/api/operations/oraclegetlastprice) |
| swaps.get_swap_by_source_id | GET | /swap/source/:sourceId | [Reference](https://docs.lnmarkets.com/api/operations/swapsgetswapbysourceid) |
| swaps.get_swap | GET | /swap/:swapId | [Reference](https://docs.lnmarkets.com/api/operations/swapsgetswap) |
| swaps.get_swaps | GET | /swap | [Reference](https://docs.lnmarkets.com/api/operations/swapsgetswaps) |
| swaps.new_swap | POST | /swap | [Reference](https://docs.lnmarkets.com/api/operations/swapsnewswap) |
| user.deposit_synthetic_usd | POST | /user/deposit/susd | [Reference](https://docs.lnmarkets.com/api/operations/userdepositsyntheticusd) |
| user.deposit | POST | /user/deposit | [Reference](https://docs.lnmarkets.com/api/operations/userdeposit) |
| user.get_bitcoin_addresses | GET | /user/bitcoin/addresses | [Reference](https://docs.lnmarkets.com/api/operations/usergetbitcoinaddresses) |
| user.get_deposit | GET | /user/deposit/:depositId | [Reference](https://docs.lnmarkets.com/api/operations/usergetdeposit) |
| user.get_deposits | GET | /user/deposit | [Reference](https://docs.lnmarkets.com/api/operations/usergetdeposits) |
| user.get_user | GET | /user | [Reference](https://docs.lnmarkets.com/api/operations/usergetuser) |
| user.get_withdrawal | GET | /user/withdrawals/:id | [Reference](https://docs.lnmarkets.com/api/operations/usergetwithdrawal) |
| user.get_withdrawals | GET | /user/withdraw | [Reference](https://docs.lnmarkets.com/api/operations/usergetwithdrawals) |
| user.new_bitcoin_address | POST | /user/bitcoin/address | [Reference](https://docs.lnmarkets.com/api/operations/usernewbitcoinaddress) |
| user.transfer | POST | /user/transfer | [Reference](https://docs.lnmarkets.com/api/operations/usertransfer) |
| user.update_user | PUT | /user | [Reference](https://docs.lnmarkets.com/api/operations/userupdate) |
| user.withdraw_synthetic_usd | POST | /user/withdraw/susd | [Reference](https://docs.lnmarkets.com/api/operations/userwithdrawalsyntheticusd) |
| user.withdraw | POST | /user/withdraw | [Reference](https://docs.lnmarkets.com/api/operations/userwithdraw) |

## Development

### Prerequisites

- Python 3.11 or higher
- Poetry

### Steps

1 - Clone the repository:

```bash
git clone https://github.com/lnmarkets/python-sdk.git
```

2 - Install the dependencies:

```bash
poetry install
```

3 - Have fun!
