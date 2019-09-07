__doc__="""
       This is a wrapper around sys_test_per_stage.py.

       sys_test_per_stage.py   starts a bridge/herald instance and emits logging messages 
       - they should be found within the database.
       This is checked by sys_test_per_stage.py - which will print EVERYTHING OK to stdout if everythin is OK. 
       This is checked here.
       The wrapper (process isolation) was needed because the sql library did not 
       properly close old connections (when called in one process for different database connection)

"""
import traceback
from subprocess import Popen, PIPE, check_call
from os import devnull
import os, sys,time, subprocess,pdb, sqlite3
from ps.Basic import Basic, DEV_STAGES
import signal,sys

def clean_the_playground():
  subprocess.call(['pwd' ] )
  subprocess.call(['/bin/rm -f herald.sqlite*' ],  shell=True )
  subprocess.call(['/bin/rm -f bridge_log*' ],        shell=True )
  subprocess.call(['/bin/rm -f herald_log*' ],        shell=True )
  subprocess.call(['/bin/rm -f *_lock*' ],        shell=True )
  subprocess.call(['/bin/rm -fR LOG' ],        shell=True )
  subprocess.call(['ls -la *herald*' ],            shell=True )


def main():
  """ The documentation """
  clean_the_playground()
  in_error = False
  for dev_stage in DEV_STAGES.keys():
      os.environ["DEV_STAGE"] = dev_stage 
      try:
         p = Popen(["python", "sys_test_per_stage.py", dev_stage], stdout=PIPE, stderr=PIPE )
         (stdout, stderr) = p.communicate()
         
         if b"EVERYTHING OK" not in stdout or p.returncode != 0:
            print("ERROR ON DEV_STAGE %s"%(dev_stage) )
            print(stdout.decode("utf-8") )
            print(stderr.decode("utf-8") )
            print(p.returncode)
            in_error = True
         else:
            print("OK:   DEV_STAGE %s"%(dev_stage) )

      except:
         print("==========================================")
         print("exception")
         print(traceback.format_exc())
  if not os.path.isdir("LOG"):
       print("No LOGS generated ???")
       in_error=True 
  if(in_error): 
          sys.exit(1)
  clean_the_playground()
  sys.exit(0) 

if __name__ == "__main__":
  main()

