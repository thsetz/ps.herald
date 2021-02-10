from datetime import datetime, timedelta
from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

import sqlalchemy

from ps.basic import Config
from ps.herald import __version__
from ps.herald.model import Log
from ps.herald.database import get_session


bp = Blueprint("angular_api", __name__)




@bp.route("/", methods=["GET", "POST"])
def index():
    session = get_session()
    return render_template("angular_api/index.html")


@bp.route("/list", methods=["GET", "POST"])
def list():
    if request.method == "POST":
       print("JUHU")
       query_parameters = request.args
       print(query_parameters)
       return '[{"message":"The message"}]'
    query_parameters = request.args
    print(query_parameters)
    print("GET CALLED")
    session = get_session()
    #rows = session.query(Log).all()
    #rows = session.query(Log).limit(10).all()

    #query = session.query(Log).limit(10)
    query_obj = session.query(Log)
    #print(query_obj)

    if query_parameters["PRODUKT_ID"] != "not_selected":
        #print("ADAPT PRODUKT_ID"*50)
        query_obj= query_obj.filter( Log.produkt_id == query_parameters["PRODUKT_ID"])
    else:
        pass
        #print("NOT ADAPT PRODUKT_ID"*50)
    if query_parameters["limit"] != "not_selected":
        limit_amount = query_parameters["limit"]
    else:
        limit_amount = 10


    #print(query_obj)
    #rows = query(Log).all()
    #rows = session.query(Log).limit(limit_amount)
    rows = query_obj.limit(limit_amount)

    k=  [l.as_dict() for l in rows  ] 
    for row in k:
          print(row["produkt_id"])
 
    #response = jsonify(rows)
    #response.status_code = 200
    #return response
 
    #log_entries = []
    #for log_entry in rows:
    #      log_entries.append(log_entry.as_dict())
    
    #return jsonify(log_entries) 
    return jsonify([l.as_dict() for l in rows  ]) 




@bp.route("/hello")
def hello():
    msg="Hello Angular World called"
    return msg


@bp.route("/hello_to_ps_basic_logger")
def hello_to_ps_basic_logger():
    msg="Hello Angular World called"
    Config.logger.info(msg)
    return msg

