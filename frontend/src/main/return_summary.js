import React from 'react';
import PropTypes from 'prop-types';

import './return_summary.css'
import { MDBTable, MDBTableBody, MDBTableHead } from 'mdbreact';



export class ReturnsSummary extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            selected_tab: 'Summary'
        }
    }

    switch_table(selection){
        this.setState({'selected_tab': selection})
    }

    render() {
        if (!this.props.data) {
            return (<div/>);
        } else {
            let table;
            let rows = [];
            const d = this.props.data;

            if (this.state.selected_tab === 'Summary') {
                let metrics;
                if (this.props.simulate_taxes) {
                    metrics = [
                        ['CAGR (Pretax)', 'cagr_', '_pretax_str'],
                        ['CAGR (Posttax)', 'cagr_', '_posttax_str'],
                        ['Total Returns (Pretax)', 'total_returns_', '_pretax'],
                        ['Total Returns (Posttax)', 'total_returns_', '_posttax'],
                        ['Max Drawdown ', 'max_dd_', '_pretax_str'],
                        ['Max Drawdown Date ', 'max_dd_date_', '_pretax_str'],
                        ['Sharpe', 'sharpe_', ''],
                        ['Sortino', 'sortino_', ''],
                        ['Annual Volatility', 'annual_volatility_', '_str']
                    ];
                } else {
                    metrics = [
                        ['CAGR', 'cagr_', '_pretax_str'],
                        ['Total Returns', 'total_returns_', '_pretax'],
                        ['Max Drawdown ', 'max_dd_', '_pretax_str'],
                        ['Max Drawdown Date ', 'max_dd_date_', '_pretax_str'],
                        ['Sharpe', 'sharpe_', ''],
                        ['Sortino', 'sortino_', ''],
                        ['Annual Volatility', 'annual_volatility_', '_str']
                    ];
                }

                const columns = [
                    {'label': 'Metric', 'field': 'metric'},
                    {'label': 'Strategy', 'field': 'strategy'},
                    {'label': 'S&P 500', 'field': 'sp500'}
                ];

                let data_rows = [];
                for (const metric of metrics){
                    data_rows.push(
                        {
                            'metric': metric[0],
                            'strategy': d[`${metric[1]}strategy${metric[2]}`],
                            'sp500': d[`${metric[1]}sp500${metric[2]}`]
                        }
                    )
                }
                table =
                    <MDBTable hover>
                        <MDBTableHead columns={columns}/>
                        <MDBTableBody rows={data_rows}/>
                    </MDBTable>;


            } else  if (this.state.selected_tab === 'Monthly Holdings'){
                const component_names = [];
                for (const component of d.monthly_data[0].holdings){
                    component_names.push(component.name);
                }

                const columns = [
                    {'label': 'Date', 'field': 'date', 'sort': 'desc'},
                    {'label': 'Return', 'field': 'returns'}
                ];
                for (const component_name of component_names){
                    columns.push({'label': component_name, 'field': component_name})
                }

                let data_rows = [];
                for (const row of [...d.monthly_data].reverse()){
                    let data_row = {
                        'date': row.date_start.toLocaleDateString('en-US',
                            {month: 'short', year:'numeric'}),
                        'returns': (((row.value_end_pretax / row.value_start_pretax) - 1) *
                             100).toFixed(3) +"%",
                    };
                    for (const component of row.holdings){
                        data_row[component.name] = component.holdings.join(", ")
                    }
                    data_rows.push(data_row);
                }
                table =
                    <MDBTable scrollY hover>
                        <MDBTableHead columns={columns}/>
                        <MDBTableBody rows={data_rows}/>
                    </MDBTable>;
            } else if (this.state.selected_tab === 'Correlations'){
                table =
                    <MDBTable hover>
                        <MDBTableHead columns={this.props.data.correlations.columns}/>
                        <MDBTableBody rows={this.props.data.correlations.data}/>
                    </MDBTable>;
            }

            return (
                <div>
                    <ul className="nav nav-tabs">
                        <li className="nav-item">
                            <a
                                className="nav-link"
                                onClick={() => this.switch_table('Summary')}
                            >Summary</a>
                        </li>
                        <li className="nav-item">
                            <a
                                className="nav-link"
                                onClick={() => this.switch_table('Monthly Holdings')}
                            >Monthly Holdings</a>
                        </li>
                        <li className="nav-item">
                            <a
                                className="nav-link"
                                onClick={() => this.switch_table('Correlations')}
                            >Correlations</a>
                        </li>

                    </ul>
                    {table}
                </div>
            );
        }
    }

}

ReturnsSummary.propTypes={
    data: PropTypes.object,
    simulate_taxes: PropTypes.bool.isRequired
};

