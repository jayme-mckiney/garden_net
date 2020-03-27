import React, { Component } from 'react';

import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';


class FormOption extends Component {

  render() {
    return(<option value="{this.props.value}">{this.props.label}</option>)
  }
}

class CreateProbe extends Component {

  render() {

    // get the zone options for real
    let zone_options = new Map([[1, "Zone 1"], [2, "Zone 2"], [3, "Zone 3"]])
    let form_options = [<FormOption value={null} label="None" />]
    for (const[k, v] of zone_options) {
      form_options.push(<FormOption value={k} label={v} />)
    }
    return (
      <Form>
        <Form.Row>
          <Form.Group as={Col} controlId="probeNameId">
            <Form.Label>Probe Name</Form.Label>
            <Form.Control placeholder="Environmental Sensor 1" />
          </Form.Group>
          <Form.Group as={Col} controlId="probeUrlId">
            <Form.Label>Probe URL</Form.Label>
            <Form.Control placeholder="ESP_3216581" />
          </Form.Group>
        </Form.Row>
        <Form.Group controlId="probeDescriptionId">
          <Form.Label>Description</Form.Label>
          <Form.Control placeholder="This environmental sensor is installed near the lights" />
        </Form.Group>
        <Form.Row>
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
              label="Activate this probe on creation"
            />
          </Form.Group>
        </Form.Row>
        <Button type="submit">Submit form</Button>
      </Form>

    )
  }
}

export default CreateProbe;
