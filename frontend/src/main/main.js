/**
 * UI Code for the visualization
 */
import React from 'react';
import PropTypes from 'prop-types';


import queryString from 'query-string';

// why does the commented out import not work?
import * as json_stable_stringify from 'json-stable-stringify';
// import {json_stable_stringify} from 'json-stable-stringify';

import equal from "fast-deep-equal/es6/react";

import {ReturnsChart} from "./return_chart";
import {AutoCompleteField} from "./autocomplete";
import {ticker_configs} from "./ticker_configs";



import { getCookie } from '../common'
import './main.css';


class MainInterface extends React.Component {
    constructor(props){
        super(props)
    }

    render(){
        const leverage = this.props.config.leverage;
        const borrowing_costs = this.props.config.borrowing_costs_above_libor;
        const start_year = this.props.config.start_year;

        let borrowing_costs_selector = null;
        if (leverage > 1) {
            borrowing_costs_selector = [
                <div key="borrow" className="col-xl-3 col-lg-4 col-md-6 col-sm-6 col-xs-12">
                    <div className="input-group input-group-sm mb-1">
                        <div className="input-group-prepend">
                            <span className="input-group-text tax_type_name">
                                Margin rate (+LIBOR)
                            </span>
                        </div>
                        <input
                            className={"form-control rem-5" + ((borrowing_costs >= 0.00 &&
                                borrowing_costs < 100) ? "" : "is-invalid")}
                            type="number" name="borrowing_costs_above_libor"
                            min={0} max={100} step={0.01}
                            value={borrowing_costs}
                            onChange={(e) => this.props.handle_config_update(e)}
                        />
                        <div className="input-group-append">
                            <span className="input-group-text">%</span>
                        </div>
                        <div className="invalid-feedback">
                            Borrowing costs have to be between 0% and 100%.
                        </div>
                    </div>
                </div>
            ];
        }


        return(
            <div>
                <div className="row">
                    <div className={"col-12"}>
                        <h2>Configuration</h2>
                    </div>
                </div>

                <div className="row">

                    {/*Start Year Selector*/}
                    <div className="col-xl-3 col-lg-4 col-md-6 col-sm-6 col-xs-12">
                        <div className="input-group input-group-sm mb-1">
                            <div className="input-group-prepend">
                                <span className="input-group-text">Start Year </span>
                            </div>
                            <input
                                className={"form-control " + ((start_year >= 1980  &&
                                    start_year < 2018) ? "" : "is-invalid")}
                                type="number" name="start_year" min="1980" max="2018" step={1}
                                value={start_year}
                                onChange={(e) => this.props.handle_config_update(e)}
                            />
                            <div className="invalid-feedback">
                                    Start year has to be between 1980 and 2018.
                            </div>
                        </div>
                    </div>

                    {/*Leverage Selector*/}
                    <div className="col-xl-3 col-lg-4 col-md-6 col-sm-6 col-xs-12">
                        <div className="input-group input-group-sm mb-1">
                            <div className="input-group-prepend">
                                <span className="input-group-text">Leverage </span>
                            </div>
                            <input
                                className={"form-control " + ((leverage > 0.00 && leverage < 4)
                                    ? "" : "is-invalid")}
                                type="number" name="leverage" min="0" max="4" step={0.01}
                                value={leverage}
                                onChange={(e) => this.props.handle_config_update(e)}
                            />
                            <div className="invalid-feedback">
                                    Leverage has to be between 0 and 4.
                            </div>
                        </div>
                    </div>


                    {/*Borrowing Costs*/}
                    {borrowing_costs_selector}

                    {/*Taxes Selector*/}
                    <div className="col-xl-3 col-lg-4 col-md-6 col-sm-6 col-xs-12">
                        <div className={"btn-group btn-group-sm btn-group-toggle mb-1 " +
                            "dual_mom_buttons input-group input-group-sm"} data-toggle="buttons">
                            <div className="input-group-prepend">
                                <span className="input-group-text">Simulate Taxes: </span>
                            </div>
                            <label className={"btn " + (this.props.config.simulate_taxes ?
                                "btn-primary active" : "btn-outline-secondary")}>
                                <input type="radio" name="simulate_taxes"
                                    onChange={(e) => this.props.handle_config_update(e)}
                                />
                                Yes
                            </label>
                            <label className={"btn " + (!this.props.config.simulate_taxes ?
                                "btn-primary active" : "btn btn-outline-secondary")}>
                                <input type="radio" name="simulate_taxes"
                                    onChange={(e) => this.props.handle_config_update(e)}
                                />
                                No
                            </label>
                        </div>
                    </div>
                </div>
                <TaxConfig
                    key={0}
                    config={this.props.config}
                    handle_config_update={(e) => this.props.handle_config_update(e)}
                    handle_tax_rate_update={(tax_type, rate) =>
                        this.props.handle_tax_rate_update(tax_type, rate)}
                />
            </div>
        )
    }
}
MainInterface.propTypes={
    config: PropTypes.object.isRequired,
    handle_config_update: PropTypes.func.isRequired,
    handle_tax_rate_update: PropTypes.func.isRequired,
};


class TaxConfig extends React.Component{
    constructor(props){
        super(props);

        this.config_to_name = {
            'short_term_cap_gains_rate': 'Short Term Cap Gains',
            'long_term_cap_gains_rate': 'Long Term Cap Gains',
            'munis_state_rate': 'Muni Bonds Income',
            'treasuries_income_rate': 'Treasuries Income',
            'gld_lt_rate': 'Gold LT Capital Gains',
        }
    }

    render() {
        if (this.props.config.simulate_taxes){
            let selectors = [];
            for (const [tax_type, _i] of Object.entries(this.props.config.tax_rates)){
                const tax_name = this.config_to_name[tax_type];
                const tax_rate = this.props.config.tax_rates[tax_type];
                const rate_valid = (tax_rate >= 0 && tax_rate <= 100);
                selectors.push(

                    <div key={tax_type} className="col-xl-3 col-lg-4 col-md-6 col-sm-12 col-xs-12">
                        <div className="tax_rate_selector input-group input-group-sm">
                            <div className="input-group-prepend">
                                <span className="input-group-text tax_type_name">{tax_name}</span>
                            </div>
                            <input
                                className={"form-control rem-5 " +
                                    ((tax_rate >= 0 && tax_rate <= 100) ? "" : "is-invalid")}
                                type="number" name={tax_type} min="0" max="100"
                                value={tax_rate}
                                onChange={(e) =>
                                    this.props.handle_tax_rate_update(tax_type, e.target.value)}
                            />
                            <div className="input-group-append">
                                <span className="input-group-text">%</span>
                            </div>
                            <div className="invalid-feedback">
                                    Tax percentage needs to be between 0 and 100.
                            </div>
                        </div>
                    </div>
                )
            }

            return(
                <div className="row">
                    {selectors}
                </div>
            )
        } else {
            return(null)
        }

    }
}
TaxConfig.propTypes={
    config: PropTypes.object.isRequired,
    handle_config_update: PropTypes.func.isRequired,
    handle_tax_rate_update: PropTypes.func.isRequired,
};

class ComponentSelector extends React.Component {
    constructor(props){
        super(props);
    }


    render() {

        // figure out if this is the final empty component
        const is_empty_component = (!('weight' in this.props.config));

        // Empty component Shell
        if (is_empty_component) {
            return (
                <div className="col-xl-3 col-lg-4 col-md-4 col-sm-6 col-xs-12 mt-4">
                    {/*Title / Name*/}
                    <input className="component_title form-control component_title_new"
                        type="text" name="name" maxLength="14" size="14" disabled
                        value={this.props.config.name}
                    />
                    {/*Add component form*/}
                    <div className="input-group input-group-sm mb-1">
                        <input className="form-control "
                            type="text" name="name" maxLength="14" size="14"
                            value={this.props.config.name}
                            onChange={(e) => this.props.handle_component_update(e)}
                        />
                        <div className="input-group-append">
                            <button className="btn btn-primary active" type="button"
                                name="add_component"
                                onClick={(e) => this.props.handle_component_update(e)}>
                                Add Component
                            </button>
                        </div>
                    </div>
                </div>
            )

        // filled component
        } else {
            let holding_boxes = [];
            for (const [holding_id, ticker] of this.props.config.holdings.entries()) {
                holding_boxes.push(
                    <AutoCompleteField
                        key={`${holding_id}_${ticker}`}
                        ticker={ticker}
                        selection_options={ticker_configs}
                        handle_holding_update={(ticker) =>
                            this.props.handle_holding_update(holding_id, ticker)}
                    />
                );
            }

            // For buy and hold, only display and use the first ticker
            if (!this.props.config.dual_momentum) {
                holding_boxes = holding_boxes.slice(0, 1);
            }

            return (
                <div className="col-xl-3 col-lg-4 col-md-4 col-sm-6 col-xs-12 mt-4">

                    {/*Title / Name*/}
                    <input className="component_title form-control"
                        type="text" name="name" maxLength="14" size="14"
                        value={this.props.config.name}
                        onChange={(e) => this.props.handle_component_update(e)}
                    />

                    {/*Buy and Hold  / Dual Momentum Selector */}
                    <div className="btn-group btn-group-sm btn-group-toggle mb-1 dual_mom_buttons"
                        data-toggle="buttons">
                        <label
                            className={this.props.config.dual_momentum ? "btn btn-primary active" :
                                "btn btn-outline-secondary"}>
                            <input type="radio" name="dual_momentum"
                                onChange={(e) => this.props.handle_component_update(e)}
                            />
                            Dual Momentum
                        </label>
                        <label
                            className={!this.props.config.dual_momentum ? "btn btn-primary active" :
                                "btn btn-outline-secondary"}>
                            <input type="radio" name="dual_momentum"
                                onChange={(e) => this.props.handle_component_update(e)}
                            />
                            Buy and Hold
                        </label>
                    </div>

                    {/*Number of holdings selector*/}
                    <div className="input-group input-group-sm mb-1">
                        <div className="input-group-prepend">
                            <span className="input-group-text">Number of holdings: </span>
                        </div>
                        <input
                            className={"form-control" + ((
                                [1, 2].includes(this.props.config.max_holdings) ||
                                !this.props.config.dual_momentum) ? "" : " is-invalid")}
                            disabled={!this.props.config.dual_momentum}
                            type="number" name="max_holdings" min="1" max="2"
                            value={this.props.config.dual_momentum ?
                                this.props.config.max_holdings : ""}
                            onChange={(e) => this.props.handle_component_update(e)}
                        />
                        <div className="invalid-feedback">
                            Number of holdings per category has to be 1 or 2.
                        </div>
                    </div>

                    {/*Lookback selector*/}
                    <div className="input-group input-group-sm mb-1">
                        <div className="input-group-prepend">
                            <span className="input-group-text rem-6">Lookback: </span>
                        </div>
                        <input
                            className={!this.props.config.dual_momentum ||
                            (this.props.config.lookback >= 1 && this.props.config.lookback <= 24) ?
                                "form-control" : "form-control is-invalid"}
                            disabled={!this.props.config.dual_momentum}
                            type="number" name="lookback" min="1" max="24"
                            value={this.props.config.dual_momentum ? this.props.config.lookback :""}
                            onChange={(e) => this.props.handle_component_update(e)}
                        />
                        <div className="input-group-append">
                            <span className="input-group-text">months</span>
                        </div>
                        <div className="invalid-feedback">
                            Lookback has to be between 1 and 24 months.
                        </div>
                    </div>


                    {/*Weight selector*/}
                    <div className="mb-1">
                        <div className="input-group input-group-sm">
                            <div className="input-group-prepend">
                                <span className="input-group-text rem-6">Weight: </span>
                            </div>
                            <input
                                className={this.props.total_allocated_weight === 100 ?
                                    "form-control" : "form-control is-invalid"}
                                type="number" name="weight" min="0" max="100"
                                value={this.props.config.weight}
                                onChange={(e) => this.props.handle_component_update(e)}
                            />
                            <div className="input-group-append">
                                <span className="input-group-text">%</span>
                            </div>
                            <div className="invalid-feedback">
                                Total weights need to add to 100%.
                            </div>
                        </div>
                    </div>
                    <div className="ticker_list">
                        <div>
                            <div className="input-group input-group-sm">
                                <div className="input-group-prepend ticker_list_heading">
                                    <span className="input-group-text ticker_list_heading">
                                        Ticker List:
                                    </span>
                                </div>
                            </div>
                            <div className="holding_boxes">
                                {holding_boxes}
                            </div>
                        </div>
                    </div>


                    {/*Add / Remove ticker buttons*/}
                    {(this.props.config.dual_momentum || this.props.config.holdings.length === 0) ?
                        <button type="button" className="btn btn-sm btn-outline-primary"
                            onClick={() => this.props.modify_number_of_holdings(1)}
                        >Add Ticker</button> : null
                    }
                    <button type="button" className="btn btn-sm btn-outline-primary button_remove"
                        onClick={() => this.props.modify_number_of_holdings(-1)}
                    >Remove {this.props.config.holdings.length > 0 ? 'Ticker' : 'Part'}</button>
                </div>
            )
        }
    }
}
ComponentSelector.propTypes={
    config: PropTypes.object.isRequired,
    total_allocated_weight: PropTypes.number.isRequired,
    handle_component_update: PropTypes.func.isRequired,
    handle_holding_update: PropTypes.func.isRequired,
    modify_number_of_holdings: PropTypes.func.isRequired
};


/***************************************************************************************************
 * Main component for the main view.
 **************************************************************************************************/
class MainView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: null,  // data for the viz
            ticker_configs: null,
            dm_config: {

                'costs_per_trade': 0.1,
                'start_year': 1980,

                'leverage': 1.0,
                'borrowing_costs_above_libor': 1.5,

                'simulate_taxes': true,
                'tax_rates': {
                    'short_term_cap_gains_rate': 34,
                    'long_term_cap_gains_rate':  20.1,
                    'munis_state_rate':          12.1,
                    'treasuries_income_rate':     9.82,
                    // 'short_term_cap_gains_rate': {'name': 'Short Term Cap Gains', 'rate':34},
                    // 'long_term_cap_gains_rate': {'name': 'Long Term Cap Gains', 'rate': 20.1},
                    // 'munis_state_rate': {'name': 'Muni Bonds Income ', 'rate': 12.1},
                    // 'treasuries_income_rate': {'name': 'Treasuries Income ', 'rate': 9.82},
                    // 'gld_lt_rate': {'name': 'Gold LT Capital Gains', 'rate': 20.1},
                },
                'money_market_holding': 'VGIT',
                'momentum_leverages': {
                    'months_for_leverage': 3,
                    'config': {
                        0.8: -0.3,  0.85: -0.3,    0.90: -0.2, 0.95: -0.2,
                        1.30: 0.2,  1.20:  0.1,  1.15:  0.1,    1.10:  0.0, 1.05:  0.0
                    }
                }
            },
            dm_components: [
                {
                    'name': 'Equities',
                    'weight': 50,
                    'dual_momentum': true,
                    'lookback': 12,
                    'max_holdings': 2,
                    'holdings': ['VTI', 'IEFA', 'IEMG', ''],
                },
                {
                    'name': 'REITs',
                    'weight': 50,
                    'dual_momentum': true,
                    'lookback': 12,
                    'max_holdings': 1,
                    'holdings': ['VNQ', 'VNQI', 'IEF', '']
                },
                {
                    'name': '',
                }
            ]
        };
        this.csrftoken = getCookie('csrftoken');
        this.time_of_last_state_change = Date.now()
    }

    shouldComponentUpdate(nextProps, nextState, nextContext) {

        console.log("shouldUpdate",
            this.state.dm_components[0].holdings, nextState.dm_components[0].holdings);
        return true
    }

    componentDidMount() {
        this.load_result_data();
    }

    handle_config_update(event){

        let dm_config = {... this.state.dm_config};
        const ename = event.target.name;

        if (ename === 'simulate_taxes') {
            dm_config['simulate_taxes'] = !dm_config['simulate_taxes']
        } else if (ename === 'start_year'){
            dm_config[ename] = parseInt(event.target.value);
        } else if (ename === 'borrowing_costs_above_libor' || ename === 'leverage'){
            dm_config[ename] = parseFloat(event.target.value);
        }
        this.setState({dm_config})
    }

    handle_tax_rate_update(tax_type, rate) {
        let dm_config = {... this.state.dm_config};
        let tax_rates = {... dm_config.tax_rates};
        tax_rates[tax_type] = parseFloat(rate);
        dm_config.tax_rates = tax_rates;
        this.setState({dm_config});
    }

    handle_holding_update(component_id, holding_id, ticker){
        let dm_components = [... this.state.dm_components];
        let dm_component = {... dm_components[component_id]};
        let holdings = [... dm_components[component_id]['holdings']];
        holdings[holding_id] = ticker;

        dm_component.holdings = holdings;
        dm_components[component_id] = dm_component;
        this.setState({dm_components});
    }

    handle_component_update(component_id, event){
        console.log("handle component update", component_id, event.target);

        if (event.target.name === 'add_component'){
            this.modify_number_of_components(1, null);
        } else {

            let dm_components = [... this.state.dm_components];
            let dm_component = {... dm_components[component_id]};

            if (event.target.name === 'dual_momentum') {
                dm_component['dual_momentum'] = !dm_component['dual_momentum']
            } else if (event.target.name === 'weight') {
                dm_component[event.target.name] = parseFloat(event.target.value);
                // dm_components[component_id][event.target.name] = parseFloat(event.target.value);
            } else if (event.target.name === 'lookback' || event.target.name === 'max_holdings') {
                dm_component[event.target.name] = parseInt(event.target.value);
                // dm_components[component_id][event.target.name] = parseInt(event.target.value);
            } else if (event.target.name === 'name') {
                dm_component[event.target.name] = event.target.value;
                // dm_components[component_id][event.target.name] = event.target.value;
            }
            dm_components[component_id] = dm_component;
            this.setState({dm_components});
        }
    }


    modify_number_of_components(i, component_id){
        // Add or remove components
        let dm_components = [... this.state.dm_components];

        // add new component
        if (i === 1) {
            let dm_component = {... dm_components[dm_components.length - 1]};
            dm_component = {
                'name': dm_components[dm_components.length -1].name,
                'weight': 0,
                'dual_momentum': true,
                'lookback': 12,
                'max_holdings': 1,
                'holdings': ['']
            };
            // add new empty component at the end
            dm_components[dm_components.length - 1] = dm_component;
            dm_components.push({'name': ''})

        // remove component
        } else {
            dm_components = dm_components.slice(
                0, component_id).concat(dm_components.slice(component_id +1));
        }

        this.setState({dm_components: dm_components});
    }

    modify_number_of_holdings(i, component_id) {
        let dm_components = [... this.state.dm_components];
        let dm_component = {... dm_components[component_id]};
        let holdings = [... dm_component.holdings];

        // add new holding
        if (i === 1) {
            holdings.push('');
            dm_component.holdings = holdings;
            dm_components[component_id] = dm_component
        //remove holding
        } else {
            // let holdings = dm_components[component_id]['holdings'];
            if (holdings.length > 0) {
                // if dual momentum mode, remove last holding
                if (dm_component['dual_momentum']) {
                    holdings = holdings.slice(0, -1);
                } else { // if buy and hold, remove the only remaining holding
                    holdings = [];
                }
                dm_component.holdings = holdings;
                dm_components[component_id] = dm_component

                // dm_components[component_id]['holdings'] = holdings;
            } else {
                this.modify_number_of_components(-1, component_id);
                return
            }
        }
        this.setState({dm_components});
    }

    async load_result_data() {
        // const dataset = encodeURIComponent(dataset_name);
        fetch(`get_test_data`)
            .then((response) => {
                response
                    .json()
                    .then((d) => {
                        let data = d.data;
                        data.forEach(element => {
                            element.date_str = element.date;
                            element.date_start = new Date(element.date[0], element.date[1]);
                            element.date_end = new Date(element.date[0], element.date[1] + 1);
                        });
                        this.setState({data:data, ticker_configs: d.ticker_configs});
                        return true
                    })
            }).catch(() => {
                console.log("error");
                return false
            });

    }




    render() {

        // get total weight allocated (should be 100)
        let total_allocated_weight = 0;

        for (const [_i, component] of this.state.dm_components.entries()) {
            if (!isNaN(component.weight)) {
                total_allocated_weight += component.weight;
            }
        }

        let dm_components = [];


        for (const [component_id, _d] of this.state.dm_components.entries()) {
            dm_components.push(
                <ComponentSelector
                    key={component_id}
                    config={{... this.state.dm_components[component_id]}}
                    total_allocated_weight={total_allocated_weight}
                    handle_holding_update={(holding_id, ticker) => {
                        this.handle_holding_update(component_id, holding_id, ticker)
                    }}
                    handle_component_update={(event) => {
                        this.handle_component_update(component_id, event)
                    }}
                    modify_number_of_holdings={(i) => {
                        this.modify_number_of_holdings(i, component_id)
                    }}
                />
            )
        }

        return (
            <div className="container">
                <MainInterface
                    config={{... this.state.dm_config}}
                    handle_config_update={(e) => this.handle_config_update(e)}
                    handle_tax_rate_update={(tax_type, rate) =>
                        this.handle_tax_rate_update(tax_type, rate)}
                />
                <div className="row">
                    {dm_components}
                </div>
                <div className={"row"}>
                    <div id={"chart_container"}>
                        <ReturnsChart
                            data={this.state.data}
                            width={800}
                            height={400}
                        />
                    </div>
                </div>
            </div>
        );
    }


    update_url(old_stringified_config){


        let cur_stringified_config = json_stable_stringify({
            'dm_components':  this.state.dm_components,
            'dm_config': this.state.dm_config
        });

        console.log("same?", old_stringified_config === cur_stringified_config);
    }

    componentDidUpdate(prevProps, prevState, snapshot) {

        const time_now = Date.now();
        console.log("time", time_now - this.time_of_last_state_change);

        console.log(this.state);

        console.log(this.state.dm_components[0].holdings, prevState.dm_components[0].holdings);
        console.log(
            equal(prevState.dm_components, this.state.dm_components),
            equal(prevState.dm_config, this.state.dm_config)
        );

        // this.time_of_last_state_change


        let stringified_config = json_stable_stringify({
            'dm_components':  this.state.dm_components,
            'dm_config': this.state.dm_config
        });

        setTimeout(() => {
            this.update_url(stringified_config)
        }, 2000);
        console.log("main");

        console.log(stringified_config);
        const url_config =  queryString.stringify({'conf': stringified_config});
        console.log(url_config);

        // window.history.pushState(this.state.dm_components);
    }
}

// when importing Main what do we get?
export default MainView;
