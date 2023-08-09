import React, { Component } from 'react';

import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import {resolveHost, get, request} from '../../helpers'
import ProbeDataDrilldown from '../common/probe_data_drilldown'
import { useParams } from "react-router";


export class ReadoutForm extends Component {
  constructor(props) {
    super(props)
    let new_monitor = {
      id: null,
      name: null,
      probedata_id: null,
      tolerable_lower_bound: null,
      tolerable_upper_bound: null,
      refresh_interval: null,
    };
    Object.assign(new_monitor, props.monitor)
    this.state = {monitor: new_monitor}
  }

  componentDidMount() {
    let host = resolveHost()
    if (this.props.edit) {
      get(`monitors/${this.props.id}`,
          (data) => this.setState({'monitor': data.monitor}),
          (e) => console.log(e))
    }
  }

  handleInput = (event) => {
    const target = event.target;
    const value = target.name === "active" ? target.checked : target.value;
    const name = target.name;
    let new_state = {}
    Object.assign(new_state, this.state.monitor)
    new_state[name] = value;
    this.setState({'monitor': new_state});
  }

  handleSelect = (probedata_id) => {
    let new_state = {}
    Object.assign(new_state, this.state.monitor)
    new_state['probedata_id'] = probedata_id
    this.setState({monitor: new_state})
  }


  save = () => {
    let host = resolveHost()
    let route = this.props.edit ? `monitors/${this.state.monitor.id}` : 'monitors'
    let method = this.props.edit ? 'PUT' : 'POST'
    let monitor = {}
    Object.assign(monitor, this.state.monitor)
    let payload = {
      monitor: monitor,
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
    return (
      <Form style={{marginTop: 20}}>
        <ProbeDataDrilldown selected={this.state.monitor.probedata_id} handleSelect={this.handleSelect} />
        <Form.Group as={Col}>
          <Form.Label>Monitor Name</Form.Label>
          <Form.Control name='name' value={this.state.monitor.name} onChange={this.handleInput} placeholder="Primary Temp" />
        </Form.Group>
        <Row>
          <Form.Group as={Col}>
            <Form.Label>Lower tolerance</Form.Label>
            <Form.Control name='tolerable_lower_bound' value={this.state.monitor.tolerable_lower_bound} onChange={this.handleInput} placeholder="5.5" />
          </Form.Group>
          <Form.Group as={Col}>
            <Form.Label>Upper tolerance</Form.Label>
            <Form.Control name='tolerable_upper_bound' value={this.state.monitor.tolerable_upper_bound} onChange={this.handleInput} placeholder="10.5" />
          </Form.Group>
          <Form.Group as={Col}>
            <Form.Label>Refresh Interval(seconds)</Form.Label>
            <Form.Control name='refresh_interval' value={this.state.monitor.refresh_interval} onChange={this.handleInput} placeholder="120" />
          </Form.Group>
        </Row>
        <Form.Group>

        </Form.Group>
        <Button onClick={this.save} type="button">{submitText}</Button>
        {cancelButton}
      </Form>

    )
  }
}

export const ReadoutFormEdit = () => {
  let { id } = useParams();
  return (<ReadoutForm id={id} edit={true} />)
}

