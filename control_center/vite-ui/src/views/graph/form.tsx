import React, { Component } from 'react';

import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import {resolveHost} from '../../helpers'

class GraphForm extends Component {
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
    let host = resolveHost()
    if (this.props.edit === true) {
      fetch(`http://${host}/graph/${this.props.id}`, {
        method: "get",
        mode: 'cors'
      })
      .then((response) => response.json())
      .then((data) => {
        this.setState({graph: data.graph, graph_lines: data.graph_lines})
        console.log(data)
      })
      .catch((error) => {
        console.log(error)
      })
    }
    fetch(`http://${host}/zones`, {
        method: "get",
        mode: 'cors'
      })
      .then((response) => response.json())
      .then((data) => {
        this.setState({zones: data.zones})
      })
      .catch((error) => {
        console.log(error)
    })
    fetch(`http://${host}/probes`, {
        method: "get",
        mode: 'cors'
      })
      .then((response) => response.json())
      .then((data) => {
        this.setState({probes: data.probes})
      })
      .catch((error) => {
        console.log(error)
    })
    fetch(`http://${host}/probe_datas`, {
        method: "get",
        mode: 'cors'
      })
      .then((response) => response.json())
      .then((data) => {
        let probeDataByID = {}
        for (let i in data.probe_datas) {
          let pd = data.probe_datas[i]
          probeDataByID[pd.id] = pd
        }
        this.setState({probe_datas: data.probe_datas, probeDataByID: probeDataByID})
      })
      .catch((error) => {
        console.log(error)
    })
  }

  handleInput = (e) => {
    console.log(e)
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
      } else if (this.state.graph_lines.filter(x => x.probe_data_id == this.state.selectedProbeData).length) {
        alert("That probe data is already selected for this graph")
        state_adjustment = {}
      } else {
        // save selection
        let new_graph_lines = this.state.graph_lines
        new_graph_lines.push({id: null, graph_id: null, probe_data_id: this.state.selectedProbeData})
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
    let probe_data_id = e.target.value
    console.log(probe_data_id)
    this.setState({selectedProbeData: probe_data_id})
  }


  render() {
    let submitText = this.props.edit ? "Save" : "Create"
    let cancelButton = null;
    if (this.props.edit === true) {
      cancelButton = <Button onClick={this.props.cancel} type="button">Cancel</Button>
    }

    let probe_data_form  = this.state.graph_lines.map(gl => <div key={gl.probe_data_id} data-value={gl.probe_data_id}>{this.state.probeDataByID[gl.probe_data_id].name}</div>)

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
      <div>
        <Modal show={this.state.showModal} onHide={this.handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>Select a piece of probe data</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form.Group as={Col} controlId="zoneId">
              <Form.Label>Zone Filter</Form.Label>
              <Form.Control as="select">
                {zoneOptions}
              </Form.Control>
            </Form.Group>
            <Form.Group as={Col} controlId="probeId">
              <Form.Label>Probe Filter</Form.Label>
              <Form.Control as="select" onChange={this.handleSelectProbe}>
                {probeOptions}
              </Form.Control>
            </Form.Group>
            <Form.Group as={Col} controlId="probeDataId">
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
          <Form.Group as={Col} controlId="graphNameId">
            <Form.Label>Graph Name</Form.Label>
            <Form.Control name='name' value={this.state.graph.name} onChange={this.handleInput} placeholder="My graph" />
          </Form.Group>
          <Form.Group controlId="graphDescriptionId">
            <Form.Label>Description</Form.Label>
            <Form.Control name='description' value={this.state.graph.description} onChange={this.handleInput} placeholder="This graph shows whatever" />
          </Form.Group>
          <Form.Group controlId="graphLines">
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

export default GraphForm