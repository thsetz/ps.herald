from ps.herald import create_app
from t_util import TEST_SERVICE_NAME
from ps.basic import Config


def test_config(stage):
    Config.reset_singleton()
    assert not create_app("muh").testing
    Config.reset_singleton()
    assert create_app("muh", test_config={"TESTING": True}).testing


def test_ps_log_msg_appears_in_logfile(stage):
    assert create_app("muh2", test_config={"TESTING": True}).testing
    msg = "This should appear in the log file"
    Config.logger.info(msg)
    assert msg in Config.get_logging_data()
    print(Config.get_logging_data())


def test_hello(client):
    response = client.get("/hello")
    assert response.data == b"Hello, World!"


def test_init_app(app):
    assert app.config["DEBUG"] is False
    assert (
        Config.log_file_name
        == "LOG/" + TEST_SERVICE_NAME + Config.suffix + ".log"
    )
    assert app.config["DATABASE"] == Config.herald_sqlite_filename
