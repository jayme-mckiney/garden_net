import React, { Component } from 'react';

import ListGroup from 'react-bootstrap/ListGroup';
import Col from 'react-bootstrap/Col';

import resolveHost from '../../helpers'

class ListProbes extends Component {

  componentWillMount() {
    let host = resolveHost()
    fetch(`http://${host}/probes`, {
      method: 'GET',
      mode: 'cors',
    })
    .then((data) => {
      this.probes = data
      console.log(data);
    })
    .catch((error) => {
      console.log(error)
    })
  }

  render() {
    let content =  "<h1>Loading</h1>"
    if (this.probes != null) {
      content = this.probes
    }

    return (

      content

    )
  }
}

export default ListProbes;
