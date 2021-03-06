"""
Views that define API endpoints for the site
"""
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import JsonResponse, HttpResponse

from dual_momentum.ticker_config import TICKER_CONFIG
import time
import json

from dual_momentum.dm_composite import DualMomentumComposite

from IPython import embed

def get_test_data(request):

    ticker_suggestions = {}
    for ticker, config in TICKER_CONFIG.items():
        if config['suggest_in_search']:
            ticker_suggestions[config['name']] = ticker

    start = time.time()


    config = json.loads(request.GET['conf'])['dm_config']
    components = json.loads(request.GET['conf'])['dm_components']

    if config['simulate_taxes']:
        tax_config = config['tax_rates']
        for key, val in tax_config.items():
            tax_config[key] = val / 100

    else:
        tax_config = {'fed_st_gains': 0.0, 'fed_lt_gains': 0.0, 'state_st_gains': 0.0,
                      'state_lt_gains': 0.0}

    parts = []
    for component in components:
        if component == {'name': ''}:
            continue
        component['ticker_list'] = [holding for holding in component['holdings'] if holding != '']
        component['lookback_months'] = component['lookback']
        component['use_dual_momentum'] = component['dual_momentum']
        if not component['use_dual_momentum']:
            component['ticker_list'] = [component['ticker_list'][0]]
        parts.append(component)

    try:
        dm = DualMomentumComposite(parts=parts,
                               money_market_holding=config['money_market_holding'],
                               momentum_leverages=config['momentum_leverages'],
                               tax_config=tax_config,
                               start_date=f'{config["start_year"]}-01-01',
                               leverage=config['leverage'],
                               borrowing_cost_above_libor=config['borrowing_costs_above_libor'])

        dm.run_multi_component_dual_momentum()
        dm.generate_results_summary()

        config_hash = dm.__hash__()
        data = dm.summary
        error = None
    except Exception as e:
        error = e.args[0]
        data = {}
        config_hash = 0

    print("dual mom took ", time.time() - start)

    return JsonResponse({'data': data, 'config_hash': config_hash, 'data_load_error': error})

    # with open('temp_data.json', 'r') as infile:
    #     data =  json.load(infile)
    #     return JsonResponse({'data': data, 'ticker_configs': ticker_suggestions})


    #
    #
    # tax_config = {'st_gains': 0.35, 'lt_gains': 0.15, 'federal_tax_rate': 0.22,
    #               'state_tax_rate': 0.12}
    # money_market_holding = 'VGIT'
    # start_date = '1980-01-01'
    # leverage = 1
    # borrowing_cost_above_libor = 1.5
    # parts = [
    #     {
    #         'name': 'equities',
    #         'ticker_list': ['VTI', 'VWO', 'TLT'],
    #         'lookback_months': 12, 'use_dual_momentum': True, 'max_holdings':1, 'weight': 0.5
    #     },
    #     {
    #         'name': 'SP500',
    #         'ticker_list': ['SPY'],
    #         'lookback_months': 12, 'use_dual_momentum': False, 'max_holdings': 1, 'weight': 0.5
    #     }
    # ]
    #
    # momentum_leverages = {
    #    'months_for_lev': 3,
    #                 0.80: -0.3, 0.85: -0.3, 0.90: -0.2, 0.95: -0.2,
    #     1.30:  0.2, 1.20:  0.1, 1.15:  0.1, 1.10:  0.0, 1.05:  0.0
    # }
    #
    #
    # start = time.time()
    # dm = DualMomentumComposite(parts=parts, money_market_holding=money_market_holding,
    #                            momentum_leverages=momentum_leverages, tax_config=tax_config,
    #                            start_date=start_date,
    #                            leverage=leverage,
    #                            borrowing_cost_above_libor=borrowing_cost_above_libor)




@api_view(['GET'])
def list_people(request):
    """
    Return a list of all Person objects, serialized.
    """
    serializer = PersonSerializer(instance=load_json_data(), many=True)
    return Response(serializer.data)
