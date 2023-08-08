import React, { Component } from 'react';
import {CanvasJSChart} from 'canvasjs-react-charts'
import {request} from '../../helpers'
import { useParams } from "react-router";

export class Graph extends Component {
  state = {
    data: null
  }

  componentDidMount() {
    request('/data', 'POST', this.props.queryInfo,
            (data) => this.setState({data: data}),
            (e) => console.log(e)
    )
  }

  render() {
    let options = {
      animationEnabled: true,
      exportEnabled: true,
      theme: "light2", // "light1", "dark1", "dark2"
      title:{
        text: "test"
      },
      // axisY: this.props.yAxisPrimary,
      // axisY2: this.props.yAxisSecondary,
      axisX: {
        title: "Time"
      },
      data: []
    }

    if (this.state.data === null) {
      return (<div>Loading</div>)
    }

    for (var key of Object.keys(this.state.data)) {

      options.data.push({
        type: "line",
        showInLegend: true,
        xValueType: "dateTime",
        name: key,
        dataPoints: this.state.data[key]
      })
    }
    console.log(options)
    
    return (
    <div style={{ marginTop: 20 }}>
      <CanvasJSChart options = {options} 
        /* onRef={ref => this.chart = ref} */
      />
      {/*You can get reference to the chart instance as shown above using onRef. This allows you to access all chart properties and methods*/}
    </div>
    );
  }
}

export const ProbeGraphWrapper = () => {
  let { id } = useParams();
  return (<Graph queryInfo={{probe_ids: [id]}} />)
}

export const ProbeDataGraphWrapper = () => {
  let { id } = useParams();
  return (<Graph queryInfo={{probedata_ids: [id]}} />)
}

export const GraphGraphWrapper = () => {
  let { id } = useParams();
  return (<Graph queryInfo={{graph_id: [id]}} />)
}

export const ZoneGraphWrapper = () => {
  let { id } = useParams();
  return (<Graph queryInfo={{zone_id: [id]}} />)
}

                   