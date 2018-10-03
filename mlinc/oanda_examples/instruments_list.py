import oandapyV20
import oandapyV20.endpoints.accounts as accounts
from mlinc.oanda_examples.exampleauth import exampleAuth


def instrument_list():
    """
    Function to retrieve all tradable instruments from Oanda.

    Returns List with instrument codes
    -------
    """

    instr_list = []
    accountID, token = exampleAuth()
    client = oandapyV20.API(access_token=token)
    r = accounts.AccountInstruments(accountID=accountID)
    rv = client.request(r)

    # instr_dict = json.dumps(rv, indent=2)

    for i in range(len(rv['instruments'])):
        instr_list.append(rv['instruments'][i]['name'])

    return instr_list


def custom_list():
    """"
    This function contains a list based on low spreads and low(er) risk coupling
    e.g. XAU_EUR and XAU_USD -> XAU_EUR removed
    """
    custom_inst = ['EUR_USD',
                   'GBP_USD',
                   'USD_CAD',
                   'USD_CHF',
                   'USD_JPY',
                   'AUD_NZD',
                   'AUD_USD',
                   'CAD_CHF',
                   'CHF_HKD',
                   'USD_CNH',
                   'USD_CZK',
                   'USD_DKK',
                   'USD_HKD',
                   'AU200_AUD',
                   'AUD_CHF',
                   'AUD_SGD',
                   'BCO_USD',
                   'CAD_SGD',
                   'CHF_JPY',
                   'CHF_ZAR',
                   'DE10YB_EUR',
                   'DE30_EUR',
                   'EU50_EUR',
                   'EUR_AUD',
                   'EUR_CAD',
                   'EUR_CHF',
                   'EUR_CZK',
                   'EUR_DKK',
                   'EUR_GBP',
                   'EUR_HUF',
                   'EUR_JPY',
                   'EUR_NOK',
                   'EUR_PLN',
                   'EUR_SEK',
                   'EUR_SGD',
                   'EUR_ZAR',
                   'FR40_EUR',
                   'GBP_AUD',
                   'GBP_CAD',
                   'GBP_CHF',
                   'GBP_HKD',
                   'GBP_JPY',
                   'GBP_NZD',
                   'GBP_PLN',
                   'GBP_SGD',
                   'HK33_HKD',
                   'HKD_JPY',
                   'IN50_USD',
                   'JP225_USD',
                   'NAS100_USD',
                   'NL25_EUR',
                   'NZD_CAD',
                   'NZD_CHF',
                   'NZD_HKD',
                   'NZD_JPY',
                   'NZD_SGD',
                   'NZD_USD',
                   'SG30_SGD',
                   'SGD_CHF',
                   'SGD_HKD',
                   'SGD_JPY',
                   'SPX500_USD',
                   'UK100_GBP',
                   'UK10YB_GBP',
                   'US2000_USD',
                   'USB10Y_USD',
                   'USD_HUF',
                   'USD_MXN',
                   'USD_NOK',
                   'USD_PLN',
                   'USD_SAR',
                   'USD_SEK',
                   'USD_SGD',
                   'USD_ZAR',
                   'XAU_USD',
                   'XCU_USD',
                   ]

    return custom_inst


print(instrument_list())
print(custom_list())

