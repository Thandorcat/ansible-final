from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.callback import CallbackBase
from termcolor import colored, cprint

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


sun = '''  
   \   / 
    .-.  
 --(   )--  
    '-' 
   /   \ '''   
     
clouds ='''
    \  /   
  _ /"".-.             
    \_(   ).        
    /(___(__) '''

storm = '''
   .-.             
 _(   ).        
(___(__)
  \ \ \ 
'''

cloud = '''
   .-.             
 _(   ).        
(___(__)
'''

delimiter = "="*50 + "\n"

class CallbackModule(CallbackBase):

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'demo'

    def show(self, task, host, result, caption):
        buf = " {0} issued on {1} {2}".format(task, host, caption)
        stdout = result.get('stdout', '')
        stderr = result.get('stderr', '')
        msg = result.get('msg', '')
        print(delimiter)
        print(buf + "\n")
        if (len(stdout) > 0):
            print("Stdout: " + stdout)
        if (len(stderr) > 0):
            print("Stderr: " + stderr)
        if (len(msg) > 0):
            print("Msg: " + msg)
        if display.verbosity >= 2 :
            print("Full result:" + str(result))

        print("\n")


    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.show(result._task, result._host.get_name(), result._result, storm)

    def v2_runner_on_ok(self, result):
        self.show(result._task, result._host.get_name(), result._result, sun)

    def v2_runner_on_skipped(self, result):
        self.show(result._task, result._host.get_name(), result._result, clouds)

    def v2_runner_on_unreachable(self, result):
        self.show(result._task, result._host.get_name(), result._result, cloud)
