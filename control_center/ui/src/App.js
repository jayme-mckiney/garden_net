import React from 'react';
import logo from './logo.svg';
import './App.css';

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';
import ListGroup from 'react-bootstrap/ListGroup';

import {
  Route,
  NavLink,
  HashRouter
} from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Navbar bg="dark" variant="dark">
        <button className="d-lg-none toggle-sidebar"><span className="navbar-toggler-icon"></span></button>
        <Navbar.Brand href="/">Garden Net</Navbar.Brand>
      </Navbar>
      <HashRouter>
        <Row>
          <Nav to="/" className="flex-sm-column" id="sidebar">
            <ListGroup className="nav nav-sidebar flex-sm-column">
              <ListGroup.Item>
                <a href="#monitor" data-toggle="collapse" aria-expanded="false" className="dropdown-toggle"><span>Monitor</span></a>
              </ListGroup.Item>
          </Nav>

          <Col xl={{ span: 7, offset: 3 }} lg={{ span: 8, offset: 3 }} xs={{ span: 8, offset: 2 }}>
            <Container>

            </Container>
          </Col>
        </Row>
      </HashRouter>
    </div>
  );
}

export default App;
