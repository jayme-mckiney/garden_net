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
  Outlet,
  NavLink,
  HashRouter
} from "react-router-dom";

import Welcome from './views/welcome';
import MonitorHome from './views/monitor/home'
import ProbeForm from './views/probe/form'
import MonitorSearchForm from './views/monitor/search'
import ListProbes from './views/probe/list'
import {SimpleGraphWrapper} from './views/monitor/graph'

function App() {
  return (
    <div className="App">
      <HashRouter>
        <Navbar bg="dark" variant="dark">
          <button data-bs-target="#sidebar" data-bs-toggle="collapse" className="d-lg-none toggle-sidebar"><span className="navbar-toggler-icon"></span></button>
          <Navbar.Brand href="/">Garden Net</Navbar.Brand>
        </Navbar>
        <Row>
          <Nav to="/" className="flex-sm-column collapse" tabindex="-1" id="sidebar">
            <ListGroup className="nav nav-sidebar flex-sm-column">

              <ListGroup.Item>
                <a href="#monitor" data-bs-toggle="collapse" aria-expanded="false" className="dropdown-toggle"><span>Monitor</span></a>
              </ListGroup.Item>
                <ListGroup>
                  <ListGroup className="sub-menu collapse" id="monitor">
                    <ListGroup.Item> <NavLink to="/data/home">Home</NavLink></ListGroup.Item>
                    <ListGroup.Item> <NavLink to="/data/search">Search</NavLink></ListGroup.Item>
                  </ListGroup>
                </ListGroup>
              <ListGroup.Item role="separator" className="divider"></ListGroup.Item>

              <ListGroup.Item>
                <a href="#config" data-bs-toggle="collapse" aria-expanded="false" className="dropdown-toggle"><span>Config</span></a>
              </ListGroup.Item>
                <ListGroup>
                  <ListGroup className="sub-menu collapse" id="config">

                    <ListGroup.Item>
                      <a href="#probes" data-bs-toggle="collapse" aria-expanded="false" className="dropdown-toggle"><span>Probes</span></a>
                    </ListGroup.Item>
                    <ListGroup>
                      <ListGroup className="sub-menu collapse" id="probes">
                        <ListGroup.Item> <NavLink to="/probes/create">Create</NavLink></ListGroup.Item>
                        <ListGroup.Item> <NavLink to="/probes/">List</NavLink></ListGroup.Item>
                        <ListGroup.Item> <NavLink to="/probes/search">Search</NavLink></ListGroup.Item>
                      </ListGroup>
                    </ListGroup>

                    <ListGroup.Item>
                      <a href="#zones" data-bs-toggle="collapse" aria-expanded="false" className="dropdown-toggle"><span>Zones</span></a>
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
                <Route path="/" element={<Welcome />}/>
                <Route path="/data/home" element={<MonitorHome />}/>
                <Route path="/data/probe/:id" element={<SimpleGraphWrapper />}/>
                <Route path="/probes" element={<ListProbes />}/>
                <Route path="/probes/create" element={<ProbeForm />}/>
                
              </Routes>
            </Container>
          </Col>
        </Row>
      </HashRouter>
    </div>
  );
}

export default App;
