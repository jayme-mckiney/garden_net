import React, { Component } from 'react';

import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import {get} from '../../helpers'


export class ProbeDataDrilldown extends Component {
  constructor(props) {
    super()
    this.state = {
      zones: [],
      probes: [],
      probe_datas: [],
      selectedZone: -1,
      selectedProbe: -1
    }
  }

  handleSelectZone = (e) => {
    let zone_id = e.target.value
    this.setState({selectedZone: zone_id})
  }
  handleSelectProbe = (e) => {
    let probe_id = e.target.value
    this.setState({selectedProbe: probe_id})
  }

  handleSelectProbeData = (e) => {
    let probedata_id = e.target.value
    console.log(probedata_id)
    this.props.handleSelect(probedata_id)
  }

  componentDidMount() {
    get(`zones`,
        (data) => this.setState({zones: data.zones}),
        (e) => console.log(e))
    get(`probes`,
        (data) => this.setState({probes: data.probes}),
        (error) => console.log())
    get(`probe_datas`, 
        (data) => {
          let probeDataByID = {}
          for (let i in data.probe_datas) {
            let pd = data.probe_datas[i]
            probeDataByID[pd.id] = pd
          }
          this.setState({probe_datas: data.probe_datas, probeDataByID: probeDataByID})
        }, (error) => console.log(error))
  }

  render() {

    let zoneOptions = this.state.zones.map(z => <option key={z.id} value={z.id}>{z.name}</option>)

    let restrictedProbeList = this.state.probes.filter(p => this.state.selectedZone < 0 || this.state.selectedZone == p.zone_id)
    let probeOptions = restrictedProbeList.map(p => <option key={p.id} value={p.id}>{p.name}</option>)
    let restrictedProbeIDs = restrictedProbeList.map(p => p.id)

    let probeDataRestricter = (pd) => this.state.selectedProbe < 0 || this.state.selectedProbe == pd.probe_id 
    if (this.state.selectedZone != -1 && this.state.selectedProbe == -1) {
      probeDataRestricter = (pd) =>  restrictedProbeIDs.indexOf(pd.probe_id) > -1
    }
    let restrictedProbeDataList = this.state.probe_datas.filter(probeDataRestricter)
    let probeDataOptions = restrictedProbeDataList.map(pd => <option key={pd.id} value={pd.id}>{pd.name}</option>)
    zoneOptions.unshift(<option key={-1} value={-1}>Select</option>)
    probeOptions.unshift(<option key={-1} value={-1}>Select</option>)
    probeDataOptions.unshift(<option key={-1} value={-1}>Select</option>)
    return(
      <Row>
        <Form.Group as={Col}>
          <Form.Label>Zone Filter</Form.Label>
          <Form.Control as="select">
            {zoneOptions}
          </Form.Control>
        </Form.Group>
        <Form.Group as={Col}>
          <Form.Label>Probe Filter</Form.Label>
          <Form.Control as="select" onChange={this.handleSelectProbe}>
            {probeOptions}
          </Form.Control>
        </Form.Group>
        <Form.Group as={Col}>
          <Form.Label>Probe Data Selection</Form.Label>
          <Form.Control as="select" value={this.props.selected} onChange={this.handleSelectProbeData}>
            {probeDataOptions}
          </Form.Control>
        </Form.Group>
      </Row>
    )
  }
}

export default ProbeDataDrilldown