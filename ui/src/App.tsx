import React from 'react';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min';
import './App.css'
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
import {GraphForm, GraphFormEdit} from './views/graph/form'
import {ReadoutForm, ReadoutFormEdit} from './views/single_point_monitor/form'
import ListGraphs from './views/graph/list'
import MonitorSearchForm from './views/monitor/search'
import ListProbes from './views/probe/list'
import {ProbeGraphWrapper, ProbeDataGraphWrapper, GraphGraphWrapper, ZoneGraphWrapper} from './views/monitor/graph'
import {Readout, ReadoutWrapperParams} from './views/monitor/single_readout'

function App() {
  return (
    <div className="App">
      <HashRouter>
        <Navbar bg="dark" variant="dark">
          <button data-bs-target="#sidebar" data-bs-toggle="collapse" className="d-lg-none toggle-sidebar"><span className="navbar-toggler-icon"></span></button>
          <Navbar.Brand href="/">Garden Net</Navbar.Brand>
        </Navbar>
        <Row>
          <Nav to="/" className="flex-sm-column collapse" id="sidebar">
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
                      <a href="#graphs" data-bs-toggle="collapse" aria-expanded="false" className="dropdown-toggle"><span>Graphs</span></a>
                    </ListGroup.Item>
                    <ListGroup>
                      <ListGroup className="sub-menu collapse" id="graphs">
                        <ListGroup.Item> <NavLink to="/graphs/create">Create</NavLink></ListGroup.Item>
                        <ListGroup.Item> <NavLink to="/graphs/">List</NavLink></ListGroup.Item>
                      </ListGroup>
                    </ListGroup>

                    <ListGroup.Item>
                      <a href="#probes" data-bs-toggle="collapse" aria-expanded="false" className="dropdown-toggle"><span>Probes</span></a>
                    </ListGroup.Item>
                    <ListGroup>
                      <ListGroup className="sub-menu collapse" id="probes">
                        <ListGroup.Item> <NavLink to="/probes/create">Create</NavLink></ListGroup.Item>
                        <ListGroup.Item> <NavLink to="/probes/">List</NavLink></ListGroup.Item>
                      </ListGroup>
                    </ListGroup>

                    <ListGroup.Item>
                      <a href="#zones" data-bs-toggle="collapse" aria-expanded="false" className="dropdown-toggle"><span>Zones</span></a>
                    </ListGroup.Item>
                    <ListGroup>
                      <ListGroup className="sub-menu collapse" id="zones">
                        <ListGroup.Item> <NavLink to="/zones/create">Create</NavLink></ListGroup.Item>
                        <ListGroup.Item> <NavLink to="/zones/list">List</NavLink></ListGroup.Item>
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
                <Route path="/data/probe/:id" element={<ProbeGraphWrapper />}/>
                <Route path="/data/probedata/:id" element={<ProbeDataGraphWrapper />}/>
                <Route path="/data/zone/:id" element={<ZoneGraphWrapper />}/>
                <Route path="/data/graph/:id" element={<GraphGraphWrapper />}/>
                <Route path="/data/readout/:id" element={<ReadoutWrapperParams />}/>                
                <Route path="/probes" element={<ListProbes />}/>
                <Route path="/probes/create" element={<ProbeForm />}/>
                <Route path="/graphs/create" element={<GraphForm />}/>
                <Route path="/graphs/:id" element={<GraphFormEdit edit={true} />}/>
                <Route path="/graphs" element={<ListGraphs />}/>
                <Route path="/readout/create" element={<ReadoutForm />}/>
                <Route path="/readout/:id" element={<ReadoutFormEdit edit={true} />}/>

              </Routes>
            </Container>
          </Col>
        </Row>
      </HashRouter>
    </div>
  );
}

export default App;
