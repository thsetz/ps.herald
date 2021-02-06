from ps.herald import database
from ps.herald.model import Log


def test_init_db_app_check_that_we_have_good_test_data(db_app_with_test_data):
    with db_app_with_test_data.app_context():
        session = database.get_session()
        assert session.query(Log).count() > 10
        assert session.query(Log.produkt_id).distinct().count() > 1
        assert session.query(Log.system_id).distinct().count() > 1
        assert session.query(Log.sub_system_id).distinct().count() > 1
        assert session.query(Log.sub_sub_system_id).distinct().count() > 1
        assert session.query(Log.user_spec_1).distinct().count() > 1
        assert session.query(Log.user_spec_2).distinct().count() > 1
