import React, { Component } from 'react';

import Table from 'react-bootstrap/Table';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';

import {withRouter, get, EditIcon, request, TrashIcon} from '../../helpers'
import ProbeForm  from './form'

function GraphEntry(props) {
  let graph = props.graph
  let trashButton = null
  if (props.listEdit == true)
    trashButton = <td onClick={props.remove}><TrashIcon /></td>
  return(
    <tr>
      <td><EditIcon onClick={props.edit} /></td>
      <td onClick={props.view}>{graph.name}</td>
      <td>{graph.description}</td>
      {trashButton}
    </tr>
  )
}

class ListGraphs extends Component {
  constructor(props) {
    super(props)
    this.state = {
      graphs: null,
      listEdit: false
    };
  }


  componentDidMount() {
    get('graphs', (data) => this.setState({graphs: data.graphs}), (e) => console.log(e))
  }

  navigateEdit = (id, e) => {
    this.props.navigate(`/graphs/${id}`)
  }

  navigateView = (id, e) => {
    this.props.navigate(`/data/graph/${id}`)
  }

  removeGraph = (id, e) => {
    request(`graphs/${id}`, 'DELETE', {},
            (data) => {
              let new_array = []
              for( let graph of this.state.graphs) {
                if(graph.id != id) {
                  let newEntry = {}
                  Object.assign(newEntry, graph)
                  new_array.push(newEntry)
                }
              }
              this.setState({graphs: new_array})
            },
            (e) => console.log(e)
    )
  }

  toggleListEdit = () => {
    this.setState({listEdit: !this.state.listEdit})
  }

  render() {
    let content = []
    for( let i in this.state.graphs) {
      let id = this.state.graphs[i].id
      content.push(<GraphEntry key={i} graph={this.state.graphs[i]} view={this.navigateView.bind(this, id)} edit={this.navigateEdit.bind(this, id)} listEdit={this.state.listEdit} remove={this.removeGraph.bind(this, id)} />)
    }
    let trashHeader = null
    if (this.state.listEdit) {
      trashHeader = <th style={{width: 20}}><TrashIcon /></th>
    }
    return (
      <>
        <div style={{ marginTop: 20 }}>
        <Table striped bordered hover>
          <thead>
            <tr>
              <th style={{width: 20}}><EditIcon /></th>
              <th>Name</th>
              <th>Description</th>
              {trashHeader}
            </tr>
          </thead>
          <tbody>
            {content}
          </tbody>
        </Table>
        <Button onClick={this.toggleListEdit}>Edit List</Button>
        </div>
      </>
    );
  }
};

export default withRouter(ListGraphs);
