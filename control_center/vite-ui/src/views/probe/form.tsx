import React, { Component } from 'react';

import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';


class FormOption extends Component {

  render() {
    return(<option value="{this.props.value}">{this.props.label}</option>)
  }
}

class ProbeForm extends Component {
  constructor(props) {
    super(props)
    let new_probe = {
      probe_id: null,
      name: null,
      zone_id: null,
      description: null,
      url: null,
      active: false,
      name_mapping: {}
    };
    Object.assign(new_probe, props.probe);
    console.log(props.probe)
    new_probe.name_mapping = JSON.stringify(new_probe.name_mapping)
    this.state = new_probe
    this.handleInput  = this.handleInput.bind(this)
  }

  handleInput(event) {
    const target = event.target;
    console.log(target)
    const value = target.name === "active" ? target.checked : target.value;
    const name = target.name;
    let new_state = {}
    new_state[name] = value;
    console.log(new_state)
    this.setState(new_state);
  }

  render() {
    let submitText = this.props.edit ? "Save" : "Create"
    let cancelButton = null;
    if (this.props.edit === true) {
      cancelButton = <Button onClick={this.props.cancel} type="button">Cancel</Button>
    }
    // get the zone options for real
    let zone_options = new Map([[1, "Zone 1"], [2, "Zone 2"], [3, "Zone 3"]])
    let form_options = [<FormOption key={0} value={null} label="None" />]
    for (const[k, v] of zone_options) {
      form_options.push(<FormOption key={k} value={k} label={v} />)
    }
    return (
      <Form>
        <Row>
          <Form.Group as={Col} controlId="probeNameId">
            <Form.Label>Probe Name</Form.Label>
            <Form.Control name='name' value={this.state.name} onChange={this.handleInput} placeholder="Environmental Sensor 1" />
          </Form.Group>
          <Form.Group as={Col} controlId="probeUrlId">
            <Form.Label>Probe URL</Form.Label>
            <Form.Control name='url' value={this.state.url} onChange={this.handleInput} placeholder="ESP_3216581" />
          </Form.Group>
        </Row>
        <Form.Group controlId="probeDescriptionId">
          <Form.Label>Description</Form.Label>
          <Form.Control name='description' value={this.state.description} onChange={this.handleInput} placeholder="This environmental sensor is installed near the lights" />
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
              checked={this.state.active}
              onChange={this.handleInput}
              label="Activate this probe"
            />
          </Form.Group>
        </Row>
        <Form.Group controlId="probeNameMapping">
          <Form.Label>Name Mapping</Form.Label>
          <Form.Control value={this.state.name_mapping} onChange={this.handleInput} />
        </Form.Group>
        <Button type="submit">{submitText}</Button>
        {cancelButton}
      </Form>

    )
  }
}

export default ProbeForm;
