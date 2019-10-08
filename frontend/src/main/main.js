/**
 * UI Code for the visualization
 */
import React from 'react';
import PropTypes from 'prop-types';

import { getCookie } from '../common'
import { create_graph, update_graph_color } from './graph.js'
import './main.css';

class MainInterface extends React.Component {
    constructor(props){
        super(props)
    }
}

class ComponentSelector extends React.Component {
    constructor(props){
        super(props);
    }

    render(){
        let holding_boxes = [];
        for (const [_i, holding] of this.props.config.holdings.entries()) {
            holding_boxes.push(
                <HoldingBox
                    key={holding.id}
                    holding={holding}
                    handle_holding_update={(event) =>
                        this.props.handle_holding_update(holding.id, event)
                    }
                />
            );
        }

        // For buy and hold, only display and use the first ticker
        if (!this.props.config.dual_momentum){
            holding_boxes = holding_boxes.slice(0, 1);
        }

        console.log(this.props.total_allocated_weight, this.props.total_allocated_weight === 100);


        return (
            <div className="dm_component col-lg-4 col-md-6 col-sm-6 col-xs-12">
                <h2>{this.props.config.name}</h2>

                {/*Buy and Hold Selector */}
                <div className="btn-group btn-group-toggle mb-1 dual_mom_buttons"
                    data-toggle="buttons">
                    <label className={this.props.config.dual_momentum ? "btn btn-primary active":
                        "btn btn-outline-secondary"}>
                        <input type="radio" name="dual_momentum"
                            onChange={(e) => this.props.handle_component_update(e)}
                        />
                        Dual Momentum
                    </label>
                    <label className={!this.props.config.dual_momentum ? "btn btn-primary active":
                        "btn btn-outline-secondary"}>
                        <input type="radio" name="dual_momentum"
                            onChange={(e) => this.props.handle_component_update(e)}
                        />
                        Buy and Hold
                    </label>
                </div>

                {/*Number of holdings selector*/}
                <div className="input-group mb-1">
                    <div className="input-group-prepend">
                        <span className="input-group-text">Number of holdings: </span>
                    </div>
                    <input
                        className={(
                            [1,2].includes(this.props.config.max_holdings) ||
                                !this.props.config.dual_momentum) ?
                            "form-control" : "form-control is-invalid"}
                        disabled={!this.props.config.dual_momentum}
                        type="number" name="max_holdings" min="1" max="2"
                        value={this.props.config.dual_momentum ? this.props.config.max_holdings : ""}
                        onChange={(e) => this.props.handle_component_update(e)}
                    />
                    <div className="invalid-feedback">
                            Number of holdings per category has to be 1 or 2.
                    </div>
                </div>

                {/*Duration selector*/}
                <div className="input-group mb-1">
                    <div className="input-group-prepend">
                        <span className="input-group-text rem-6">Duration: </span>
                    </div>
                    <input
                        className={!this.props.config.dual_momentum ||
                        (this.props.config.duration >= 1 && this.props.config.duration <= 24) ?
                            "form-control" : "form-control is-invalid"}
                        disabled={!this.props.config.dual_momentum}
                        type="number" name="duration" min="1" max="24"
                        value={this.props.config.dual_momentum ? this.props.config.duration : ""}
                        onChange={(e) => this.props.handle_component_update(e)}
                    />
                    <div className="input-group-append">
                        <span className="input-group-text">months</span>
                    </div>
                    <div className="invalid-feedback">
                            Duration has to be between 1 and 24 months.
                    </div>
                </div>


                {/*Weight selector*/}
                <div className="mb-1">
                    <div className="input-group">
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

                <div>{holding_boxes}</div>
                {(this.props.config.dual_momentum || this.props.config.holdings.length === 0) ?
                    <button type="button" className="btn btn-outline-primary"
                        onClick={() => this.props.modify_number_of_holdings(1)}
                    >Add Ticker</button> : null
                }
                <button type="button" className="btn btn-outline-primary button_remove"
                    onClick={() => this.props.modify_number_of_holdings(-1)}
                >Remove {this.props.config.holdings.length > 0 ? 'Ticker': 'Part'}</button>
            </div>
        )
    }
}
ComponentSelector.propTypes={
    config: PropTypes.object,
    total_allocated_weight: PropTypes.number,
    handle_component_update: PropTypes.func,
    handle_holding_update: PropTypes.func,
    modify_number_of_holdings: PropTypes.func
};

class HoldingBox extends React.Component {
    constructor(props){
        super(props);
    }

    render(){
        return (
            <div className="input-group mb-1">
                <div className="input-group-prepend">
                    <span className="input-group-text rem-6">Ticker {this.props.holding.id + 1}: </span>
                </div>
                <input className="form-control input_ticker"
                    type="text" name="ticker" maxLength="20" size="20"
                    value={this.props.holding.ticker}
                    onChange={(e) => this.props.handle_holding_update(e)}
                />
            </div>
        )
    }
}
HoldingBox.propTypes={
    holding: PropTypes.object,
    handle_holding_update: PropTypes.func
};


/***************************************************************************************************
 * Main component for the main view.
 **************************************************************************************************/
class MainView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            config: {
                width: 500,
                height: 500,
                color: 'blue',
            },  // initial configuration for the viz
            data: null,  // data for the viz
            mouseover: false,  // info panel state (based on callbacks from viz)
            dm_config: {
                'leverage': 1.0,
                'borrowing_costs_above_libor': 0.015,
                'costs_per_trade': 0.001,
                'start_year': 1980,

                'simulate_taxes': true,
                'short_term_cap_gains_rate': 0.34,
                'long_term_cap_gains_rate': 0.201,
                'munis_state_rate': 0.121,
                'treasuries_income_rate': 0.0982,
                'gld_lt_rate': 0.201,
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
                    'id': 0,
                    'name': 'Equities',
                    'weight': 50,
                    'dual_momentum': true,
                    'duration': 12,
                    'max_holdings': 2,
                    'holdings': [
                        {'id': 0, 'ticker': 'VTI'},
                        {'id': 1, 'ticker': 'IEFA'},
                        {'id': 2, 'ticker': 'IEMG'},
                        {'id': 3, 'ticker': ''}
                    ]
                },
                {
                    'id': 1,
                    'name': 'REITs',
                    'weight': 50,
                    'dual_momentum': true,
                    'duration': 12,
                    'max_holdings': 1,
                    'holdings': [
                        {'id': 0, 'ticker': 'VNQ'},
                        {'id': 1, 'ticker': 'VNQI'},
                        {'id': 2, 'ticker': 'REM'},
                        {'id': 3, 'ticker': ''}
                    ]
                }
            ]
        };
        this.csrftoken = getCookie('csrftoken');
    }

    /**
     * Runs when the MainView item is connected to the server.
     */
    componentDidMount() {
        fetch("api/people/")
            .then((response) => {
                // console.log(response);
                response
                    .json()
                    .then((data) => {
                        this.setState({data});
                        // console.log(data);
                    })
            }).catch(() => {
                console.log("error");
            });
    }



    handle_holding_update(component_id, holding_id, event){
        console.log("update", event.target);
        let dm_components = this.state.dm_components;
        dm_components[component_id]['holdings'][holding_id][event.target.name] = event.target.value;
        this.setState({dm_components: dm_components});
    }

    handle_component_update(component_id, event){
        let dm_components = this.state.dm_components;
        let dm_component = this.state.dm_components[component_id];

        console.log(event.target);
        if (event.target.name === 'dual_momentum'){
            dm_component['dual_momentum'] = !dm_component['dual_momentum']
        } else if (event.target.name === 'weight') {
            dm_components[component_id][event.target.name] = parseFloat(event.target.value);
        } else if (event.target.name === 'duration' || event.target.name === 'max_holdings'){
            dm_components[component_id][event.target.name] = parseInt(event.target.value);
        }
        this.setState({dm_components: dm_components});
    }


    modify_number_of_components(i, component_id){
        // Add or remove components

        let dm_components = this.state.dm_components;

        // add new component
        if (i === 1) {
            if (dm_components.length === 0) { //if no component currently, add new one
                dm_components = [{
                    'id': 0,
                    'name': 'Name',
                    'weight': 50,
                    'duration': 12,
                    'dual_momentum': true,
                    'max_holdings': 1,
                    'holdings': [{'id': 0, 'ticker': ''}]
                }];
            } else {
                dm_components.push({
                    'id': 10,
                    'name': 'Name',
                    'weight': 50,
                    'max_holdings': 1,
                    'dual_momentum': true,
                    'duration': 12,
                    'holdings': [{'id': 0, 'ticker': ''}]
                })
            }

        // remove component
        } else {
            console.log(component_id, dm_components.slice(0, component_id), dm_components.slice(component_id +1));
            dm_components = dm_components.slice(0, component_id).concat(dm_components.slice(component_id +1));
        }

        this.setState({dm_components: dm_components});

    }

    modify_number_of_holdings(i, component_id) {
        let dm_components = this.state.dm_components;

        // add new holding
        if (i === 1) {
            dm_components[component_id]['holdings'].push({
                'id': dm_components[component_id]['holdings'].length,
                'ticker': '', 'percentage': 0
            });
        //remove holding
        } else {
            let holdings = dm_components[component_id]['holdings'];
            if (holdings.length > 0) {

                // if dual momentum mode, remove last holding
                if (dm_components[component_id]['dual_momentum']) {
                    holdings = holdings.slice(0, -1);
                } else { // if buy and hold, remove the only remaining holding
                    holdings = [];
                }
                dm_components[component_id]['holdings'] = holdings;
            } else {
                this.modify_number_of_components(-1, component_id);
                return
            }
        }
        this.setState({dm_components: dm_components});
    }



    render() {
        if (this.state.data) {

            // get total weight allocated (should be 100)
            let total_allocated_weight = 0;
            for (const[_i, component] of this.state.dm_components.entries()){
                total_allocated_weight += component.weight;
            }

            let dm_components = [];
            for (const [component_id, _d] of this.state.dm_components.entries()) {
                dm_components.push(
                    <ComponentSelector
                        key={component_id}
                        config={this.state.dm_components[component_id]}
                        total_allocated_weight={total_allocated_weight}
                        handle_holding_update={(holding_id, event) =>{
                            this.handle_holding_update(component_id, holding_id, event)
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
                    <div className="row">
                        {dm_components}
                        <div className="col-sm-3">
                            <button type="button" className="btn btn-outline-success"
                                onClick={() => this.modify_number_of_components(1)}
                            >Add Category</button>
                        </div>
                    </div>
                </div>
            );
        } else {
            return (
                <div>Loading!</div>
            )
        }
    }
}

// when importing Main what do we get?
export default MainView;
