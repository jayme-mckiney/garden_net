import React, { Component } from 'react';

import Table from 'react-bootstrap/Table';
import Col from 'react-bootstrap/Col';

import { get} from '../../helpers'
import ProbeForm  from './form'


function ProbeEntry(props) {
  let probe = props.probeData
  return(
    <tr onClick={props.onClick}>
      <td>{probe.name}</td>
      <td>{probe.description}</td>
      <td>{probe.url}</td>
      <td>{probe.active? "Active" : "Deactivated"}</td>
    </tr>
  )
}

function EditFormWrapper(props) {
  return (
    <tr>
    <td colSpan="4">
      <ProbeForm edit={true} cancel={props.cancel} probe={props.probe}/> </td>
    </tr>
  )
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
    get('probes', (data) => this.setState({probes: data.probes}), (e) => console.log(e))
  }

  startEdit = (id, event) => {
    this.setState({edit: id});
  }

  cancelEdit = (event) => {
    this.setState({edit: null});
  }

  render() {
    let content =  null
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
      <Table style={{marginTop: 20}} striped bordered hover>
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
