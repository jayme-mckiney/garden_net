import React, { Component } from 'react';

import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import {get, request, TrashIcon} from '../../helpers'
import { useParams } from "react-router";


export class GraphForm extends Component {
  constructor(props) {
    super(props)
    let newGraph = {
      id: null,
      name: "",
      description: ""
    }
    Object.assign(newGraph, props.graph);
    let graphLines = []
    this.state = {
      graph: newGraph,
      graph_lines: graphLines,
      showModal: false,
      zones: [],
      probes: [],
      probe_datas: [],
      selectedZone: -1,
      selectedProbe:-1,
      selectedProbeData: -1,
      probeDataByID: {}
    }
  }

  componentDidMount() {
    if (this.props.edit === true) {
      get(`graphs/${this.props.id}`,
          (data) => this.setState({graph: data.graph, graph_lines: data.graph_lines}),
          (e) => console.log(e))
    }
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

  handleNameInput = (e) => {
    let graph = {}
    Object.assign(graph, this.state.graph)
    graph.name = e.target.value
    this.setState({graph: graph})
  }
  handleDescInput = (e) => {
    let graph = {}
    Object.assign(graph, this.state.graph)
    graph.description = e.target.value
    this.setState({graph: graph})
  }
  openModal = (e) => {
    this.setState({showModal: true})
  }
  handleClose = (e) => {
    let state_adjustment = {showModal: false, selectedZone: -1, selectedProbe:-1, selectedProbeData: -1}
    if (e && e.target.id == 'save') {
      if (this.state.selectedProbeData == -1) {
        alert('Please select a probe data to represent a line in the graph first')
        state_adjustment = {}
      } else if (this.state.graph_lines.filter(x => x.probedata_id == this.state.selectedProbeData).length) {
        alert("That probe data is already selected for this graph")
        state_adjustment = {}
      } else {
        // save selection
        let new_graph_lines = this.state.graph_lines
        new_graph_lines.push({graph_id: null, probedata_id: this.state.selectedProbeData})
        console.log(new_graph_lines)
        state_adjustment.graph_lines = new_graph_lines
      }
    }
    this.setState(state_adjustment)
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
    this.setState({selectedProbeData: probedata_id})
  }

  removeLine = (probedata_id, e) => {
    let newArray = []
    for ( let graphLine of this.state.graph_lines) {
      if( graphLine.probedata_id != probedata_id) {
        newLine = Object.assign({}, graphLine)
        newArray.push(newLine)
      }
    }
    this.setState({graph_lines: newArray})
  }

  save = (e) => {
    if (this.state.graph_lines.length == 0) {
      let alerts = []
      for(let i in this.state.alerts)
        alerts.push(copy(this.state.alerts[i]))
      alerts.push({type: "warning", message: "Please add a line first"})
      this.setState({alerts: alerts})
      return
    }
    const method = this.props.edit ? "PUT" : "POST"
    const path = this.props.edit ? `graphs/${this.state.graph.id}` : 'graphs'
    let payload = {
      graph: this.state.graph,
      graph_lines: this.state.graph_lines
    }
    request(path,
            method,
            payload,
            (data) => this.setState(),
            (e) => console.log(e))
  }


  render() {
    let submitText = this.props.edit ? "Save" : "Create"
    let cancelButton = null;
    if (this.props.edit === true) {
      cancelButton = <Button onClick={this.props.cancel} type="button">Cancel</Button>
    }
    let alerts = []
    for( let i in this.state.alerts) {
      const type = this.state.alerts[i].type
      const message = this.state.alerts[i].message
      alerts.push(<div class={`alert alert-${type}`} role="alert">{message}</div>)
    }
    let probe_data_form = null
    if(this.state.probe_datas.length > 0) 
      probe_data_form  = this.state.graph_lines.map(gl => <div key={gl.probedata_id} data-value={gl.probedata_id}><TrashIcon onClick={this.removeLine.bind(this, gl.probedata_id)} /> {this.state.probeDataByID[gl.probedata_id].name}</div>)

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
      <div style={{marginTop: 20}}>
        {alerts}
        <Modal show={this.state.showModal} onHide={this.handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>Select a piece of probe data</Modal.Title>
          </Modal.Header>
          <Modal.Body>
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
              <Form.Control as="select" onChange={this.handleSelectProbeData}>
                {probeDataOptions}
              </Form.Control>
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={this.handleClose}>
              Cancel
            </Button>
            <Button id='save' variant="primary" onClick={this.handleClose}>
              Select
            </Button>
          </Modal.Footer>
        </Modal>
        <Form>
          <Form.Group as={Col}>
            <Form.Label>Graph Name</Form.Label>
            <Form.Control name='name' value={this.state.graph.name} onChange={this.handleNameInput} placeholder="My graph" />
          </Form.Group>
          <Form.Group>
            <Form.Label>Description</Form.Label>
            <Form.Control name='description' value={this.state.graph.description} onChange={this.handleDescInput} placeholder="This graph shows whatever" />
          </Form.Group>
          <Form.Group>
            <Form.Label>Graph Lines</Form.Label>
            {probe_data_form}
            <Button onClick={this.openModal} type='button'>Add Graph Line</Button>
          </Form.Group>
          <Button onClick={this.save} type="button">{submitText}</Button>
          {cancelButton}
        </Form>
      </div>
    )
  }
}

export const GraphFormEdit = () => {
  let { id } = useParams();
  return (<GraphForm id={id} edit={true} />)
}
