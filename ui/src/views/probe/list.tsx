import React, { Component } from 'react';

import Table from 'react-bootstrap/Table';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';

import {withRouter, get, EditIcon, request, TrashIcon} from '../../helpers'

import ProbeForm  from './form'


function ProbeEntry(props) {
  let probe = props.probeData
  let trashButton = null
  if (props.listEdit == true)
    trashButton = <td onClick={props.remove}><TrashIcon /></td>
  return(
    <tr>
      <td><EditIcon onClick={props.onClick} /></td>
      <td>{probe.name}</td>
      <td>{probe.description}</td>
      <td>{probe.url}</td>
      <td>{probe.active? "Active" : "Deactivated"}</td>
      {trashButton}
    </tr>
  )
}

function EditFormWrapper(props) {
  return (
    <tr>
    <td colSpan={props.span}>
      <ProbeForm edit={true} cancel={props.cancel} probe={props.probe}/> </td>
    </tr>
  )
}

class ListProbes extends Component {
  constructor(props) {
    super(props)
    this.state = {
      probes: null,
      editEntry: null,
      listEdit: false
    };
  } 

  componentDidMount() {
    get('probes', (data) => this.setState({probes: data.probes}), (e) => console.log(e))
  }

  startEdit = (id, event) => {
    this.setState({editEntry: id});
  }

  cancelEdit = (event) => {
    this.setState({editEntry: null});
  }

  toggleListEdit = () => this.setState({listEdit: !this.state.listEdit})

  render() {
    let content =  null
    if (this.state.probes != null) {
      content = []

      for(let index in this.state.probes) {
        if (this.state.editEntry !== null && this.state.editEntry === index) {
          content.push(<EditFormWrapper key={index} span={this.state.listEdit? 6 : 5} cancel={this.cancelEdit.bind(this)} probe={this.state.probes[index]} />)
        } else {
          content.push(<ProbeEntry key={index} listEdit={this.state.listEdit} onClick={this.startEdit.bind(this, index)} probeData={this.state.probes[index]} />)
        }
      }
    }
    let trashHeader = null
    if (this.state.listEdit) {
      trashHeader = <th style={{width: 20}}><TrashIcon /></th>
    }

    return (
      <>
      <Table style={{marginTop: 20}} striped bordered hover>
        <thead>
          <tr>
            <th style={{width: 20}}><EditIcon /></th>
            <th>Name</th>
            <th>Description</th>
            <th>URL</th>
            <th>Active</th>
            {trashHeader}
          </tr>
        </thead>
        <tbody>
          {content}
        </tbody>
      </Table>
      <Button onClick={this.toggleListEdit}>Edit List</Button>
      </>
    )
  }
}

export default ListProbes;
