from drozer.modules import Module, common
class OperateMem(Module,common.ClassLoader):
    name = ""
    description = ""
    examples = ""
    author = "Li Hailin (@jbloggs)"
    date = "2017-01-09"
    license = "BSD (3-clause)"
    path = ["xv"]
    
    def add_arguments(self, parser):
        parser.add_argument("-stt","--start",default="8899",help="start the native programe from client")
        #parser.add_argument("-stp","--stop",  help="stop the native programe from client")
        parser.add_argument("-ps","--pids", help="get pids")
        parser.add_argument("-sp","--setpid", help="set pid")
        parser.add_argument("-ms","--maps", help="get maps")
        parser.add_argument("-sm","--search_memory", nargs=2, metavar=("type", "content"), help="specify the content and type values to use when obtaining the message")
        parser.add_argument("-mm","--mand_memory", nargs=3, metavar=( "start_addr", "type","content"), help="specify the content and type values to use when obtaining the message")
        parser.add_argument("-dmp","--dump", nargs=3, metavar=( "start_addr", "end_addr","path"), help="Dump Specifies the memory contents between addresses, which are stored under the specified file")
        

    def execute(self, arguments):
        dextest = self.loadClass("common/native_agent.apk", "native_agent/Nat_conn")
        
        dextest.initData(arguments.start);
        result = dextest.start_native()
        #print result
 
        if arguments.pids!=None:
            result = dextest.run_command("pids")
            print result
        #elif arguments.setpid!=None:
        # result = dextest.run_command("setpid"+arguments.setpid)
        #    print result
        elif arguments.search_memory!=None:
            result = dextest.run_command("setpid "+arguments.setpid)
            result = dextest.run_command("sm "+ arguments.search_memory[0]+" "+ arguments.search_memory[1])
            print result
        elif arguments.mand_memory!=None:
            result = dextest.run_command("setpid "+arguments.setpid)
            result = dextest.run_command("mm "+ arguments.mand_memory[0]+" "+ arguments.mand_memory[1]+ " "+ arguments.mand_memory[2])
            print result
        elif arguments.dump!=None:
            result = dextest.run_command("setpid "+arguments.setpid)
            print result
            result = dextest.run_command("dump "+ arguments.dump[0]+" "+ arguments.dump[1]+ " "+ arguments.dump[2])
            print result
        elif arguments.maps!=None:
            result = dextest.run_command("setpid "+arguments.setpid)
            #print result
            result = dextest.run_command("maps")
            print result
        else:
            result = "..."
            print result
        result = dextest.end_native()
        #print result
