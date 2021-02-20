import os
from ps.herald import database
from ps.herald.model import Log
from ps.basic import Config
import time


def test_ps_bridge_receives_logging_messages(
    with_ps_bridge_in_background, db_app, client
):
    # def test_ps_bridge(with_ps_bridge_in_background,\
    # db_app_with_test_data,client ):
    """[summary]
    start a bridge in the backgorund and check:

        -  that the logging messages appear in the database

    :param with_ps_bridge_in_background: starts a ps_bridge in the background
    :param db_app_with_test_data: gives us a dtabase provided with test data
    :type db_app_with_test_data: [type]
    :param client: [description]
    :type client: [type]
    """
    Config.logger.info("Emit a message 1")
    with db_app.app_context():
        session = database.get_session()
        num_rows = session.query(Log).count()
        print(f"We have {num_rows} rows")
        Config.logger.info("Emit a message 2")
        Config.logger.info("Emit a message 3")
        Config.logger.info("Emit a message 4")
        time.sleep(4)
        rows = session.query(Log.message).all()
        # for row in rows:
        #    print(row)
        # [('Emit a message 2',), ...] to# ['Emit a message 2', ...]
        rows = [y[0] for y in rows]
        assert "Emit a message 2" in rows
        assert "Emit a message 3" in rows
        assert "Emit a message 4" in rows
        assert len(rows) >= 3


def test_ps_bridge_herald_logging_messages(
    with_ps_bridge_in_background, db_app, client
):
    """[summary]
    Given :
        - a running ps_bridge
        - empty log table
    call : /hello_to_ps_basic_logger which emits a logging message
      via ps.basic.Config.logger
        - check that the message is in the database
    """
    with db_app.app_context():
        response = client.get("/hello_to_ps_basic_logger")
        assert response.data == b"Hello, World!"

        time.sleep(5)
        session = database.get_session()
        num_rows = session.query(Log).count()
        assert num_rows >= 1

        rows = session.query(Log.message).all()
        for row in rows:
            print(row)
        rows = [y[0] for y in rows]
        assert "Hello World called" in rows
