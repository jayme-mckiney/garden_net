import React, { Component, createRef } from 'react';
import {request, get} from '../../helpers'
import { useParams } from "react-router";
import './single_readout.css';

export class Readout extends Component {
  constructor(props) {
    super()
    this.interval = createRef()
    this.state = {
      readout_data: null,
      data: null
    }
  }

  componentDidMount() {
    get(`/monitors/${this.props.id}`,
        (data) => {
            this.setState({readout_data: data.monitor})
            this.fetchData(data.monitor.probedata_id)
            this.interval = setInterval(this.fetchData, data.monitor.refresh_interval * 1000, data.monitor.probedata_id)
        },
        (e) => console.log(e)
    )
  }

  componentWillUnmount() {
    clearInterval(this.interval)
  }

  fetchData = (id) => {
    request('/data', 'POST', {probedata_ids: [id], limit: 1},
            (data) => this.setState({data: data[Object.keys(data)[0]][0]['y']}),
            (e) => console.log(e)
    )
  }

  render() {

    if (this.state.data === null) {
      return (<div>Loading</div>)
    }

    const rangeCenter = (this.state.readout_data.tolerable_lower_bound + this.state.readout_data.tolerable_upper_bound) / 2
    const rangeSize = this.state.readout_data.tolerable_upper_bound - this.state.readout_data.tolerable_lower_bound
    const centerDelta = Math.abs(rangeCenter - this.state.data)
    const relativeDelta = centerDelta / (rangeSize /2)
    let redValue = (200 * relativeDelta)
    if(redValue > 255)
      redValue = 255
    let greenValue = 255 - (200 * relativeDelta)
    if(greenValue < 0)
      greenValue = 0
    const color = `rgb(${redValue} ${greenValue} 0)`
    
    return (
    <div className="single-readout-display">
      {this.state.readout_data.name}
      <div className="data" style={{color: color}}>{this.state.data}</div>
    </div>
    );
  }
}

export const ReadoutWrapperParams = () => {
  let { id } = useParams();
  return (<Readout id={id} />)
}