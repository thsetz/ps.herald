from bs4 import BeautifulSoup

from ps.herald.database import get_session
from ps.herald.model import Log


def test_ps_herald(db_app_with_test_data, client):
    """[summary]
       Given a  fixture generating a context with test_data,

       Check that:

          - client.get("/") has all form parameters set
          - client.post("/") sets a form parameter

    :param db_app_with_test_data: fixture with data
    """
    with db_app_with_test_data.app_context():
        response = client.get("/hello")
        assert response.data == b"Hello, World!"

        response = client.get("/")
        soup = BeautifulSoup(response.data, "html.parser")
        # print(soup.prettify())
        assert len(soup.find_all(id="form_system_id")) == 1
        assert len(soup.find_all(id="form_sub_system_id")) == 1
        assert len(soup.find_all(id="form_sub_sub_system_id")) == 1
        assert len(soup.find_all(id="form_user_spec_1")) == 1
        assert len(soup.find_all(id="form_user_spec_2")) == 1
        assert len(soup.find_all(id="form_produkt_id")) == 1
        assert len(soup.find_all(id="form_pattern")) == 1
        assert len(soup.find_all(id="form_starting_at")) == 1
        assert len(soup.find_all(id="form_notify_level")) == 1
        assert len(soup.find_all(id="form_num_records")) == 1
        assert len(soup.find_all(id="form_order")) == 1
        assert len(soup.find_all(id="form_input")) == 1

        # print(response.data)

        # define a new form to post
        form = {
            "PRODUKT_ID": "not_selected",
            "SYSTEM_ID": "not_selected",
            "SUB_SYSTEM_ID": "not_selected",
            "SUB_SUB_SYSTEM_ID": "not_selected",
            "USER_SPEC_1": "not_selected",
            "USER_SPEC_2": "not_selected",
            "pattern": "ANewPattern",
            "starting_at": "not_selected",
            "notify_level": "not_selected",
            "max_rows": "not_selected",
            "old_row_first": "not_selected",
        }
        response = client.post("/", data=form)
        soup = BeautifulSoup(response.data, "html.parser")
        # print(soup.prettify())
        pattern_html_form_string = str(soup.find_all(id="form_pattern")[0])
        assert "ANewPattern" in pattern_html_form_string
        # assert False


def test_ps_herald_rm_log(db_app_with_test_data, client):
    """[summary]
       Given a  fixture generating a context with test_data,

       Check that:

          - client.get("/rm_log") deletes sentences
          - it's redirection (to / )  deliveres a
            working form

    :param db_app_with_test_data: fixture with data
    """
    with db_app_with_test_data.app_context():
        session = get_session()
        start_rows = session.query(Log).count()
        print(f"Initially we have {start_rows}")
        response = client.get("/rm_logs", follow_redirects=True)
        soup = BeautifulSoup(response.data, "html.parser")
        # print(soup.prettify())
        assert len(soup.find_all(id="form_system_id")) == 1
        assert len(soup.find_all(id="form_sub_system_id")) == 1
        assert len(soup.find_all(id="form_sub_sub_system_id")) == 1
        assert len(soup.find_all(id="form_user_spec_1")) == 1
        assert len(soup.find_all(id="form_user_spec_2")) == 1
        assert len(soup.find_all(id="form_produkt_id")) == 1
        assert len(soup.find_all(id="form_pattern")) == 1
        assert len(soup.find_all(id="form_starting_at")) == 1
        assert len(soup.find_all(id="form_notify_level")) == 1
        assert len(soup.find_all(id="form_num_records")) == 1
        assert len(soup.find_all(id="form_order")) == 1
        assert len(soup.find_all(id="form_input")) == 1

        fin_rows = session.query(Log).count()
        print(f"After rm_log we have {fin_rows}")
        assert start_rows > fin_rows
        # assert False
