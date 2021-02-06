"""[summary]

Provide helper functions used within the test environment.
"""
import os
from socket import gethostname

from ps.basic import Config, DEV_STAGES

TEST_SERVICE_NAME = "test_service_name"


def common_Config_class_attributes_after_initialisation(  # noqa: N802
    stage_p: str, test_service_name: str = TEST_SERVICE_NAME
):
    assert Config.service_name == test_service_name
    assert Config.__dict__["service_name"] == test_service_name
    assert os.getenv("SYSTEM_ID", None) == test_service_name
    assert os.getenv("SUB_SYSTEM_ID", None) == gethostname()
    assert Config.dev_stage == stage_p
    assert Config.suffix == DEV_STAGES[stage_p]["suffix"]
    assert Config.log_file_name == os.path.join(
        "LOG", Config.service_name + Config.suffix + ".log"
    )
    assert Config.logging_port == DEV_STAGES[stage_p]["logging_port"]
    assert Config.webserver_port == DEV_STAGES[stage_p]["logging_port"] + 1
    assert (
        Config.logging_bridge_port
        == DEV_STAGES[stage_p]["logging_bridge_port"]  # noqa: W503
    )
    assert Config.logging_level == DEV_STAGES[stage_p]["logging_level"]
    assert Config.admin_mail == DEV_STAGES[stage_p]["l_admin_mail"]
    assert Config.herald_sqlite_filename == os.path.join(
        os.getcwd(), "herald.sqlite%s" % Config.suffix
    )
    assert Config.lock_file_name == os.path.join(
        os.getcwd(), "%s_lock%s" % (Config.service_name, Config.suffix)
    )

    assert os.path.isdir("LOG")
    assert os.path.isfile(Config.log_file_name)
