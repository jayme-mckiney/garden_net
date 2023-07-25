import React, { Component } from 'react';

import Table from 'react-bootstrap/Table';
import Col from 'react-bootstrap/Col';

import {resolveHost} from '../../helpers'
import ProbeForm  from './form'


class ProbeEntry extends Component {
  render() {
    let probe = this.props.probeData
    return(
      <tr onClick={this.props.onClick}>
        <td>{probe.name}</td>
        <td>{probe.description}</td>
        <td>{probe.url}</td>
        <td>{probe.active? "Active" : "Deactivated"}</td>
      </tr>
    )
  }
}

class EditFormWrapper extends Component {
  render() {
    return (
      <tr>
      <td colSpan="4">
        <ProbeForm edit={true} cancel={this.props.cancel} probe={this.props.probe}/> </td>
      </tr>
    )
  }
}

class ListProbes extends Component {
  constructor(props) {
    super(props)
    this.state = {
      probes: null,
      edit: null
    };
  }

  componentDidMount() {
    let host = resolveHost()
    fetch(`http://${host}/probes`, {
      method: 'GET',
      mode: 'cors',
    })
    .then((response) => response.json())
    .then((data) => {
      this.setState({probes: data.probes})
    })
    .catch((error) => {
      console.log(error)
    })
  }

  startEdit(id, event) {
    this.setState({edit: id});
  }

  cancelEdit(event) {
    this.setState({edit: null});
  }

  render() {
    let content =  "<h1>Loading</h1>"
    if (this.state.probes != null) {
      content = []

      for(let index in this.state.probes) {
        if (this.state.edit !== null && this.state.edit === index) {
          content.push(<EditFormWrapper key={index} cancel={this.cancelEdit.bind(this)} probe={this.state.probes[index]} />)
        } else {
          content.push(<ProbeEntry key={index} onClick={this.startEdit.bind(this, index)} probeData={this.state.probes[index]} />)
        }
      }
    }

    return (
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>URL</th>
            <th>Active</th>
          </tr>
        </thead>
        <tbody>
          {content}
        </tbody>
      </Table>
    )
  }
}

export default ListProbes;
