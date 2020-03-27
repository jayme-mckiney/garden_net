import React, { Component } from 'react';

import ListGroup from 'react-bootstrap/ListGroup';
import Col from 'react-bootstrap/Col';

class ListProbes extends Component {

  componentWillMount() {
    fetch('http://0.0.0.0:5000/probes', {
      method: 'GET',
      mode: 'cors',
    })
    .then((data) => {
      this.probes = data
      console.log(data);
    })
    .catch((data) => {
      console.log(data)
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
