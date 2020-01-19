import React from 'react';
import PropTypes from 'prop-types';

import './return_chart.css'

import * as d3 from 'd3';
window.d3 = d3;





export class ReturnsChart extends React.Component {
    constructor(props){
        super(props);

        this.state = {
            tooltip_data: null,
            zoom_status: 1.5,
            drag_dx : 0,
            zoomTransform: null
            // zoom_center: null
        };

        // the main graph SVG
        this.graphSVG = React.createRef();


        // the data array holding a zoomed version of the data array
        this.zoomedData = null;

        // if true, d3 paths are recalculated
        this.recalculateD3Paths = true;

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

        // margins of the element
        this.margin = {
            'bottom': 30,
            'top': 30,
            'left': 35,
            'right': 30
        };


        this.zoom = d3.zoom()
            .scaleExtent([-5, 5])
            .translateExtent([[-100, -100], [props.width+100, props.height+100]])
            .extent([[-100, -100], [props.width+100, props.height+100]])
            .on("zoom", this.zoomed.bind(this))

    }
    zoomed() {
        // this has elements k, x, y
        console.log("transform", d3.event.transform);
        this.setState({
            zoomTransform: d3.event.transform
        });
    }


    shouldComponentUpdate(nextProps, nextState, nextContext) {
        // in shouldComponentUpdate, figure out if d3 paths need to be recalculated
        // we don't recalculate here because the state is not yet updated (it is in render())

        if (
            // if zoom status changed, update paths during render
            (this.state.zoom_status !== nextState.zoom_status) ||
            // if we have data but no calculated bars yet, update paths during render
            (nextProps.data && !this.bars) ||
            // if drag, re-calculate paths
            (this.state.drag_dx !== nextState.drag_dx)
        ){
            this.recalculateD3Paths = true;
        } else {
            this.recalculateD3Paths = false;
        }

        // we always update the component, this function is here purely to determine if we need
        // to recalculate d3 paths
        return true
    }

    handle_mouse_wheel(e){
        if (e.deltaY > 0){
            // this.setState({'zoom_status': Math.max(1, this.state.zoom_status / 1.5)});
            console.log('zoom out');
        } else {
            console.log('zoom in');
            // this.setState({'zoom_status': Math.min(40, this.state.zoom_status * 1.5)});
        }
    }


    handle_mouseover(e){
        const x = e.pageX - e.target.getBoundingClientRect().x - this.margin.left;

        // figure out what bar we're over
        const bar_width = (this.props.width - this.margin.left-this.margin.right) / this.bars.length;
        const bar_id = Math.floor(x / bar_width);
        this.setState({tooltip_data: this.bars[bar_id]})
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

        this.zoomedData = this.props.data.slice();
        if (this.state.zoom_status > 1){
            const no_data_elements = parseInt(this.zoomedData.length / this.state.zoom_status);

            // if we need to move from orig_data_len to zoomed_data_len, the first element will
            // be at (orig_len - zoomed_len)/2, i.e. we cut half from the beginning and half
            // from the end
            let first_idx = parseInt((this.zoomedData.length - no_data_elements) / 2);

            // next, we calculate the drag offset
            const graph_width = this.props.width - this.margin.left - this.margin.right;
            const width_per_datum = graph_width / this.zoomedData.length;

            // take drag_dx (pixels) and calculate how many data rows to offset
            let drag_offset = this.state.drag_dx / width_per_datum;
            // then take the zoom status into consideration, i.e. the more zoom, the smaller
            // the drag offset
            drag_offset /= this.state.zoom_status;

            console.log("drag offset", this.state.drag_dx, drag_offset);

            first_idx -= drag_offset;
            first_idx = Math.max(0, first_idx);

            this.zoomedData = this.zoomedData.slice(first_idx, first_idx + no_data_elements);
        }

        const xScale = d3.scaleTime()
            // margin left and right to avoid cutting off axis labels
            .range([this.margin.left, this.props.width - this.margin.right])
            .domain(d3.extent(this.zoomedData, d => d.date_start));

        const yScale = d3.scaleLog().base(10)
            .range([this.props.height - this.margin.top, this.margin.bottom])
            .domain([
                0.5 * d3.min(this.zoomedData, d => d.value_start),
                1.5 * d3.max(this.zoomedData, d => d.value_end)]);

        this.initialize_bar_paths(xScale, yScale);

        this.xAxisGenerator = d3.axisBottom().scale(xScale)
            .tickFormat(d3.timeFormat('%Y'));

        // to create grid lines, we basically create an empty axis with "ticks" (i.e. the
        // lines connecting the axis to the numbers) that run across the whole chart.
        // the ticks are empty because we don't want to render axis labels for this "axis"
        this.xAxisGridLinesGenerator = d3.axisBottom().scale(xScale)
            .tickSize(-this.props.height + this.margin.top + this.margin.bottom)
            .tickFormat('');

        this.yAxisGenerator = d3.axisLeft().scale(yScale)
            .tickFormat(d3.format(',.1f'))
            .ticks(2);
        this.yAxisGridLinesGenerator = d3.axisLeft().scale(yScale)
            .tickSize(-this.props.width + this.margin.left + this.margin.right)
            .ticks(2)
            .tickFormat('');
    }


    initialize_bar_paths(xScale, yScale){
        // initialize the bars for the chart

        const chart_width = this.props.width - this.margin.left - this.margin.right;
        const data_len = this.zoomedData.length;
        let number_of_months_to_merge = 1;
        let bar_width;
        for ( number_of_months_to_merge in [1, 2, 3, 4, 6, 12, 24]){
            // why on earth is number_of... a string here rather than an int???
            number_of_months_to_merge = parseInt(number_of_months_to_merge);
            bar_width = chart_width / data_len * number_of_months_to_merge;
            if (bar_width > 5){
                break
            }
        }

        this.bars = [];
        for (let index = 0; index < data_len; index += number_of_months_to_merge){
            const start = this.zoomedData[index];
            // make sure to limit last value to an existing index
            const end = this.zoomedData[Math.min(
                index + number_of_months_to_merge - 1, data_len - 1)];
            const y1 = yScale(d3.max([start.value_start, end.value_end]));
            const y2 = yScale(d3.min([start.value_start, end.value_end]));
            const bar = {
                'x': xScale(start.date_start), 'y': y1, 'height': Math.max(1, (y2 - y1)),
                'gained_money': end.value_end > start.value_start,
                'value_start': start.value_start, 'value_end': end.value_end,
                'date_start': start.date_start, 'date_end': end.date_end
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
                        width={this.props.width}
                        height={this.props.height}
                        onMouseMove={(e) => this.handle_mouseover(e)}
                        onWheel={(e) => this.handle_mouse_wheel(e)}
                        zoomTransform={this.state.zoomTransform}
                        zoomType="scale"
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
                                        width={(this.props.width / this.bars.length) - 2}
                                        height={d.height}
                                        style={{'fill': d.gained_money ? '#00b061' : '#ff3031'}}
                                    />
                                })
                            }
                        </g>
                        <g id={"crosshairs"}>
                            <line
                                // x data + half of the bar width
                                x1={ttdata ? ttdata.x + (this.props.width / this.bars.length) / 2 - 1 : -1000}
                                x2={ttdata ? ttdata.x + (this.props.width / this.bars.length) / 2 - 1 : -1000}
                                y1={this.margin.top}
                                y2={this.props.height - this.margin.bottom}
                                style={{'stroke': 'black', 'strokeDasharray': '4'}}
                            />
                            <line
                                x1={this.margin.left}
                                x2={this.props.width - this.margin.right}
                                // y data + height if loss
                                y1={ttdata ? ttdata.y + (ttdata.gained_money ? 0 : ttdata.height) : -1000}
                                y2={ttdata ? ttdata.y + (ttdata.gained_money ? 0 : ttdata.height) : -1000}
                                style={{'stroke': 'black', 'strokeDasharray': '4'}}
                            />
                        </g>

                        {/*My idea was to create a transparent rect that acts as the target for */}
                        {/*mousemove. Before, moving the mouse over bars made the crosshairs */}
                        {/*disappear. My idea was to bind mousemove to the top element, i.e. this rect.*/}
                        {/*However, after adding this rect all of the mousemove actions triggered*/}
                        {/*properly w/o having been bound to this rect. Not sure why...*/}
                        <rect id={"chart_mouseover_target"}
                            width={this.props.width} height={this.props.height}
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


        d3.select(this.graphSVG.current)
            .call(this.zoom);

        // bind event handlers for nodes
        d3.select(this.graphSVG.current)
            .call(
                d3.drag()
                    .on("start", (e) => {
                        console.log("start", e);
                    })
                    .on("drag", (e) => {
                        if (d3.event.dx !== 0 ){
                            this.setState({'drag_dx': this.state.drag_dx + d3.event.dx})
                        }



                        // d.x = d3.event.x;
                        // d.y = d3.event.y;
                        // render_simulation(config, data, data_bindings);
                    })
                    .on("end", (e) => {
                        console.log("end", e);
                        // d.x = d3.event.x;
                        // d.y = d3.event.y;
                        // render_simulation(config, data, data_bindings);
                        // data_bindings.nodes
                        //     .on("mouseover", (d) => handle_viz_events('mouseover', d))
                        //     .on("mouseout", (d) => handle_viz_events('mouseout', d))
                    })
            );
    }

}

ReturnsChart.propTypes={
    data: PropTypes.array.isRequired,
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
