"""
Views that define API endpoints for the site
"""
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import PersonSerializer
from .models import load_json_data
from django.http import JsonResponse, HttpResponse

def get_test_data(request):

    from dual_momentum.dm_composite import DualMomentumComposite

    tax_config = {'st_gains': 0.35, 'lt_gains': 0.15, 'federal_tax_rate': 0.22,
                  'state_tax_rate': 0.12}
    money_market_holding = 'VGIT'
    start_date = '1980-01-01'
    leverage = 2
    borrowing_cost_above_libor = 1.5
    parts = [
        {
            'name': 'equities',
            'ticker_list': ['VTI', 'VWO'],
            'lookback_months': 12, 'use_dual_momentum': True, 'max_holdings':1, 'weight': 0.5
        },
        {
            'name': 'SP500',
            'ticker_list': ['SPY'],
            'lookback_months': 12, 'use_dual_momentum': False, 'max_holdings': 1, 'weight': 0.5
        }
    ]

    momentum_leverages = {
       'months_for_lev': 3,
                    0.80: -0.3, 0.85: -0.3, 0.90: -0.2, 0.95: -0.2,
        1.30:  0.2, 1.20:  0.1, 1.15:  0.1, 1.10:  0.0, 1.05:  0.0
    }

    dm = DualMomentumComposite(parts=parts, money_market_holding=money_market_holding,
                               momentum_leverages=momentum_leverages, tax_config=tax_config,
                               start_date=start_date,
                               leverage=leverage,
                               borrowing_cost_above_libor=borrowing_cost_above_libor)
    dm.run_multi_component_dual_momentum()
    return JsonResponse({'data': dm.get_result_json()})



@api_view(['GET'])
def list_people(request):
    """
    Return a list of all Person objects, serialized.
    """
    serializer = PersonSerializer(instance=load_json_data(), many=True)
    return Response(serializer.data)
