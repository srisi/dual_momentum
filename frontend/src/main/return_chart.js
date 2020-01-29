// for good d3 react zoom example, see
// https://swizec.com/blog/two-ways-build-zoomable-dataviz-component-d3-zoom-react/swizec/7753

import React from 'react';
import PropTypes, {node} from 'prop-types';

import './return_chart.css'

import * as d3 from 'd3';
window.d3 = d3;


export class ReturnsChart extends React.Component {
    constructor(props){
        super(props);

        this.state = {
            tooltip_data: null,
            highlighted_idx: undefined,
            zoomTransform: null,
        };


        // the main graph SVG
        this.graphSVG = React.createRef();
        this.graph_width = 800;
        //     document.getElementById('components_row').clientWidth);
        // document.getElementById('chart_row').clientWidth);

        // if true, d3 paths are recalculated
        this.recalculateD3Paths = true;

        this.xScale = null;
        this.yScale = null;

        // reference to the xAxis group and d3 xAxis generator
        this.xAxisRef = React.createRef();
        this.xAxisGenerator = null;

        // refernce to xAxisGrid group and generator (grid works like an axis)
        this.xAxisGridLinesRef = React.createRef();
        this.xAxisGridLinesGenerator = null;

        // same for y axis
        this.yAxisRef = React.createRef();
        this.yAxisGenerator = null;
        this.yAxisGridLinesRef = React.createRef();
        this.yAxisGridLinesGenerator = null;

        // the actual bars to render for the barchart (often, multiple months of data are
        // aggregated into one bar
        this.bars = null;
        // multiple functions calculate the width of the bar -> better to just store it here
        this.bar_width = null;

        this.lineGenerator = d3.line();
        this.returns_line = null;
        this.sp500_line = null;

        this.returnsLineRef = React.createRef();
        this.sp500LineRef = React.createRef();

        // margins of the element
        this.margin = {
            'bottom': 30,
            'top': 30,
            'left': 35,
            'right': 30
        };

        this.zoom = d3.zoom()
            // extent of the zoom (10% to 800%)
            .scaleExtent([1, 8])
            // limit dragging to areas with datapoints
            .translateExtent([[-100, -100], [this.graph_width + 100, this.props.height+100]])
            .extent([[-100, -100], [this.graph_width + 100, this.props.height + 100]])
            .on("zoom", this.zoomed.bind(this));
    }
    zoomed() {
        this.setState({
            zoomTransform: d3.event.transform
        });
    }


    shouldComponentUpdate(nextProps, nextState, nextContext) {
        // in shouldComponentUpdate, figure out if d3 paths need to be recalculated
        // we don't recalculate here because the state is not yet updated (it is in render())

        if (
            // if zoom status changed, update paths during render
            (this.state.zoomTransform !== nextState.zoomTransform) ||
            // if we have data but no calculated bars yet, update paths during render
            (nextProps.data && !this.bars) ||
            // if the dual momentum config has changed (indicated by hash) -> update
            (this.props.config_hash === nextProps.config_hash)
        ){
            this.recalculateD3Paths = true;
        } else {
            this.recalculateD3Paths = false;
        }

        // we always update the component, this function is here purely to determine if we need
        // to recalculate d3 paths
        return true
    }

    handle_mouseover(e) {
        // on mouseover, figure out which bar to display data from in the tooltip
        // the same bar is at the center of the crosshairs
        const x = e.pageX - e.target.getBoundingClientRect().x;
        const date = this.xScale.invert(x);

        let highlighted_idx = null;
        for (const [idx, month] of this.props.data.monthly_data.entries()){
            if (month.date_start <= date && date <= month.date_end){
                highlighted_idx = idx;
                month.x = this.xScale(month.date_end);
                month.x = Math.max(month.x, this.margin.left);
                month.x = Math.min(month.x, this.graph_width - this.margin.left);
                month.y = this.yScale(month.value_end);
                month.y = Math.min(month.y, this.props.height - this.margin.top);
                month.y = Math.max(month.y, this.margin.top);

                this.setState({'tooltip_data': month, highlighted_idx: highlighted_idx});
            }
        }
    }

    handle_mouseout(){
        this.setState({tooltip_data: null, highlighted_idx: undefined})}

    calculate_paths_with_d3(){

        // before rendering, use D3 to calculate the things that we will render with react and
        // store them as local variables. In this case, that includes the bars in the charts.
        // in addition, we are initializing the axes and bind them to local variables.
        // we do this in shouldComponentUpdate because that allows us to calculate the paths
        // that we need in the render function
        // (I suppose we could also do the calculations in the render function but that clog up
        // that code)
        // importantly, the bars are not stored in the state because then we'd have to set the
        // state with the newly calculated bars, triggering an infinite update cycle (each update
        // leads to recalculation of the bars)

        this.graph_width = Math.max(
            document.getElementById('components_row').clientWidth,
            document.getElementById('chart_row').clientWidth);

        this.xScale = d3.scaleTime()
            // margin left and right to avoid cutting off axis labels
            .range([this.margin.left, this.graph_width - this.margin.right])
            .domain(d3.extent(this.props.data.monthly_data, d => d.date_start));

        this.yScale = d3.scaleLog().base(10)
            .range([this.props.height - this.margin.top, this.margin.bottom])
            .domain([
                0.5 * d3.min(this.props.data.monthly_data, d => d.value_start),
                1.5 * d3.max(this.props.data.monthly_data, d => d.value_end)]);

        // update x and y scale with zoom/drag information
        if (this.state.zoomTransform){
            this.xScale.domain(this.state.zoomTransform.rescaleX(this.xScale).domain());
            this.yScale.domain(this.state.zoomTransform.rescaleY(this.yScale).domain());
        }

        // get line generators for returns and benchmark
        this.returns_line_generator = this.get_line_generator('value_end');
        this.sp500_line_generator = this.get_line_generator('value_end_spy_pretax');

        this.xAxisGenerator = d3.axisBottom().scale(this.xScale)
            .tickFormat(d3.timeFormat('%Y'));

        // to create grid lines, we basically create an empty axis with "ticks" (i.e. the
        // lines connecting the axis to the numbers) that run across the whole chart.
        // the ticks are empty because we don't want to render axis labels for this "axis"
        this.xAxisGridLinesGenerator = d3.axisBottom().scale(this.xScale)
            .tickSize(-this.props.height + this.margin.top + this.margin.bottom)
            .tickFormat('');

        this.yAxisGenerator = d3.axisLeft().scale(this.yScale)
            .tickFormat(d3.format(',.0f'))
            .ticks(2);
        this.yAxisGridLinesGenerator = d3.axisLeft().scale(this.yScale)
            .tickSize(-this.graph_width + this.margin.left + this.margin.right)
            .ticks(2)
            .tickFormat('');
    }

    get_line_generator(return_field_name){
        return d3.line()
            .x(d => this.xScale(d.date_end))
            .y(d => this.yScale(d[return_field_name]))

            // defined can be used for clipping but it is choppy
            .defined(d => {
                const x = this.xScale(d.date_end);
                const y = this.yScale(d[return_field_name]);
                return (
                    (x < this.graph_width - this.margin.right) &&
                    (x > this.margin.left) &&
                    (y < this.props.height - this.margin.top) &&
                    (y > this.margin.bottom)
                )
            })
    }

    render() {
        if (!this.props.data) {
            return (<div/>);
        } else {

            if (this.recalculateD3Paths) {
                this.calculate_paths_with_d3();
            }

            const ttdata = this.state.tooltip_data;


            return (
                <>
                    <svg ref={this.graphSVG}
                        width={this.graph_width}
                        // width={800}
                        height={this.props.height}
                        onMouseMove={(e) => this.handle_mouseover(e)}
                        onMouseOut={() => this.handle_mouseout()}
                    >
                        <g>
                            <g ref={this.xAxisGridLinesRef} className={"grid"} />
                            <g ref={this.yAxisGridLinesRef} className={"grid"} />
                        </g>
                        <g>
                            {/*<path className={"benchmark_line"} d={this.sp500_line}*/}
                            {/*    stroke={d3.schemeCategory10[1]}/>*/}
                            {/*<path className={"return_line"} d={this.returns_line}*/}
                            {/*    stroke={d3.schemeCategory10[0]}/>*/}
                            <path ref={this.sp500LineRef} className={"benchmark_line"}
                                stroke="#ff7f0e"/>
                            <path ref={this.returnsLineRef} className={"return_line"}
                                stroke="#1f77b4"/>
                        </g>
                        <g>
                            <g ref={this.xAxisRef} />
                            <g ref={this.yAxisRef} />
                        </g>

                        <g id={"crosshairs"}>

                            <line
                                // vertical line
                                x1={ttdata ? ttdata.x : -1000}
                                x2={ttdata ? ttdata.x : -1000}
                                y1={this.margin.top}
                                y2={this.props.height - this.margin.bottom}
                                style={{'stroke': 'black', 'strokeDasharray': '4'}}
                            />

                            <line
                                // horizontal line
                                x1={this.margin.left}
                                x2={this.graph_width - this.margin.right}
                                // y data + height if loss
                                y1={ttdata ? ttdata.y : -1000}
                                y2={ttdata ? ttdata.y : -1000}
                                style={{'stroke': 'black', 'strokeDasharray': '4'}}
                            />
                        </g>

                        {/*My idea was to create a transparent rect that acts as the target for */}
                        {/*mousemove. Before, moving the mouse over bars made the crosshairs */}
                        {/*disappear. My idea was to bind mousemove to the top element,this rect.*/}
                        {/*However, after adding this rect all of the mousemove actions triggered*/}
                        {/*properly w/o having been bound to this rect. Not sure why...*/}
                        <rect id={"chart_mouseover_target"}
                            width={this.graph_width} height={this.props.height}
                            style={{'fill': '#21252900'}}
                        />
                    </svg>
                    <ChartTickerTooltips
                        // if one month is highlighted, select data from that month. Otherwise
                        // select the last month
                        data={this.props.data.monthly_data[
                            this.state.highlighted_idx ?
                                this.state.highlighted_idx :
                                this.props.data.monthly_data.length - 1
                        ]}
                    />
                    <ChartTooltip
                        tooltip_data={this.state.tooltip_data}
                        // highlighted_idx={this.state.highlighted_idx}
                    />
                </>
            )

        }
    }


    componentDidUpdate() {

        // componentDidUpdate fires AFTER render() in an update cycle
        // this means that we have access to the rendered but empty xAxisRef group and can fill
        // it with d3
        d3.select(this.xAxisRef.current)
            .call(this.xAxisGenerator)
            // place at the bottom of the chart
            .attr('transform', `translate(0, ${this.props.height - this.margin.bottom})`);

        d3.select(this.xAxisGridLinesRef.current)
            .call(this.xAxisGridLinesGenerator)
            .attr('transform', `translate(0, ${this.props.height - this.margin.bottom})`);


        d3.select(this.yAxisRef.current)
            .call(this.yAxisGenerator)
            .attr('transform', `translate(${this.margin.left}, 0)`);

        d3.select(this.yAxisGridLinesRef.current)
            .call(this.yAxisGridLinesGenerator)
            .attr('transform', `translate(${this.margin.left}, 0)`);

        // this.sp500_line = this.lineGenerator(this.props.data.monthly_data);

        // path.datum(data).attr("d", line);
        d3.select(this.returnsLineRef.current)
            .datum(this.props.data.monthly_data)
            .attr("d", this.returns_line_generator);

        d3.select(this.sp500LineRef.current)
            .datum(this.props.data.monthly_data)
            .attr("d", this.sp500_line_generator);

        // on update ?? figure out new zoom state?? still not quite sure what this does...
        d3.select(this.graphSVG.current)
            .call(this.zoom);
    }

}

ReturnsChart.propTypes={
    data: PropTypes.object,
    data_load_error: PropTypes.string,
    config_hash: PropTypes.string,
    width: PropTypes.number.isRequired,
    height: PropTypes.number.isRequired
};


class ChartTickerTooltips extends React.Component{
    constructor(props) {
        super(props);
    }

    render(){
        if(this.props.data) {
            return (
                <div id={"ticker_boxes"}>
                    <div id={"strategy_box"} className={"ticker_box"}>
                        <div>Strategy</div>
                        <div className={"ticker_box_value_div"}>
                            {(this.props.data.value_end * 100).toFixed(0) + "%"}
                        </div>
                    </div>
                    <div id={"benchmark_box"} className={"ticker_box"}>
                        <div>S&P 500</div>
                        <div className={"ticker_box_value_div"}>
                            {(this.props.data.value_end_spy_pretax * 100).toFixed(0) + "%"}
                        </div>
                    </div>
                </div>
            )
        } else {
            return <div/>
        }
    }
}
ChartTickerTooltips.propTypes = {
    data: PropTypes.object,
};


class ChartTooltip extends React.Component{
    constructor(props){
        super(props);
    }

    render(){
        if (this.props.tooltip_data){

            const data = this.props.tooltip_data;
            const date_start = data.date_start
                .toLocaleDateString('en-US', {month: 'short', year:'numeric'});

            // // period ends on previous month, not current month
            // const date_month_to_last = new Date(data.date_end);
            // date_month_to_last.setMonth(data.date_end.getMonth() - 1);
            // const date_end = date_month_to_last
            //     .toLocaleDateString('en-US', {month: 'long', year:'numeric'});
            const pl_percent = (((data.value_end / data.value_start) - 1) * 100).toFixed(3) +"%";

            let holdings = [];
            for (const holding of this.props.tooltip_data.holdings){
                holdings.push(
                    <tr key={holding.name}>
                        <td>{holding.holdings}</td>
                        <td className={"returns_col"}>
                            {((holding.pretax - 1) * 100).toFixed(3) + "%"}
                        </td>
                    </tr>)
            }

            return(
                <div className={'chart_tooltip'}>
                    <table className="table">
                        <tbody>
                            <tr>
                                <td colSpan={2}>{date_start}</td>
                            </tr>
                            <tr>
                                <td>Return</td>
                                <td className={"returns_col"}>{pl_percent}</td>
                            </tr>
                            {holdings}
                        </tbody>
                    </table>

                </div>
            )
        } else {
            return(
                <div/>
            )
        }
    }
}
ChartTooltip.propTypes = {
    tooltip_data: PropTypes.object,
    // highlighted_idx: PropTypes.number
};
