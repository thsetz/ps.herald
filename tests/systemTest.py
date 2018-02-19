import future        # pip install future
import builtins      # pip install future
import past          # pip install future
import six           # pip install six

import os, time, subprocess,pdb, sqlite3
from ps.Basic import Basic, DEV_STAGES
import signal




def main():
  """ The documentation """
  for dev_stage in DEV_STAGES.keys():
      os.environ["DEV_STAGE"] = dev_stage 
      subprocess.call(['pwd' ] )
      subprocess.call(['/bin/rm -f herald.sqlite*' ],  shell=True )
      subprocess.call(['/bin/rm -f *_lock_*' ],        shell=True )
      subprocess.call(['ls -la *herald*' ],            shell=True )
      try:
         print("DEV_STAGE " + dev_stage)
         herald_proc = subprocess.Popen(['ps_herald'],  shell=True  )
         #pdb.set_trace()
         time.sleep(7)
         bridge_proc = subprocess.Popen(['ps_bridge'], shell=True  )
         time.sleep(3)
         #pdb.set_trace()
         x=Basic("Test",guarded_by_lockfile=True)
         con = sqlite3.connect(Basic.herald_sqlite_filename)
         cur = con.cursor()    
         cur.execute('SELECT *from log')
         data = cur.fetchall()
         print("There are %d Entries"%(len(data)))
     
         for i in range(0,4):
            Basic.logger.info("Test %d"%(i))
         time.sleep(2) 

         cur.execute('SELECT *from log')
         data = cur.fetchall()
         print("There are %d Entries"%(len(data)))
         #print data 
         #pdb.set_trace()
         #Basic.__del__(1,2,3)
      finally:
         os.kill(herald_proc.pid,signal.SIGKILL)
         os.kill(bridge_proc.pid,signal.SIGKILL)


  




if __name__ == "__main__":
  main()





