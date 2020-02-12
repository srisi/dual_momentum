from dual_momentum.dm_composite import DualMomentumComposite
from dual_momentum.fred_data import load_fred_data
from IPython import embed


import time
import itertools
import random
from dual_momentum.dm_config import DATA_PATH
from collections import deque

from pathlib import Path

import sqlite3

from multiprocessing import Manager, Process, cpu_count
FLAG_ALL_DONE = "WORK FINISHED"
FLAG_WORKER_FINISHED_PROCESSING = "WORKER FINISHED PROCESSING"


class DualMomentumComparisonRunner:
    """
    Simulates and compares multiple configurations and stores them in a sqlite
    table

    """

    def __init__(self, db_table_name, runner_type, **kwargs):

        default_config = {
            'money_market_holding': 'VGIT',
            'start_date': '1980-01-01',
            'leverage': 1,
            'borrowing_cost_above_libor': 1.5,
            'lookback_months': 12,
            'tax_config': {
                'fed_st_gains': 0.22, 'fed_lt_gains': 0.15, 'state_st_gains': 0.12,
                'state_lt_gains': 0.051
            },
            'momentum_leverages': {
                'months_for_lev': 3,
                            0.80: -0.3, 0.85: -0.3, 0.90: -0.2, 0.95: -0.2,
                1.30:  0.2, 1.20:  0.1, 1.15:  0.1, 1.10:  0.0, 1.05:  0.0
            }
        }

        for config_item in ['tax_config', 'money_market_holding', 'start_date',
                            'leverage', 'borrowing_cost_above_libor',
                            'momentum_leverages']:
            if config_item in kwargs.keys():
                setattr(self, config_item, kwargs[config_item])
            else:
                setattr(self, config_item, default_config[config_item])

        self.runner_type = runner_type
        self.dmcs = []
        if self.runner_type == 'compare_single_component':
            if 'tickers' not in kwargs.keys():
                raise KeyError("when running compare_single_comoponent, you need to"
                               "specify a list of tickers to compare")
            else:
                tickers = kwargs['tickers']
                libor_rates = load_fred_data('libor_rate')
                if 'looback_months' in kwargs.keys():
                    lookback_months = kwargs['lookback_months']
                else:
                    lookback_months = default_config['lookback_months']

                for i in range(1, len(tickers) + 1):
                    print(i, len(self.dmcs))
                    for combo in itertools.combinations(tickers, i):
                        parts = [
                            {
                                'name': 'part1',
                                'ticker_list': sorted(combo),
                                'lookback_months': kwargs['lookback_months'],
                                'use_dual_momentum': kwargs['use_dual_momentum'],
                                'max_holdings': kwargs['max_holdings'],
                                'weight': 1
                            }
                        ]
                        dmc = DualMomentumComposite(
                            parts=parts, money_market_holding=self.money_market_holding,
                            start_date=self.start_date, momentum_leverages=self.momentum_leverages,
                            tax_config=self.tax_config, leverage=self.leverage,
                            borrowing_cost_above_libor=self.borrowing_cost_above_libor,
                            force_new_data=False, libor_rates=libor_rates, is_backtest=True)
                        self.dmcs.append(dmc)


        self.db_path = str(Path(DATA_PATH, 'comparison_db', 'comparison.db'))
        self.db_table_name = db_table_name
        self.init_db_table(kwargs)

    def init_db_table(self, kwargs):

        db_path = str(Path(DATA_PATH, 'comparison_db', 'comparison.db'))
        db = sqlite3.connect(db_path)
        cur = db.cursor()

        if self.runner_type == 'compare_single_component':

            cur.execute(f'''CREATE TABLE IF NOT EXISTS {self.db_table_name}(
                            hash            text,
                            ticker_list     text,
                            lookback_months int,
                            max_holdings    int,
                            
                            max_dd_pretax   real,
                            max_dd_posttax  real,
                            cagr_pretax     real,
                            cagr_posttax    real,
                            max_dd_date     text,
                            sharpe          real,
                            sortino         real,
                            cor_sp500       real,
                            
                            UNIQUE(hash) ON CONFLICT REPLACE
                            );
        ''')


    def run_comparison(self):

        db = sqlite3.connect(self.db_path)
        cur = db.cursor()
        random.shuffle(self.dmcs)
        entry_queue = Manager().Queue()
        results_queue = Manager().Queue()
        for idx, dmc in enumerate(self.dmcs):
            entry_queue.put(dmc)
        self.dmcs = None

        number_of_processes = 7
        for _ in range(number_of_processes):
            entry_queue.put('FLAG_ALL_DONE')

        for process_n in range(number_of_processes):
            p = Process(target=self.run_comparison_worker, args=(entry_queue, results_queue))
            p.start()

        processors_finished = 0
        while True:
            time.sleep(0.1)
            new_result = results_queue.get()

            if new_result == FLAG_WORKER_FINISHED_PROCESSING:
                processors_finished += 1
                print("Finished", processors_finished)
                if processors_finished == number_of_processes:
                    break

    def run_comparison_worker(self, entry_queue, results_queue):

        db = sqlite3.connect(self.db_path)
        cur = db.cursor()
        while True:
            entry = entry_queue.get()
            print(entry == 'FLAG_ALL_DONE', entry)
            if entry == 'FLAG_ALL_DONE':
                results_queue.put(FLAG_WORKER_FINISHED_PROCESSING)
                break
            else:
                dmc = entry
                cur.execute(f'SELECT hash FROM {self.db_table_name} WHERE hash="{dmc.__hash__()}"')
                if cur.fetchall():
                    continue

                dmc.run_multi_component_dual_momentum()
                dmc.generate_results_summary()

                sql = f'''INSERT INTO {self.db_table_name} (
                            hash, ticker_list, lookback_months, max_holdings,
                            max_dd_pretax, max_dd_posttax, max_dd_date, 
                            cagr_pretax, cagr_posttax, sharpe, sortino, cor_sp500) 
                               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'''
                s = dmc.summary
                comp = dmc.components[0]
                print(comp.max_holdings)
                sql_res = (dmc.__hash__(),
                           str(comp.ticker_list), comp.lookback_months, comp.max_holdings,
                           s['max_dd_strategy_pretax'], s['max_dd_strategy_posttax'],
                           s['max_dd_date_strategy_posttax_str'], s['cagr_strategy_pretax'],
                           s['cagr_strategy_posttax'], s['sharpe_strategy'], s['sortino_strategy'],
                           s['correlations']['data'][0]['performance_sp500_pretax'])
                cur.execute(sql, sql_res)
                db.commit()


def bond_comparsion():

    tickers =  [
        'SHY', 'VGIT', 'IEF', 'TLT', 'TIP',
        'BOND', 'BND',
        'LQD', 'VCSH', 'HYG',
        'VTEB', 'HYD', 'MBB',
        'CWB',
        'BNDX', 'PCY'
    ]
    comp_runner = DualMomentumComparisonRunner(
        db_table_name='bond_comparison', runner_type='compare_single_component',
        tickers=tickers, lookback_months=6, use_dual_momentum=True, max_holdings=2)
    comp_runner.run_comparison()

def equities_comparison():
    tickers = [
        'VTI', 'QQQ', 'IEFA', 'IEMG',
        'VB', 'VSS',
        # 'VMOT', 'QVAL', 'QMOM', 'IVAL', 'IMOM'
    ]
    comp_runner = DualMomentumComparisonRunner(
        db_table_name='eq_comparison_no_alpha', runner_type='compare_single_component',
        tickers=tickers, lookback_months=12, use_dual_momentum=True, max_holdings=2)
    comp_runner.run_comparison()


if __name__ == '__main__':
    equities_comparison()
