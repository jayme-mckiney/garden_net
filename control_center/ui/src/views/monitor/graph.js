import React, { Component } from 'react';
import CanvasJSReact from '../../assets/canvasjs.react';
var CanvasJSChart = CanvasJSReact.CanvasJSChart;
 
class Graph extends Component {
  state = {
    data: null
  }

  componentDidMount() {

  }

  render() {
    const options = {
      animationEnabled: true,
      exportEnabled: true,
      theme: "light2", // "light1", "dark1", "dark2"
      title:{
        text: this.props.title
      },
      axisY: yAxisPrimary,
      axisY2: yAxisSecondary,
      axisX: {
        title: "Time"
      },
      data: []
    }
    options[data]
    
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

export default LineChart;                           