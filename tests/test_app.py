import unittest, os,sys
from ps.herald import herald_app, db, User, Log
from flask import url_for
import  os,time
from ps.Basic import Basic
import subprocess,signal,os


import future        # pip install future
import builtins      # pip install future
import past          # pip install future
import six           # pip install six
import pytest

basedir = os.path.abspath(os.path.dirname(__file__))
USER="user@company.de"
PASS="cat"


class herald_TestCase(unittest.TestCase):
    def setUp(self):
        self.app = herald_app
        self.app.config['TESTING']=True
        #self.app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir, 'test.sqlite_d')
        #self.app.config['SQLALCHEMY_ECHO']=True
        self.app.config['SERVER_NAME']="localhost:5000"
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        try:
          u=User(email=USER, password= PASS)
          db.session.add(u)
          log=Log(produkt_id="None",system_id="None",sub_system_id="None",sub_sub_system_id="None",user_spec_1="None",
             user_spec_2="None",summary="None")
          db.session.add(log)
          db.session.commit()
        except:
          db.session.rollback()
          raise
          pass

        self.post_dict={ "pattern":"pattern", 
                         "starting_at":"starting_at", 
                         "notify_level":"30",\
                         "max_rows":"10", 
                         "old_row_first":"1", 
                         "PRODUKT_ID":"PRODUKT_ID", \
                         "SYSTEM_ID":"SYSTEM_ID", 
                         "SUB_SYSTEM_ID":"SUB_SYSTEM_ID",\
                         "SUB_SUB_SYSTEM_ID":"SUB_SUB_SYSTEM_ID", 
                         "USER_SPEC_1":"USER_SPEC_1",\
                         "USER_SPEC_2":"USER_SPEC_2",}
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self):
        """
             - Login to the server (with the in SetUp created User.
             - check that we get a good looking table
             - log out
             - check, that we are on the login page again
        """
        response = self.client.get(url_for('index'))
        sys.stdout.write(response.data)
        response2 = self.client.post(url_for('login'), data={
            'email': USER,
            'password': PASS
        }, follow_redirects=True)
        sys.stdout.write(response2.data)
        self.assertTrue('Logging Server Status Page'.encode("utf-8") in response2.data)
        #self.assertTrue('Module'    in response2.data)
        #self.assertTrue('App' in response2.data)



class FirstTest(herald_TestCase):

    def test_app_exists(self):
        self.assertFalse(self.app is None)

    def test_app_is_testing(self):
        self.assertTrue(self.app.config['TESTING'])


class First_ClientTest(herald_TestCase):
    def test_a(self):
      response = self.client.get(url_for('hello_world'))
      assert("Hello".encode("utf-8")  in response.data) 

class First_dbTest(herald_TestCase):
    def test_a(self):
      response = self.client.get(url_for('hello_world'))
      assert("Hello".encode("utf-8")  in response.data) 

class UserModelTestCase(herald_TestCase):
    def test_password_setter(self):
        u = User( password = "cat")
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User( password = "cat")
        with self.assertRaises(AttributeError):
          u.password

    def test_password_verification(self):
        u = User( password = "cat")
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User( password = "cat")
        u2 = User( password = "cat")
        self.assertTrue(u.password_hash != u2.password_hash)



class UserLoginLogouTestCase(herald_TestCase):

    def test_login(self):
        self.login()
        pass

    def test_logout(self):
        self.login()
        response = self.client.get(url_for('logout'), follow_redirects=True)
        self.assertTrue('Keep me logged in'.encode("utf-8")  in response.data)

class UICheck(herald_TestCase):
    #XXX TBD define more tests here e.g. make shure the state of the form is maintained for all
    # session variables 
    def test_grep(self):
        self.login()
        impossible="An Sring which for shure is not in the template".encode("utf-8") 
        self.post_dict["pattern"]=impossible
        response = self.client.post("/",data=self.post_dict ,follow_redirects=True)
        print("===================================")
        print(response.data)
        print("===================================")
        #self.assertTrue(impossible in response.data)
      

class HomepageCheck(herald_TestCase):
    def test_home_page2(self):
        """ """
        self.login()
        response = self.client.get("/",follow_redirects=True)
        self.assertTrue('Date'.encode("utf-8")       in response.data)
        self.assertTrue('Level'.encode("utf-8")      in response.data)
        self.assertTrue('System'.encode("utf-8")    in response.data)
        self.assertTrue('App'.encode("utf-8")   in response.data)
        self.assertTrue('Module'.encode("utf-8")      in response.data)
        self.assertTrue('Exception'.encode("utf-8")      in response.data)



class herald_SysTestCase(herald_TestCase):
    def setUp(self):
        super(herald_SysTestCase, self).setUp() 
        # Put the new logging values first
        os.environ['SYSTEM_ID']="SYSTEM_ID"
        os.environ['SUB_SYSTEM_ID']="SUB_SYSTEM_ID"
        os.environ['SUB_SUB_SYSTEM_ID']="SUB_SUB_SYSTEM_ID"
        os.environ['PRODUKT_ID']="PRODUKT_ID"
        os.environ['USER_SPEC_1']="USER_SPEC_1"
        os.environ['USER_SPEC_2']="USER_SPEC_2"
        os.environ['DEV_STAGE']="TESTING"
        Basic("Tests")
        if os.path.isfile( Basic.herald_sqlite_filename):
           os.remove(Basic.herald_sqlite_filename)         
        #get the eggs into path:
        NEW_PYTHONPATH=""
        base=os.getcwd()
        try:
         for egg in os.listdir("eggs"):
           NEW_PYTHONPATH += ":" + os.path.join(base,"eggs",egg)
        except:
          pass
        old_path=os.environ.get("PYTHONPATH","")
        os.environ["PYTHONPATH"] = old_path + NEW_PYTHONPATH
        sys.stdout.write(os.environ["PYTHONPATH"])


    def tearDown(self):
        sys.stdout.write("Kill "+str(self.bridge_proc.pid))
        os.kill(self.bridge_proc.pid,signal.SIGTERM)
        sys.stdout.write("Kill "+str(self.herald_proc.pid))
        os.kill(self.herald_proc.pid,signal.SIGTERM)
        super(herald_SysTestCase, self).tearDown() 







#class FirstSysTest(herald_SysTestCase): 
#   """ Check, that messages created with logging are found in the sqlite database.
#       Bridge does not delete .... """   
#   def setUp(self):
#        super(FirstSysTest, self).setUp() 
#        time.sleep(3)
#        subprocess.Popen(['rm','-f','herald.sqlite_t' ] )
#
#        self.herald_proc = subprocess.Popen(['ps_herald' ] )
#        time.sleep(3)
#        self.bridge_proc = subprocess.Popen(['ps_bridge' ] )
#        time.sleep(2)
#
#   def test_if_messages_are_inserted_into_the_database(self):
#     self.login()
#     response = self.client.get(url_for('logout'), follow_redirects=True)
#     self.assertTrue('Keep me logged in' in response.data)
#     Basic.logger.info("HURZ")
#     Basic.logger.info("HURZ")
#     Basic.logger.info("HURZ")
#     Basic.logger.info("HURZ")
#     time.sleep(5)
#     #db.session.commit() # This will create a new transaction, thereby deleting the "cache"
#     records = db.session.query(Log).all()
#     sys.stdout.write("===============")
#     sys.stdout.write("Number of Records is " +str( len(records) ))
#     pytest.set_trace() 
#     sys.stdout.write(str(records) )
#     sys.stdout.write("===============")
#     self.assertTrue( len(records) >= 4)
#     self.assertTrue( len(records) < 15)
#     for record in records:
#       if record.system_id == "None": continue   #skip entry inserted on startup  needed for UI
#       self.assertTrue(record.system_id   in ["Tests","herald","bridge"]) # The param to the Basic Class
#        #currently the SUB_SYSTEM_ID is overwritten by "hostname"
#        # maybe this will be introduced later, when a better distinction between TESTING Stage and
#        # DEVELOPMENT is done.
#       self.assertFalse(record.sub_system_id    == "SUB_SYSTEM_ID" )# should be overwritten by the class
#       self.assertEqual(record.sub_sub_system_id, "SUB_SUB_SYSTEM_ID" )
#       self.assertEqual(record.user_spec_1       , "USER_SPEC_1" )
#       self.assertEqual(record.user_spec_2       , "USER_SPEC_2" )
#       self.assertEqual(record.pid               , "PID" )
#
#   def tearDown(self):
#        super(FirstSysTest, self).tearDown() 
#         
#class SecondSysTest(herald_SysTestCase): 
#   """ Check, that messages created with logging are found in the sqlite database.
#       Bridge does delete ....  ( -s 1 ==> older one second / -r 1 ==> check every round"""   
#   def setUp(self):
#        super(SecondSysTest, self).setUp() 
#        self.bridge_proc = subprocess.Popen(['ps_bridge' ,'-v' , '-s 1','-r 1'] )
#        self.herald_proc = subprocess.Popen(['ps_herald' ] )
#        time.sleep(5)
#   def test_that_not_all_messages_are_inserted_into_the_database(self):
#     self.login()
#     response = self.client.get(url_for('logout'), follow_redirects=True)
#     self.assertTrue('Keep me logged in' in response.data)
#     Basic.logger.info("HURZ")
#     Basic.logger.info("HURZ")
#     Basic.logger.info("HURZ")
#     Basic.logger.info("HURZ")
#     time.sleep(5)
#     db.session.commit() # This will create a new transaction, thereby deleting the "cache"
#     Basic.logger.info("The new message") # This will make the bridge to delete old messages
#     time.sleep(2)
#     records = db.session.query(Log).all()
#     sys.stdout.write("===============")
#     sys.stdout.write("Number of Records with deleting bridge is " +str( len(records) ))
#     sys.stdout.write("===============")
#     self.assertTrue( len(records) <= 4)
#     self.assertTrue( len(records) > 0)
#     for record in records:
#       if record.system_id == "None": continue   #skip entry inserted on startup  needed for UI
#       self.assertTrue(record.system_id   in ["Tests","herald","bridge"]) # The param to the Basic Class
#        #currently the SUB_SYSTEM_ID is overwritten by "hostname"
#        # maybe this will be introduced later, when a better distinction between TESTING Stage and
#        # DEVELOPMENT is done.
#       self.assertFalse(record.sub_system_id    == "SUB_SYSTEM_ID" )# should be overwritten by the class
#       self.assertEqual(record.sub_sub_system_id, "SUB_SUB_SYSTEM_ID" )
#       self.assertEqual(record.user_spec_1       , "USER_SPEC_1" )
#       self.assertEqual(record.user_spec_2       , "USER_SPEC_2" )
#       self.assertEqual(record.pid               , "PID" )
#         
#   def tearDown(self):
#        super(SecondSysTest, self).tearDown() 

