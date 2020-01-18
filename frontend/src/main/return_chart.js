import React from 'react';
import PropTypes from 'prop-types';

import * as d3 from 'd3';
window.d3 = d3;
export class ReturnsChart extends React.Component {
    constructor(props){
        super(props);
        this.xAxisRef = React.createRef();
        this.xAxisGenerator = null;
        this.yAxisRef = React.createRef();
        this.yAxisGenerator = null;
        this.bars = null;
        this.margin = {
            'bottom': 30,
            'top': 30,
            'left': 30,
            'right': 30
        }
    }

    shouldComponentUpdate(nextProps, nextState, nextContext) {

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

        if (nextProps.data) {
            const xScale = d3.scaleTime()
                .range([0, nextProps.width])
                // .range([this.margin.left, nextProps.width - this.margin.right])
                .domain([])
                .domain(d3.extent(nextProps.data, d => d.date));
            const yScale = d3.scaleLog().base(10)
                .range([nextProps.height - this.margin.top, this.margin.bottom])
                .domain([0.1, d3.max(nextProps.data, d => d.value_end)]);
            this.bars = nextProps.data.map(d => {
                const y1 = yScale(d3.max([d.value_start, d.value_end]));
                const y2 = yScale(d3.min([d.value_start, d.value_end]));
                return {
                    x: xScale(d.date),
                    y: y1, height: (y2 - y1),
                    gained_money: d.value_end > d.value_start
                }
            });
            this.xAxisGenerator = d3.axisBottom().scale(xScale)
                .tickFormat(d3.timeFormat('%Y'));
            this.yAxisGenerator = d3.axisLeft().scale(yScale);

            console.log("bars", this.bars);

        }
        return true;
    }

    render() {
        if (!this.props.data) {
            return (<div></div>);
        } else {
            return (
                <svg width={this.props.width} height={this.props.height}>
                    <g>
                        <g>
                            <g ref={this.xAxisRef}></g>
                            <g ref={this.yAxisRef}></g>
                        </g>
                    </g>
                    <g className="bars">
                        {
                            this.bars.map((d, idx) => {
                                return <rect
                                    key={idx}
                                    x={d.x} y={d.y}
                                    width='2' height={d.height}
                                    style={{'fill': d.gained_money ? 'green' : 'red'}}
                                />
                            })
                        }
                    </g>
                </svg>
            )

        }
    }


    componentDidUpdate() {

        // componentDidUpdate fires AFTER render() in an update cycle
        // this means that we have access to the rendered but empty xAxisRef group and can fill
        // it with d3
        d3.select(this.xAxisRef.current)
            .call(this.xAxisGenerator)
            .attr('transform', `translate(0, ${this.props.height - this.margin.bottom})`);
        // .attr('transform', `translate(${this.margin.left},
        //        ${this.props.width-this.margin.right})`);

        d3.select(this.yAxisRef.current)
            .call(this.yAxisGenerator)
            // .attr('transform', `translate(${this.margin.left}, 0)`);


    }

}

ReturnsChart.propTypes={
    data: PropTypes.array.isRequired,
    width: PropTypes.number.isRequired,
    height: PropTypes.number.isRequired
};
