import React from 'react';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min';

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';
import ListGroup from 'react-bootstrap/ListGroup';

import {
  Route,
  Routes,
  NavLink,
  HashRouter
} from "react-router-dom";

import Welcome from './views/welcome';
import MonitorHome from './views/monitor/home'
import CreateProbe from './views/probe/form'
import ListProbes from './views/probe/list'
import {SimpleGraphWrapper} from './views/monitor/graph'

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
                <ListGroup>
                  <ListGroup className="sub-menu collapse" id="monitor">
                    <ListGroup.Item> <NavLink to="/data/home">Home</NavLink></ListGroup.Item>
                    <ListGroup.Item> <NavLink to="/data/search">Search</NavLink></ListGroup.Item>
                  </ListGroup>
                </ListGroup>
              <ListGroup.Item role="separator" className="divider"></ListGroup.Item>

              <ListGroup.Item>
                <a href="#config" data-toggle="collapse" aria-expanded="false" className="dropdown-toggle"><span>Config</span></a>
              </ListGroup.Item>
                <ListGroup>
                  <ListGroup className="sub-menu collapse" id="config">

                    <ListGroup.Item>
                      <a href="#probes" data-toggle="collapse" aria-expanded="false" className="dropdown-toggle"><span>Probes</span></a>
                    </ListGroup.Item>
                    <ListGroup>
                      <ListGroup className="sub-menu collapse" id="probes">
                        <ListGroup.Item> <NavLink to="/probes/create">Create</NavLink></ListGroup.Item>
                        <ListGroup.Item> <NavLink to="/probes/list">List</NavLink></ListGroup.Item>
                        <ListGroup.Item> <NavLink to="/probes/search">Search</NavLink></ListGroup.Item>
                      </ListGroup>
                    </ListGroup>

                    <ListGroup.Item>
                      <a href="#zones" data-toggle="collapse" aria-expanded="false" className="dropdown-toggle"><span>Zones</span></a>
                    </ListGroup.Item>
                    <ListGroup>
                      <ListGroup className="sub-menu collapse" id="zones">
                        <ListGroup.Item> <NavLink to="/zones/create">Create</NavLink></ListGroup.Item>
                        <ListGroup.Item> <NavLink to="/zones/list">List</NavLink></ListGroup.Item>
                        <ListGroup.Item> <NavLink to="/zones/search">Search</NavLink></ListGroup.Item>
                      </ListGroup>
                    </ListGroup>

                  </ListGroup>
                </ListGroup>
              <ListGroup.Item role="separator" className="divider"></ListGroup.Item>

            </ListGroup>
          </Nav>

          <Col xl={{ span: 7, offset: 3 }} lg={{ span: 8, offset: 3 }} xs={{ span: 8, offset: 2 }}>
            <Container>
              <Routes>
                {/*<Route path="/" component={Welcome}/>*/}
                <Route path="/data/home" component={MonitorHome}/>
                <Route path="/data/probe/:id" component={SimpleGraphWrapper}/>
                <Route path="/probes/create" component={CreateProbe}/>
                <Route path="/probes" component={ListProbes}/>
              </Routes>
            </Container>
          </Col>
        </Row>
      </HashRouter>
    </div>
  );
}

export default App;
