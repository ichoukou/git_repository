from drozer.modules import Module, common
class TestCommand(Module,common.ClassLoader):
    name = ""
    description = ""
    examples = ""
    author = "Joe Bloggs (@jbloggs)"
    date = "2012-12-21"
    license = "BSD (3-clause)"
    path = ["xv", "s"]
    def execute(self, arguments):
        in_shell = True
        command = ""
        dextest = self.loadClass("common/native_agent.apk", "native_agent/Nat_conn")
        self.stdout.write("\n>>>")
        while in_shell:
            command = raw_input()
            if command == 'pids':
                result = dextest.run_command(command)
                print result
            elif command[0:5] == 'start':
                dextest.initData(command[6:]);
                result = dextest.start_native()
                print result
                #self.stdout.write('sm end')
            elif command[0:3] == 'end':
                result = dextest.end_native()
                print result
            elif command[0:6] == 'setpid' or command[0:2] == 'mm' or command[0:2] == 'sm' or command[0:4] == 'maps':
                #print command
                result = dextest.run_command(command)
                print result				
            if not in_shell:
                break
            self.stdout.write("\n>>>")


