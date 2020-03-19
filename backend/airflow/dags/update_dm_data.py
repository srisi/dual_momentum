from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

import time


def load_dual_momentum_ticker_data():
    """
    Load data for all tickers from yahoo and store monthly and daily dataframes
    in redis

    :return:
    """
    from dual_momentum.ticker_data import TickerData
    from dual_momentum.ticker_config import TICKER_CONFIG
    for ticker in TICKER_CONFIG:
        if ticker == 'TBIL':
            continue

        time.sleep(1)
        print(ticker)
        _ = TickerData(ticker).data_monthly


def load_fred_data():
    """
    Load fred data (libor, tbil, 10y term premium, treasury yields)

    :return:
    """

    print('loading fred data')
    from dual_momentum.fred_data import load_fred_data

    for index_name in ['libor_rate', 'tbil_rate', 'term_premium_10y',
                       'treasuries_10y_yield']:
        load_fred_data(index_name)

def load_default_dm_composite():
    """
    Load default dual momentum composite for website

    :return:
    """
    from dual_momentum.dm_composite import DualMomentumComposite
    tax_config = {'fed_st_gains': 0.22, 'fed_lt_gains': 0.15, 'state_st_gains': 0.12,
                  'state_lt_gains': 0.051}
    money_market_holding = 'VGIT'
    start_date = '1980-01-01'
    leverage = 1
    borrowing_cost_above_libor = 1.5
    parts = [
        {
            'name': 'Equities',
            'ticker_list': ['VTI', 'IEFA', 'IEMG'],
            'lookback_months': 12, 'use_dual_momentum': True, 'max_holdings': 1, 'weight': 0.25
        },
        {
            'name': 'REITs',
            'ticker_list': ['VNQ', 'REM'],
            'lookback_months': 12, 'use_dual_momentum': True, 'max_holdings': 1, 'weight': 0.25
        },
        {
            'name': 'Bonds',
            'ticker_list': ['LQD', 'HYG'],
            'lookback_months': 12, 'use_dual_momentum': True, 'max_holdings': 1, 'weight': 0.25
        },
        {
            'name': 'Safety',
            'ticker_list': ['TLT', 'GLD'],
            'lookback_months': 12, 'use_dual_momentum': True, 'max_holdings': 1, 'weight': 0.25
        }
    ]

    momentum_leverages = {
        'months_for_lev': 3,
        0.80: 0, 0.85: 0, 0.90: 0, 0.95: 0,
        1.30: 0, 1.20: 0, 1.15: 0, 1.10: 0.0, 1.05: 0.0
    }

    dm = DualMomentumComposite(parts=parts, money_market_holding=money_market_holding,
                               momentum_leverages=momentum_leverages, tax_config=tax_config,
                               start_date=start_date,
                               leverage=leverage,
                               borrowing_cost_above_libor=borrowing_cost_above_libor,
                               force_new_data=False)

    dm.run_multi_component_dual_momentum()
    dm.generate_results_summary()
    return True


args = {
    'owner': 'Airflow',
    'start_date': days_ago(1),

    'email_on_failure': True,
    'email': ['stephan.risi+aws_errors@gmail.com']

}

dag = DAG(
    dag_id='update_dual_momentum_data',
    default_args=args,
    catchup=False,
    schedule_interval='*/5 * * * *',

)

dual_momentum_ticker_loader = PythonOperator(
    task_id='load_dual_momentum_ticker_data',
    python_callable=load_dual_momentum_ticker_data,
    dag=dag
)

fred_data_loader = PythonOperator(
    task_id='load_fred_data',
    python_callable=load_fred_data,
    dag=dag
)

default_dm_composite_loader = PythonOperator(
    task_id='load_default_dm_composite',
    python_callable=load_default_dm_composite,
    dag=dag
)

fred_data_loader >> default_dm_composite_loader
dual_momentum_ticker_loader >> default_dm_composite_loader

#
# run_this = PythonOperator(
#     task_id='print_the_context',
#     provide_context=True,
#     python_callable=print_context,
#     dag=dag,
# )
# # [END howto_operator_python]

#
# # [START howto_operator_python_kwargs]
# def my_sleeping_function(random_base):
#     """This is a function that will run within the DAG execution"""
#     time.sleep(random_base)


# # Generate 5 sleeping tasks, sleeping from 0.0 to 0.4 seconds respectively
# for i in range(5):
#     task = PythonOperator(
#         task_id='sleep_for_' + str(i),
#         python_callable=my_sleeping_function,
#         op_kwargs={'random_base': float(i) / 10},
#         dag=dag,
#     )

    # dummy_operator >> task
# [END howto_operator_python_kwargs]
