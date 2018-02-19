__doc__="""
  Herald is a webserver displaying log messages.  The log messages are stored within a database.

  Usage:

	          ps_herald  [-t] [-v] [-d]

  Options:

     -h, --help        Show this screen.
     -d, --debug       debug mode 
     -v, --verbose     verbose mode 

"""
import os,time,datetime,sys,traceback
import docopt
from socket import gethostname
from sqlalchemy.sql import or_
from . import herald_package_version
from flask import Flask, render_template,request, session, redirect, url_for, abort
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap

from flask import render_template, redirect, request, url_for, flash

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import LoginManager, UserMixin
from threading import Timer, Thread
from time import sleep

from ps.Basic import Basic
HOSTNAME=gethostname()
VERBOSE    = False
TEST_ONLY  = False 
DEBUG      = False 
herald_app = Flask(__name__)
db=SQLAlchemy(herald_app)
#leave_a_reference_for_garbage_collection_here = Basic("herald", guarded_by_lockfile = True)
Basic("herald" )
Basic.logger.debug("started", extra={"package_version":herald_package_version.version})
if Basic.dev_stage=="TESTING":
   herald_app.config['TESTING']=True
   herald_app.config['WTF_CSRF_ENABLED'] = False
#   herald_app.config['DEBUG']=True


herald_app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'hard to guess string'
herald_app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + Basic.herald_sqlite_filename
sys.stdout.write(herald_app.config['SQLALCHEMY_DATABASE_URI'])
#DEBUG
#herald_app.config['SERVER_NAME']="localhost:5000"
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view         = 'login'
bootstrap = Bootstrap()
bootstrap.init_app(herald_app)
login_manager.init_app(herald_app)


###################Start Models########################
class Log(db.Model):
 """The model currently is build around the data structure, the standard python logging mechanism
   uses to send logging Events across the **class logging.StreamHandler()**.
 """
 __tablename__ = 'log'
 __table_args__ = {'sqlite_autoincrement': True} # needed for sqlite. needed for pg ?
 id                = db.Column(db.Integer,primary_key=True)
 created           = db.Column(db.String())     #:e.g. 2015-01-08 10:52:41 currently the time the record is created in the 
                                                #bridge as string sqlite does not support datetime per se here, that is, why the 
                                                #string representation was choosen.
 threadname        = db.Column(db.String())     #:e.g. MainThread
 api_version       = db.Column(db.String())     #:e.g. 1.2.44 
 package_version   = db.Column(db.String())     #:e.g. The version of the module where logging appeared 
 name              = db.Column(db.String())     #:e.g. Tests
 relativecreated   = db.Column(db.Float())      #:e.g. 10.5919839592
 process           = db.Column(db.Integer)      #:e.g. 896
 args              = db.Column(db.String())     #:e.g. None
 module            = db.Column(db.String())     #:e.g. t
 funcname          = db.Column(db.String())     #:e.g. run
 levelno           = db.Column(db.Integer)      #:e.g. 40
 processname       = db.Column(db.String())     #:MainProcess
 thread            = db.Column(db.BigInteger)   #:e.g. 140735286908888
 msecs             = db.Column(db.Float())      #:e.g. 616.5919839592
 message           = db.Column(db.String())     #:e.g. "The msg of a log.info statement"
 exc_text          = db.Column(db.String())     #:e.g. None
 exc_info          = db.Column(db.String())     #:e.g. None
 stack_info        = db.Column(db.String())     #:e.g. None
 pathname          = db.Column(db.String())     #:e.g. /Users/setzt/Haufe/basic_package
 filename          = db.Column(db.String())     #:e.g. Basic.py
 asctime           = db.Column(db.String())     #:e.g. ???? 
 levelname         = db.Column(db.String())     #:INFO
 lineno            = db.Column(db.Integer)      #:e.g. 42
 # These are "extra fields" not in the standard python logging
 produkt_id        = db.Column(db.String(10))   #:e.g. PRODUKT_ID
 system_id         = db.Column(db.String(10))   #:e.g. SYSTEM_ID 
 sub_system_id     = db.Column(db.String(10))   #:e.g. SUB_SYSTEM_ID 
 sub_sub_system_id = db.Column(db.String(10))   #:e.g. SUB_SUB_SYSTEM_ID 
 user_spec_1       = db.Column(db.String(10))   #:e.g. User_specific_value_one
 user_spec_2       = db.Column(db.String(10))   #:e.g. User_specific_value_two
 summary           = db.Column(db.String(70))   #:e.g. concatenation of the before values






 def __repr__(self):
  d={}
  d['created']             = self.created
  d['package_version']     = self.package_version
  d['module']              = self.module
  d['lineno']              = self.lineno
  d['funcname']            = self.funcname
  try:    d['lower_levelname']     = self.levelname.lower()
  except: d['lower_levelname']     = str(self.levelno)

  d['levelname']           = self.levelname
  d['message']             = self.message
  d['exc_text']            = self.exc_text
  d['stack_info']          = self.stack_info
  d['system_id']           = self.system_id
  d['sub_system_id']       = self.sub_system_id
  d['sub_sub_system_id']   = self.sub_sub_system_id
  d['user_spec_1']         = self.user_spec_1
  d['user_spec_2']         = self.user_spec_2
  d['produkt_id']          = self.produkt_id

  return '<tr class="%(lower_levelname)s"> \
                           <td>%(created)s</td> \
                           <td>%(levelname)s</td> \
                           <td>%(system_id)s<br>%(sub_system_id)s<br>%(sub_sub_system_id)s</td> \
                           <td>%(produkt_id)s<br>%(user_spec_1)s<br>%(user_spec_2)s</td>\
                           <td>%(module)s %(package_version)s<br>%(funcname)s<br>line: %(lineno)s<br></td> \
                           <td>%(message)s</td> \
                           <td>%(exc_text)s</td> \
                           <td>%(stack_info)s</td> \
                           </tr>'%d





class User(UserMixin, db.Model):
    """Describe the users having access to the monitor"""
    __tablename__ = "users"
     
    id              = db.Column(db.Integer,      primary_key=True)
    email           = db.Column(db.String(64),   unique=True     )
    password_hash   = db.Column(db.String(128)                   )

    @property
    def password(self):
        raise AttributeError('password is not an readable Attribute')
   
    @password.setter
    def password(self,password_p):
        self.password_hash = generate_password_hash(password_p)

    def verify_password(self,password_p):
        return check_password_hash(self.password_hash, password_p)

    
    def __repr__(self):
          return '<User: %r' % self.email

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    
class HeartBeat(db.Model):
 """Store the HeartBeat of the different systems """
 __tablename__ = 'heartbeat'
 __table_args__ = {'sqlite_autoincrement': True} # needed for sqlite. needed for pg ?

 id                = db.Column(db.Integer,primary_key=True)
 newest_heartbeat  = db.Column(db.String())     #:e.g. 2015-01-08 10:52:41 
 system_id         = db.Column(db.String(10),unique=True)   #:e.g. SYSTEM_ID 
   
 def __repr__(self):
     return '<system_id: %r <heartbeat: %r' % (self.system_id, self.newest_heartbeat)

###################Fin Models########################
###################Start Forms ########################
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
class LoginForm(FlaskForm):
 """Standard Login Form"""
 email       = StringField('Email', validators=[Required(), Length(1, 64), Email()])
 password    = PasswordField('Password', validators=[Required()])
 remember_me = BooleanField('Keep me logged in')
 submit      = SubmitField('Log In')
###################Fin Forms ########################

sys.stdout.write ("\nFile is " + Basic.herald_sqlite_filename)

if not os.path.isfile(Basic.herald_sqlite_filename):
  sys.stdout.write("herald will initialize database")
  try:
     db.create_all()
     u=User(email="a@b.ch", password= "c")
     db.session.add(u)
     log=Log(produkt_id="None",system_id="None",sub_system_id="None",sub_sub_system_id="None",user_spec_1="None",
             user_spec_2="None",summary="None")
     db.session.add(log)

     db.session.commit()
     sys.stdout.write("herald database initialized")
  except:
     #db.session.rollback()
     sys.stdout.write(traceback.format_exc())
     Basic.logger.exception("error init database", extra={"package_version":herald_package_version.version})
     sys.exit(1)
else:
  sys.stdout.write("herald will reuse existing database file")
  

###################Start Views########################
@herald_app.route('/hello_world')
def hello_world():

    return 'Hello World!'

#================START AUTHENTICATION VIEWS =======================
from flask.ext.login import login_user, logout_user, login_required, \
    current_user

@herald_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@herald_app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))
#================Fin AUTHENTICATION VIEWS =======================
@herald_app.route('/',methods=['GET', 'POST'])
@herald_app.route('/index',methods=['GET', 'POST'])
#@login_required #
def index():
    """ Handle the html-request"""
    import pdb
    
#    pdb.set_trace()

    #                                              hosts in the haufe-net all start 
    #                                              with vl_, we do not need a login here
    dev_stage=Basic.dev_stage

    if  not current_user.is_authenticated and not HOSTNAME.startswith("vl-") :
        return herald_app.login_manager.unauthorized()
  
    Basic.logger.debug("web interface got a request", extra={"package_version":herald_package_version.version})
    if not 'pattern'      in session:
                             session["pattern"]      = ""
    if not 'starting_at'  in session:
                             session["starting_at"]   = \
                                                      str(datetime.datetime.now() + \
                                                          datetime.timedelta(days=-5)) # Five days before Today 
    if not 'notify_level' in session:
                             session["notify_level"] = 30 #30 is error
    if not 'max_rows'     in session:
                             session["max_rows"]     = 1000
    if not 'old_row_first'in session:
                             session["old_row_first"]= 1
    if not 'PRODUKT_ID'        in session:     session["PRODUKT_ID"]        = "None"
    if not 'SYSTEM_ID'         in session:     session["SYSTEM_ID"]         = "None"
    if not 'SUB_SYSTEM_ID'     in session:     session["SUB_SYSTEM_ID"]     = "None"
    if not 'SUB_SUB_SYSTEM_ID' in session:     session["SUB_SUB_SYSTEM_ID"] = "None"
    if not 'USER_SPEC_1'       in session:     session["USER_SPEC_1"]       = "None"
    if not 'USER_SPEC_2'       in session:     session["USER_SPEC_2"]       = "None"

    if request.method == 'POST':
        session["pattern"]           = request.form['pattern'].strip()
        session["starting_at"]       = request.form['starting_at'].strip()
        session["notify_level"]      = request.form['notify_level']
        session["max_rows"]          = request.form['max_rows']
        session["old_row_first"]     = request.form['old_row_first']
        session["PRODUKT_ID"]               = request.form['PRODUKT_ID'].strip()
        session["SYSTEM_ID"]         = request.form['SYSTEM_ID'].strip()
        session["SUB_SYSTEM_ID"]     = request.form['SUB_SYSTEM_ID'].strip()
        session["SUB_SUB_SYSTEM_ID"] = request.form['SUB_SUB_SYSTEM_ID'].strip()
        session["USER_SPEC_1"]       = request.form['USER_SPEC_1'].strip()
        session["USER_SPEC_2"]       = request.form['USER_SPEC_2'].strip()
    pattern           = session["pattern"]
    starting_at       = session["starting_at"]
    notify_level      = session["notify_level"]
    max_rows          = session["max_rows"]
    old_row_first     = session['old_row_first']
    PRODUKT_ID               = session["PRODUKT_ID"]
    SYSTEM_ID         = session["SYSTEM_ID"]
    SUB_SYSTEM_ID     = session["SUB_SYSTEM_ID"]
    SUB_SUB_SYSTEM_ID = session["SUB_SUB_SYSTEM_ID"]
    USER_SPEC_1       = session["USER_SPEC_1"]
    USER_SPEC_2       = session["USER_SPEC_2"]
    if int(old_row_first) == 1:  user_interface_time_order_of_rows="asc"
    else:                        user_interface_time_order_of_rows="desc"
    
    def isset(param1,param2):
       """jinjas equalto did not work at this point in time. So this wrapper function
          enables the jinja-template do check if a value within a option was selected
          by the user interface.
          If another way is found to set an <option> value im the jinja template,
          this workaround should be eliminated.
       """
       if str(param1)==str(param2):
             return {"value":param1,"selected":True}
       return {"value":param1,"selected":False}

    unset={'selected': False, 'value': 'None'}
    sset ={'selected': True, 'value': 'None'}
    # The kind, how values for the userinterface are choosen is computing intensive - but generic
    # I am no t quite shure if this approach satisfies future performance requirements
    # An easy way to eliminate the queries (on each call) would be to define the
    # values in a config file.
    pid_query         = db.session.query(Log.produkt_id.distinct().label("produkt_id"))
    pids              = [ isset(row.produkt_id,PRODUKT_ID)                              for row in pid_query.all() ]
    sid_query         = db.session.query(Log.system_id.distinct().label("system_id"))
    system_ids        = [ isset(row.system_id,SYSTEM_ID)                  for row in sid_query.all() ]
    sub_sid_query     = db.session.query(Log.sub_system_id.distinct().label("sub_system_id"))
    sub_system_ids    = [ isset(row.sub_system_id,SUB_SYSTEM_ID)          for row in sub_sid_query.all() ]
    sub_sub_sid_query = db.session.query(Log.sub_sub_system_id.distinct().label("sub_sub_system_id"))
    sub_sub_system_ids= [ isset(row.sub_sub_system_id, SUB_SUB_SYSTEM_ID) for row in sub_sub_sid_query.all() ]
    u1_query          = db.session.query(Log.user_spec_1.distinct().label("user_spec_1"))
    user_spec_1_ids   = [ isset(row.user_spec_1,USER_SPEC_1)              for row in u1_query.all() ]
    u2_query          = db.session.query(Log.user_spec_2.distinct().label("user_spec_2"))
    user_spec_2_ids   = [ isset(row.user_spec_2,USER_SPEC_2)              for row in u2_query.all() ]

    #print sid_query.all()
    #print system_ids 
   
    records = Log.query.filter(
                        Log.created  >=  session["starting_at"],
                        Log.levelno  >=  int(session["notify_level"]),
                        Log.module.like("%"+session["pattern"]+"%"),
                        Log.summary.like("%"+session["PRODUKT_ID"]+"%"),
                        Log.summary.like("%"+session["SYSTEM_ID"]+"%"),
                        Log.summary.like("%"+session["SUB_SYSTEM_ID"]+"%"),
                        Log.summary.like("%"+session["SUB_SUB_SYSTEM_ID"]+"%"),
                        Log.summary.like("%"+session["USER_SPEC_1"]+"%"),
                        Log.summary.like("%"+session["USER_SPEC_2"]+"%"),
                        or_(Log.message.like("%"+session["pattern"]+"%"),
                                Log.module.like("%"+session["pattern"]+"%"),
                                Log.funcname.like("%"+session["pattern"]+"%")
                                ),
                      ).order_by("created %s"%(user_interface_time_order_of_rows)).limit(int(session["max_rows"])).all()
    num_records = len(records)
    return render_template("index.html", **locals())


@herald_app.route('/reset_database',methods=[ 'GET'])
@login_required
def reset_database():
    start_date = str(datetime.datetime.now() -  datetime.timedelta(days=30)) # 30 days before Today 
    to_del = Log.query.filter(Log.created < start_date).delete()
    return "OK: %s rows deleted"%(to_del)

@herald_app.route('/shutdown')
def server_shutdown():
   shutdown = request.environ.get('werkzeug.server.shutdown')
   if not shutdown: abort(500)
   shutdown()
   return "Shutting down server"

 
###################Fin Views########################

def main():
    
    global  VERBOSE, TEST_ONLY, DEBUG
    options = docopt.docopt(__doc__, version=1 )
    if options["-v"]: VERBOSE    = True
    if options["-d"]: DEBUG      = True
    if options["-t"]:
         VERBOSE    = True
         TEST_ONLY  = True
    

    herald_app.run(host="0.0.0.0", port=Basic.webserver_port, debug=DEBUG)
    sys.stdout.write("FINISHED HERALD")
    Basic.logger.debug("Exit Now ", extra={"package_version":herald_package_version.version})
    sys.exit(0)

if __name__ == '__main__':
  main()




