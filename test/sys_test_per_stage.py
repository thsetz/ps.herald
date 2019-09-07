import sys
import traceback
from subprocess import Popen, check_call
from os import devnull
import os, sys,time, subprocess,pdb, sqlite3
from ps.Basic import Basic, DEV_STAGES
import signal

bridge_proc, herald_proc = None,None
       
def test(dev_stage):
    try:
         print("DEV_STAGE " + dev_stage)
         Basic.INSTANCE=None
         x=Basic.get_instance("Test_"+dev_stage,guarded_by_lockfile=True)
         print(Basic.herald_sqlite_filename)
         bridge_proc = subprocess.Popen(['nohup', 'ps_bridge','-v'], stdout=open("bridge_log_out"+dev_stage, "w") , stderr=open("bridge_log_err"+dev_stage, "w")  )
         print("bridge started")
         while(not os.path.isfile(Basic.herald_sqlite_filename)):
             print("Datei %s noch nicht da"%(Basic.herald_sqlite_filename))
             time.sleep(1)
         statinfo = os.stat(Basic.herald_sqlite_filename)
        
         while(statinfo.st_size < 1000):
             statinfo = os.stat(Basic.herald_sqlite_filename)
             print("len is %d"%(statinfo.st_size))
             time.sleep(1)

         time.sleep(7)
         herald_proc = Popen(["nohup", "ps_herald"], stdout=open("herald_log_"+dev_stage, "w") , stderr=open("herald_log_err"+dev_stage, "w"))
         print("herald started")
         time.sleep(3)
         con = sqlite3.connect(Basic.herald_sqlite_filename)
         cur = con.cursor()    
         cur.execute('SELECT *from log')
         data = cur.fetchall()
         initial_amount_of_rows = len(data)
         print("There are %d Entries"%(len(data)))
         cur.close()
         del(con) 
     
        
         for i in range(0,100):
            Basic.logger.info("Test %d"%(i))
         time.sleep(10) 

         con2 = sqlite3.connect(Basic.herald_sqlite_filename)
         cur2 = con2.cursor()    
         cur2.execute('SELECT *from log')
         data = cur2.fetchall()
         amount_of_rows = len(data)
         print("There are %d Entries"%(len(data)))
         cur2.close()
         del(con2) 
         if amount_of_rows > initial_amount_of_rows + 99:
               print("EVERYTHING OK")

    finally:
         check_call("ps -ef | grep {} | grep -v grep".format(herald_proc.pid), shell=True)
         check_call("ps -ef | grep {} | grep -v grep".format(bridge_proc.pid), shell=True)
         herald_proc.terminate()
         bridge_proc.terminate()
         check_call("ps -ef | grep {} | grep -v grep".format(herald_proc.pid), shell=True)
         check_call("ps -ef | grep {} | grep -v grep".format(bridge_proc.pid), shell=True)
         time.sleep(7)








    

if __name__ == "__main__":
  test(sys.argv[1])

