import {Autocomplete} from "@material-ui/lab";
import {TextField} from "@material-ui/core";
import React from "react";

import './autocomplete.css'
import {ticker_configs} from "./ticker_configs";


import PropTypes from 'prop-types';


export class AutoCompleteField extends React.Component {

    constructor(props){
        super(props);
        //unpack ticker data and only retain those that should be suggested in search
        this.search_options = [];           // array of options to display
        this.display_name_to_ticker = {};   // map from displayed name to actual ticker
        this.ticker_to_display_name = {};   // map from ticker to display name

        for (const d of Object.entries(ticker_configs)) {
            const ticker = d[0];
            const config = d[1];
            if (config.suggest_in_search){
                const display_name = `${config.name} (${ticker})`;
                this.search_options.push({
                    'ticker': ticker,
                    'name': config.name,
                    'category': config.tax_category,
                    'display_name': display_name
                });
                this.display_name_to_ticker [display_name] = ticker;
                this.ticker_to_display_name[ticker] = display_name;
            }
        }

        // sort by category and ticker
        this.search_options.sort(function (a, b) {
            if (a.category > b.category) return 1;
            if (a.category < b.category) return -1;
            if (a.ticker > b.ticker) return 1;
            if (a.ticker < b.ticker) return -1;
        });
    }

    sanitize_input_and_handle_update(reason, value) {

        console.log("sanitize", reason, value);

        // on input, update values
        if (reason === 'input'){
            this.props.handle_holding_update(value);


        // clear gets triggered when the user clicks the clear button -> empty field
        } else if (reason === 'clear') {
            this.props.handle_holding_update('');

        // reset gets triggered on re-renders or when a ticker has been selected from the
        //dropdown
        } else if (reason === 'reset') {
            const ticker = this.display_name_to_ticker[value];
            if (ticker !== undefined) {
                console.log("ticker", ticker);
                this.props.handle_holding_update(ticker);
            }
        }
    }


    render(){
        return(

            <Autocomplete
                // allow options outside of suggestions, e.g. stocks not in list
                freeSolo

                // what options to display
                options={this.search_options}

                // group options by category
                groupBy={option => option.category}

                // in selection dropdown, display as 2 spans for vertical alignment
                renderOption={option => (
                    <React.Fragment>
                        <span className="ticker_span">{option.ticker}</span>
                        <span>{option.name}</span>
                    </React.Fragment>
                )}

                // what to display once an option has been selected. Has to be a
                // string because it's an input field
                getOptionLabel={option => option.display_name}

                // the initial input
                inputValue={
                    (this.props.ticker in this.ticker_to_display_name) ?
                        this.ticker_to_display_name[this.props.ticker] :
                        this.props.ticker
                }

                // clear when user presses Escape
                // clearOnEscape={true}

                // what classes to apply to the different html entitites created by
                // autocomplete (see https://material-ui.com/api/autocomplete/)
                classes={{
                    root: "ticker_selector_root",
                    inputRoot: "ticker_selector_inputroot",
                    input: "ticker_selector_input",
                    popper: "ticker_selector_popper"
                }}
                onInputChange={(event, value, reason) => {
                    console.log(event);
                    console.log(value, reason);
                    this.sanitize_input_and_handle_update(reason, value);
                }}
                renderInput={params => (
                    <TextField
                        {...params}
                        margin="none"
                        variant="filled"
                        type="text"
                        size="small"
                        inputProps={{
                            ...params.inputProps,
                            autoComplete: 'new-password', // disable autocomplete and autofill
                        }}
                    />)}
                // PopperComponent={{
                //     keepMounted:true
                // }}
            />

        // <Autocomplete
        //     id="free-solo-demo"
        //     freeSolo={true}
        //     // options={Object.keys(this.state.ticker_configs)}
        //     options={Object.keys(ticker_configs)}
        //     // options={this.state.ticker_configs.map(option => option.name)}
        //     renderInput={params => (
        //         <TextField {...params}
        //             placeholder="Type a name here"
        //             margin="normal"
        //             variant="outlined" fullWidth
        //             value={this.state.cur_value}
        //             onChange={(e) => this.update_searchbar_value(e.target.value)}
        //         />
        //     )}
        //     inputValue={'VTI'}
        //     autoComplete={true}
        //     forcePopupIcon={false}
        //     // onChange={(_event, value) => this.props.update_searchbar_value(value)}
        //     onInputChange={(_event, value, reason) =>
        //         // this.autocomplete_change(value, reason)
        //         console.log(value, reason)
        //     }
        // />

        )
    }
}
AutoCompleteField.propTypes = {
    ticker: PropTypes.string.isRequired,
    handle_holding_update: PropTypes.func.isRequired
};

