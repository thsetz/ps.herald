import os
import pytest
import signal
import subprocess
import time
import tempfile

from ps.basic import DEV_STAGES
# from ps.basic import Config

from ps.herald import create_app
from ps.herald import database
# from ps.herald.model import Log

from t_util import TEST_SERVICE_NAME

with open(os.path.join(os.path.dirname(__file__), "test_data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8").split("\n")


#@pytest.fixture(scope="module", params=["TESTING"])
# @pytest.fixture(params=["TESTING"])
# @pytest.fixture(scope="module", params=DEV_STAGES.keys())
@pytest.fixture(params=DEV_STAGES.keys())
def dev_allowed_stages(request):
    os.environ["TESTING"] = "YES"
    os.environ["DEV_STAGE"] = request.param
    return request.param


@pytest.fixture
def stage(dev_allowed_stages):
    db_fd, db_path = tempfile.mkstemp()
    stage = "TESTING"
    stage = dev_allowed_stages
    os.environ["DEV_STAGE"] = stage
    cwd = os.getcwd()
    # create a root dir for all test environments
    tmp_run_tests_root_dir = os.path.join(cwd, "tmp_test_run")
    if not os.path.isdir(tmp_run_tests_root_dir):
        os.mkdir(tmp_run_tests_root_dir)
    os.chdir(tmp_run_tests_root_dir)
    # create a stage specific dir for all tests
    tmp_run_tests_stage_dir = os.path.join(
        tmp_run_tests_root_dir, DEV_STAGES[stage]["suffix"]
    )
    if not os.path.isdir(tmp_run_tests_stage_dir):
        os.mkdir(tmp_run_tests_stage_dir)
    os.chdir(tmp_run_tests_stage_dir)
    old_herald_sqlite_file = f'herald.sqlite{DEV_STAGES[stage]["suffix"]}'
    if os.path.isfile(old_herald_sqlite_file):
        os.remove(old_herald_sqlite_file)
        print(f"{old_herald_sqlite_file} found and deleted")
    else:
        print(f"{old_herald_sqlite_file} Not found and not deleted")
    yield stage
    os.close(db_fd)
    os.unlink(db_path)
    os.chdir(cwd)


@pytest.fixture
def app(stage):

    db_fd, db_path = tempfile.mkstemp()
    os.environ["DEV_STAGE"] = stage
    app = create_app(
        TEST_SERVICE_NAME,
        test_config={
            "TESTING": True,
            "DATABASE": db_path,
        },
    )
    yield app
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def db_app_with_test_data(app):

    with app.app_context():
        database.init_db()
        engine = database.get_engine()
        try:
            for insert_sql_staement_line in _data_sql:
                engine.execute(insert_sql_staement_line)
        except Exception:
            print("Error Inserting Test data into the database")
            raise
    return app


@pytest.fixture
def db_app(app):
    with app.app_context():
        # The fixture is called sometimes with ps_bridge in the background,
        # that needs a ittle time ...
        time.sleep(10)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def with_ps_bridge_in_background(stage):
    # proc = subprocess.Popen('ps_bridge -v > ps_brige_log 2>&1 ',
    proc = subprocess.Popen(
        "ps_bridge -v ",
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    yield proc

    # if the kill finds a terminated bridge - it will raise
    # an exception.
    os.kill(int(proc.pid), 0)
    print(f"process with pid {proc.pid} is still alive. Kill it now.")
    os.kill(proc.pid, signal.SIGKILL)
    # give bitbucket a littlt more time
    time.sleep(5)
    return "OK"


# def have_neelix_config_file():
#    with open(Config.config_file_name, "w") as fp:
#        fp.write("[test_section]\n")
#        fp.write("    test_name = test_value  \n")
#        fp.write("[GLOBAL]\n")
#        fp.write("    LOGGING =  DEBUG\n")
