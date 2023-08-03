import React, { Component } from 'react';

import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import {resolveHost, get, request} from '../../helpers'

class FormOption extends Component {
  render() {
    return(<option value="{this.props.value}">{this.props.label}</option>)
  }
}

class ProbeForm extends Component {
  constructor(props) {
    super(props)
    let new_probe = {
      id: null,
      name: null,
      zone_id: null,
      description: null,
      url: null,
      active: false,
    };
    Object.assign(new_probe, props.probe);
    let probe_data = []
    this.state = {'probe': new_probe, 'probe_data': probe_data, 'zones': [] }
  }

  componentWillMount() {
    let host = resolveHost()
    get(`zones`,
        (data) => this.setState({zones: data.zones}),
        (e) => console.log(e))
    if (this.props.probe) {
      get(`probes/${this.props.probe.id}`,
          (data) => this.setState({'probe_data': data.probe_data}),
          (e) => console.log(e))
    }
  }

  addProbeData = () => {
    let new_data_part = {
      id: null,
      name: null,
      name_in_probe: null,
      description: null,
      probe_id: this.state.probe.id,
    }
    let data_parts = this.state.probe_data
    data_parts.push(new_data_part)
    this.setState({probe_data: data_parts})
  }

  handleInput = (event) => {
    const target = event.target;
    const value = target.name === "active" ? target.checked : target.value;
    const name = target.name;
    let new_state = {}
    Object.assign(new_state, this.state.probe)
    new_state[name] = value;
    this.setState({'probe': new_state});
  }

  handleProbeDataInput = (event) => {
    const target = event.target;
    const name = target.name;
    const i = parseInt(target.getAttribute('data-index'))
    let new_array = []
    for(let j = 0; j < this.state.probe_data.length; j++) {
      let new_state = {}
      Object.assign(new_state, this.state.probe_data[j])
      new_array.push(new_state)
    }
    new_array[i][name] = target.value
    this.setState({'probe_data': new_array});
  }

  save = () => {
    let host = resolveHost()
    let route = this.props.edit ? `probes/${this.state.probe.id}` : 'probes'
    let method = this.props.edit ? 'PUT' : 'POST'
    let probe = {}
    Object.assign(probe, this.state.probe)
    let new_array = []
    for(let j=0; j < this.state.probe_data.length; j++) {
      let new_state = {}
      Object.assign(new_state, this.state.probe_data[j])
      new_array.push(new_state)
    }
    let payload = {
      probe: probe,
      probe_data: new_array
    }
    request(`${route}`,
            method,
            payload,
            (data) => this.setState(),
            (e) => console.log(e))
  }

  render() {
    const submitText = this.props.edit ? "Save" : "Create"
    let cancelButton = null;
    if (this.props.edit === true) {
      cancelButton = <Button onClick={this.props.cancel} type="button">Cancel</Button>
    }
    // get the zone options for real
    let form_options = []
    if (this.state.zones.length == -1) {
      form_options.push(<FormOption key={0} value={null} label="Loading" />)
    }
    for (let zone of this.state.zones) {
      form_options.push(<FormOption key={zone.id} value={zone.id} label={zone.name} />)
    }
    let probe_data_form = []
    let i =0
    for (let probe_data of this.state.probe_data) {
      probe_data_form.push(
        <div className="form-group row" key={i}>
          <div className="col">
            {i==0 ? <Form.Label>Name</Form.Label>: ""}
            <Form.Control data-index={i} name='name' value={this.state.probe_data[i].name} onChange={this.handleProbeDataInput} placeholder="temp high" /></div>
          <div className="col">
            {i==0 ? <Form.Label>Name in Probe</Form.Label>: ""}
            <Form.Control data-index={i} name='name_in_probe' value={this.state.probe_data[i].name_in_probe} onChange={this.handleProbeDataInput} placeholder="tempertureF" /></div>
          <div className="col">
            {i==0 ? <Form.Label>Description</Form.Label>: ""}
            <Form.Control data-index={i} name='description' value={this.state.probe_data[i].description} onChange={this.handleProbeDataInput} placeholder="temperture from high in the tent" /></div>
        </div>
      )
      i ++;
    }
    return (
      <Form>
        <Row>
          <Form.Group as={Col} controlId="probeNameId">
            <Form.Label>Probe Name</Form.Label>
            <Form.Control name='name' value={this.state.probe.name} onChange={this.handleInput} placeholder="Environmental Sensor 1" />
          </Form.Group>
          <Form.Group as={Col} controlId="probeUrlId">
            <Form.Label>Probe URL</Form.Label>
            <Form.Control name='url' value={this.state.probe.url} onChange={this.handleInput} placeholder="ESP_3216581" />
          </Form.Group>
        </Row>
        <Form.Group controlId="probeDescriptionId">
          <Form.Label>Description</Form.Label>
          <Form.Control name='description' value={this.state.probe.description} onChange={this.handleInput} placeholder="This environmental sensor is installed near the lights" />
        </Form.Group>
        <Row>
          <Form.Group as={Col} controlId="zoneId">
            <Form.Label>Probe Zone Location</Form.Label>
            <Form.Control as="select">
              {form_options}
            </Form.Control>
          </Form.Group>
          <Form.Group as={Col} controlId="activeIid">
            <Form.Check 
              type="switch"
              id="active"
              name='active'
              checked={this.state.probe.active}
              onChange={this.handleInput}
              label="Activate this probe"
            />
          </Form.Group>
        </Row>
        <Form.Group controlId="probeNameMapping">
          <Form.Label>Data Name Mapping</Form.Label>
          {probe_data_form}
          <Button onClick={this.addProbeData} type='button'>Add Data Mapping</Button>
        </Form.Group>
        <Button onClick={this.save} type="button">{submitText}</Button>
        {cancelButton}
      </Form>

    )
  }
}

export default ProbeForm;
