/**
 * UI Code for the visualization
 */
import React from 'react';
import PropTypes from 'prop-types';

import { getCookie } from '../common'
import { create_graph, update_graph_color } from './graph.js'
import './main.css';


/***************************************************************************************************
 * Controls and settings components for the visualization
 **************************************************************************************************/
class Controls extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const checked = this.props.config.color === 'blue';
        return (
            <div className="col-3">
                <input
                    type="checkbox"
                    checked={checked}
                    onChange={this.props.handle_checkbox}
                />
                <label>Color is blue</label>
            </div>
        );

    }
}
Controls.propTypes = {
    config: PropTypes.object.isRequired,
    handle_checkbox: PropTypes.func.isRequired,
};


/***************************************************************************************************
 * Wrapper for the Visualization
 **************************************************************************************************/
class Viz extends React.Component {
    constructor(props) {
        super(props);
        this._graphRoot = React.createRef();
    }

    componentDidMount() {
        // D3 Code to create the chart
        create_graph(
            this._graphRoot.current,  // current gives the DOM object (as opposed to the React ref)
            this.props.data,
            this.props.config,
            this.props.handle_viz_events,
        );
    }

    componentDidUpdate() {
        // D3 Code to update the chart
        if (this.props.config.viz_update_func === 'update_graph_color') {
            update_graph_color(
                this._graphRoot.current,
                this.props.data,
                this.props.config,
            );
        }
    }

    render() {
        return (
            <div className="col-6" ref={this._graphRoot}>

            </div>
        )
    }
}
Viz.propTypes = {
    data: PropTypes.arrayOf(PropTypes.object).isRequired,
    config: PropTypes.object.isRequired,
    handle_viz_events: PropTypes.func,
};

/**
 * Info panel - data from the visualization
 */
class Info extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="col-3">
                <p>Your mouse is {this.props.mouseover ? 'OVER' : 'NOT OVER'}  a bar on the viz!</p>
                <p>The current viz color is {this.props.currentColor}</p>
            </div>
        );
    }
}
Info.propTypes ={
    mouseover: PropTypes.bool,
    currentColor: PropTypes.string,
};

class ComponentSelector extends React.Component {
    constructor(props){
        super(props);
    }

    render(){
        let holding_boxes = [];
        for (const [_i, holding] of this.props.config.holdings.entries()) {
            holding_boxes.push(
                <HoldingBox
                    key={holding.ticker}
                    holding={holding}
                    handle_component_update={(percentage) =>
                        this.props.handle_component_update(holding.id, percentage)
                    }
                />
            );
        }
        return (
            <div>
                <h2>{this.props.config.name}</h2>
                <table>
                    <tbody>
                        {holding_boxes}
                    </tbody>
                </table>
            </div>
        )
    }
}
ComponentSelector.propTypes={
    config: PropTypes.object,
    handle_component_update: PropTypes.func
};

class HoldingBox extends React.Component {
    constructor(props){
        super(props);
    }

    render(){
        return (
            <tr>
                <td>
                    <input type="text" name="ticker" maxLength="6" size="6"
                        value={this.props.holding.ticker}
                        onChange={(e) => this.props.handle_component_update(e)}
                    />
                </td>
                <td>{this.props.holding.name}</td>
                <td>

                    <input
                        type="number" name="percentage" min="0" max="100"
                        value={this.props.holding.percentage}
                        onChange={(e) => this.props.handle_component_update(e)}
                    />
                </td>
            </tr>
        )
    }
}
HoldingBox.propTypes={
    holding: PropTypes.object,
    handle_component_update: PropTypes.func
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
            components: [
                {
                    'id': 0,
                    'name': 'Equities',
                    'holdings': [
                        {'id': 0, 'ticker': 'VTI', 'name': 'U.S. Stock Market', 'percentage': 20}
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

    /**
     * Calls when checkbox is changed.  Changes the color from blue to red or vice versa.
     */
    handle_checkbox() {
        // "..." is the 'spread' operator - this is a copy
        const config = {...this.state.config};
        if (config.color === 'blue') {
            config.color = 'red';
        } else {
            config.color = 'blue'
        }
        config.viz_update_func = 'update_graph_color';
        this.setState({
            config: config,
        })
    }

    /**
     * Handles a visualization event
     *
     * @param event_name: String
     */
    handle_viz_events(event_name) {
        if (event_name === "mouseover") {
            this.setState({mouseover: true});
        } else if (event_name === "mouseout") {
            this.setState({mouseover: false});
        }
    }

    update_components(component_id, holding_id, event){
        console.log("update", event.target);
        let components = this.state.components;
        components[component_id]['holdings'][holding_id][event.target.name] = event.target.value;
        this.setState({components: components});
        console.log(this.state.components[0]['holdings'][0])
    }



    /**
     * Render the app on the page
     *
     * @returns {Node}
     */
    render() {
        if (this.state.data) {
            return (

                <div className="container">
                    <div className="row">
                        <Controls
                            handle_checkbox={() => this.handle_checkbox()}
                            config={this.state.config}
                        />
                        <Viz
                            data={this.state.data}
                            config={this.state.config}
                            handle_viz_events={(event_name) => this.handle_viz_events(event_name)}
                        />
                        <Info
                            mouseover={this.state.mouseover}
                            currentColor={this.state.config.color}
                        />
                    </div>

                    <div className="row">
                        <ComponentSelector
                            config={this.state.components[0]}
                            handle_component_update={(holding_id, event) =>{
                                this.update_components(0, holding_id, event)
                            }}
                        />
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
