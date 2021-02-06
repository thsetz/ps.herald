import socket
from ps.basic import Config
from ps.herald.ps_neelix import check
from ps.herald.database import get_session
from ps.herald.model import Log, HeartBeat


def test_neelix(db_app_with_test_data):
    """[summary]
       Given a  fixture generating a context with test_data,

        - We generate a configfile (write_conig_parser)
        - the test data heartbeat table is empty
        - run the neelix main function checking

        Check that:
           - the heartbeat was updated
           - an email was sent to the adress defined in the
             the config file

    :param db_app_with_test_data: fixture with data
    """
    with db_app_with_test_data.app_context():
        write_conig_parser()
        from configparser import ConfigParser

        Config.config_parser = ConfigParser()
        Config.config_parser.read(Config.config_file_name)

        check()

        session = get_session()

        # Check that HeartBeat Table was updated for each system_id
        rows = session.query(Log.system_id).distinct().all()
        for row in rows:
            system_id = row[0]
            num_rows = (
                session.query(HeartBeat)
                .filter(HeartBeat.system_id == system_id)
                .count()
            )
            assert num_rows == 1
        # Check that the email has been sent
        assert Config.curr_mail_sender == f"neelix@{socket.gethostname()}"
        assert Config.curr_mail_recipients == ['"a@b.de', 'b@c.de"']
        assert "neelix" in Config.curr_mail_subject
        assert "Dear Madam" in Config.curr_mail_text


def write_conig_parser():
    with open(Config.config_file_name, "w") as fp:
        fp.write("[GLOBAL]\n")
        fp.write("url = http://localhost:8080/bugs/\n")
        fp.write("username = dhellmann\n")
        fp.write("password = SECRET\n")
        fp.write("\n")
        fp.write("[box1.a.de]\n")
        fp.write('MAIL_TO = "a@b.de,b@c.de"\n')
        fp.write('MSG="HUHU"\n')
        fp.write("AGE=60*60*2\n")
