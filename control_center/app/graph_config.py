from flask import (
    request,
    jsonify
  )
from flask_restful import (
    Resource,
    abort,
    marshal
  )
from app.models import Graph, GraphLine
from app.db import db_session
import logging
_logger = logging.getLogger('')

class GraphList(Resource):
  def get(self):
    results = Graph.query.all()
    dictionary_list = list(map(lambda r: r.as_dict(), results))
    return {'graphs': dictionary_list}, 200

  def post(self):
    json = request.get_json(force=True)
    graph_json = json.get('graph')
    try:
      new_graph = Graph(name=graph_json.get('name'), description=graph_json.get('description'))
      db_session.add(new_graph)
      db_session.commit()
      graph_lines_json = json.get('graph_lines', [])
      for graph_line in graph_lines_json:
        new_graph_line = GraphLine(graph_id = new_graph.id, probedata_id = graph_line.get('probedata_id'))
        db_session.add(new_graph_line)
      db_session.commit()
    except TypeError as e:
      _logger.error(e)
      error_data = {'message': 'payload does no match db schema'}
      abort(400, **error_data)
    except Exception as e:
      error_data = {'message': 'Something went wrong'}
      abort(500, **error_data)
    return ({}, 200)


class GraphConfig(Resource):
  def get(self, id):
    result = Graph.query.filter(Graph.id == id).first()
    graph_lines = []
    for graph_line in result.graph_lines:
      graph_lines.append(graph_line.as_dict())
    graph_dict = result.as_dict()
    return {'graph': graph_dict, 'graph_lines': graph_lines}

  def put(self, id):
    graph = Graph.query.filter(Graph.id == id).first()
    graph_dict = graph.as_dict()
    json = request.get_json(force=True)
    graph_lines_json = json.get('graph_lines', [])
    try:
      for key in graph_dict:
        setattr(graph, key, json.get('graph').get(key))
      for graph_line_json in graph_lines_json:
        if graph_line_json.get('id') != None:
          for graph_line in graph.graph_lines:
            if graph_line.id == graph_line_json.get('id'):
              graph_line.probedata_id = graph_line_json.get('probedata_id')
              break
        else:
          new_graph_line = GraphLine(graph_id = graph.id, probedata_id = graph_line_json.get('probedata_id'))
          db_session.add(new_graph_line)
      db_session.commit()
    except TypeError as e:
      _logger.error(e)
      error_data = {'message': 'payload does no match db schema'}
      abort(400, **error_data)
    except Exception as e:
      error_data = {'message': 'Something went wrong'}
      abort(500, **error_data)
    return ({}, 200)
