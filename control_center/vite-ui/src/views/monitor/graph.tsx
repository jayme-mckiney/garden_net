import React, { Component } from 'react';
import {CanvasJSChart} from 'canvasjs-react-charts'
import {resolveHost} from '../../helpers'
import { useParams } from "react-router";

export class Graph extends Component {
  state = {
    data: null
  }

  componentDidMount() {
    let host = resolveHost()
    fetch(`http://${host}/data`, {
      method: "POST",
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(this.props.queryInfo),
      mode: 'cors'
    })
    .then((response) => response.json())
    .then((data) => {
      this.setState({data: data})
    })
    .catch((error) => {
      console.log(error)
    })
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
    <div>
      <h1>React Line Chart</h1>
      <CanvasJSChart options = {options} 
        /* onRef={ref => this.chart = ref} */
      />
      {/*You can get reference to the chart instance as shown above using onRef. This allows you to access all chart properties and methods*/}
    </div>
    );
  }
}

export const SimpleGraphWrapper = () => {
  let { id } = useParams();
  return (<Graph queryInfo={{probe_ids: [id]}} />)
}

                   