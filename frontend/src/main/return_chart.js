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
            //update if we have new data: Note: this is flimsy. if new data has the same final
            // value, it won't update
            (this.props.data && nextProps.data && (
                nextProps.data[nextProps.data.length - 1].value_end !==
                this.props.data[this.props.data.length - 1].value_end)
            )
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

        for (const bar of this.bars) {
            if (bar.date_start <= date && date <= bar.date_end) {
                this.setState({'tooltip_data': bar});
                break;
            }
        }
    }

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
        console.log("width", this.graph_width);

        this.xScale = d3.scaleTime()
            // margin left and right to avoid cutting off axis labels
            .range([this.margin.left, this.graph_width - this.margin.right])
            .domain(d3.extent(this.props.data, d => d.date_start));

        this.yScale = d3.scaleLog().base(10)
            .range([this.props.height - this.margin.top, this.margin.bottom])
            .domain([
                0.5 * d3.min(this.props.data, d => d.value_start),
                1.5 * d3.max(this.props.data, d => d.value_end)]);

        // update x and y scale with zoom/drag information
        if (this.state.zoomTransform){
            this.xScale.domain(this.state.zoomTransform.rescaleX(this.xScale).domain());
            this.yScale.domain(this.state.zoomTransform.rescaleY(this.yScale).domain());
        }

        this.initialize_bar_paths();

        this.xAxisGenerator = d3.axisBottom().scale(this.xScale)
            .tickFormat(d3.timeFormat('%Y'));

        // to create grid lines, we basically create an empty axis with "ticks" (i.e. the
        // lines connecting the axis to the numbers) that run across the whole chart.
        // the ticks are empty because we don't want to render axis labels for this "axis"
        this.xAxisGridLinesGenerator = d3.axisBottom().scale(this.xScale)
            .tickSize(-this.props.height + this.margin.top + this.margin.bottom)
            .tickFormat('');

        this.yAxisGenerator = d3.axisLeft().scale(this.yScale)
            .tickFormat(d3.format(',.1f'))
            .ticks(2);
        this.yAxisGridLinesGenerator = d3.axisLeft().scale(this.yScale)
            .tickSize(-this.graph_width + this.margin.left + this.margin.right)
            .ticks(2)
            .tickFormat('');
    }


    initialize_bar_paths(){

        // initialize the bars for the chart

        // Step 1: figure out how many months of data to merge into each bar
        const chart_width = this.graph_width - this.margin.left - this.margin.right;
        const data_len = this.props.data.length;
        let number_of_months_to_merge = 1;
        for ( number_of_months_to_merge of [1, 2, 4, 6, 12, 24]){
            this.bar_width = chart_width / data_len * number_of_months_to_merge;
            if (this.state.zoomTransform){
                // zoomTransform essentially stretches how wide the chart is
                this.bar_width *= this.state.zoomTransform.k;
            }
            if (this.bar_width > 5){
                break
            }
        }

        // Step 2: generate bars
        this.bars = [];
        for (let index = 0; index < data_len; index += number_of_months_to_merge){
            const start = this.props.data[index];
            const x = this.xScale(start.date_start);

            // if bar is outside chart area, skip it
            if (x < this.margin.left || x > this.graph_width - this.margin.right){
                continue
            }

            // make sure to limit last value to an existing index
            const end = this.props.data[Math.min(
                index + number_of_months_to_merge - 1, data_len - 1)];
            let y1 = this.yScale(Math.max(start.value_start, end.value_end));
            let y2 = this.yScale(Math.min(start.value_start, end.value_end));

            // if y2 < top margin, the element is invisible
            if (y2 < this.margin.top){
                continue
            }
            // if y1 > chart height, element is invisible
            if (y1 > this.props.height - this.margin.bottom){
                continue
            }


            // limit y1 and y2 to chart area
            y1 = Math.max(this.margin.top, y1);
            y2 = Math.max(this.margin.top, y2);
            y1 = Math.min(this.props.height - this.margin.bottom, y1);
            y2 = Math.min(this.props.height - this.margin.bottom, y2);

            const bar = {
                'x': x, 'y': y1, 'height': Math.max(1, (y2 - y1)),
                'gained_money': end.value_end > start.value_start,
                'value_start': start.value_start, 'value_end': end.value_end,
                'date_start': start.date_start, 'date_end': end.date_end,
                'width': this.bar_width - 2
            };
            this.bars.push(bar);
        }
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
                    >
                        <g>
                            <g>
                                <g ref={this.xAxisGridLinesRef} className={"grid"} />
                                <g ref={this.yAxisGridLinesRef} className={"grid"} />
                            </g>

                            <g>
                                <g ref={this.xAxisRef} />
                                <g ref={this.yAxisRef} />
                            </g>
                        </g>
                        <g className="bars">
                            {
                                this.bars.map((d, idx) => {
                                    return <rect
                                        key={idx}
                                        x={d.x} y={d.y}
                                        width={d.width}
                                        height={d.height}
                                        style={{'fill': d.gained_money ? '#00b061' : '#ff3031'}}
                                    />
                                })
                            }
                        </g>
                        <g id={"crosshairs"}>

                            <line
                                // vertical line
                                x1={ttdata ? ttdata.x + this.bar_width / 2 - 1 : -1000}
                                x2={ttdata ? ttdata.x + this.bar_width / 2 - 1 : -1000}
                                y1={this.margin.top}
                                y2={this.props.height - this.margin.bottom}
                                style={{'stroke': 'black', 'strokeDasharray': '4'}}
                            />

                            <line
                                // horizontal line
                                x1={this.margin.left}
                                x2={this.graph_width - this.margin.right}
                                // y data + height if loss
                                y1={ttdata ?
                                    ttdata.y + (ttdata.gained_money ? 0 : ttdata.height) :
                                    -1000}
                                y2={ttdata ?
                                    ttdata.y + (ttdata.gained_money ? 0 : ttdata.height) :
                                    -1000}
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
                    <ChartTooltip
                        tooltip_data={this.state.tooltip_data}
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

        // on update ?? figure out new zoom state?? still not quite sure what this does...
        d3.select(this.graphSVG.current)
            .call(this.zoom);
    }

}

ReturnsChart.propTypes={
    data: PropTypes.array,
    width: PropTypes.number.isRequired,
    height: PropTypes.number.isRequired
};


class ChartTooltip extends React.Component{
    constructor(props){
        super(props);
    }

    render(){
        if (this.props.tooltip_data){

            const data = this.props.tooltip_data;
            const date_start = data.date_start
                .toLocaleDateString('en-US', {month: 'long', year:'numeric'});

            // period ends on previous month, not current month
            const date_month_to_last = new Date(data.date_end);
            date_month_to_last.setMonth(data.date_end.getMonth() - 1);
            const date_end = date_month_to_last
                .toLocaleDateString('en-US', {month: 'long', year:'numeric'});
            const pl_percent = (((data.value_end / data.value_start) - 1) * 100).toFixed(3) +"%";

            return(
                <div className={'chart_tooltip'}>
                    <table className="table">
                        <tbody>
                            <tr>
                                <td colSpan={2}>{date_start}-{date_end}</td>
                            </tr>
                            <tr>
                                <td>Return</td>
                                <td>{pl_percent}</td>
                            </tr>
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
    tooltip_data: PropTypes.object
};
