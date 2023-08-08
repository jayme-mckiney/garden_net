import React, { Component } from 'react';
import { Container, Row, Col, Spinner } from 'react-bootstrap';

import {resolveHost} from '../../helpers'



class MonitorHome extends Component {
  state = {
    data: null
  };

  componentDidMount() {

  }

  render() {
    let content =  <Row><Spinner animation="grow" /><Spinner animation="grow" /><Spinner animation="grow" /></Row>
    if (this.state.data != null) {

    }

    return (
      <Container>
        <Row>
          Monitor Home Screen
        </Row>
        {content}


      </Container>
    )
  }
}

export default MonitorHome;
