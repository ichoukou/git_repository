#include "tools.h"
#include "pidtools.h"
#include "msg_handle.h"
#include "memopt_b.h"
#include "memopt.h"
//#include <unistd.h>
#include "./socket/jni/SocketException.h"
#include "./socket/jni/ServerSocket.h"



int main(int argc,char *argv[])
{
	
	int port;
	if (argc < 2)
	{
		cout<<"Insufficient parameters,press any key to exit..."<<endl;
		getchar();
		return 0;
	}	
	else 
	{
		string par1 = argv[1];
		if (par1 == "start") 
		{
			if(argc == 3)
				port = string_o_types::stoi(argv[2]);
			else 
			{
				cout<<"Too many parameters,press any key to exit..."<<endl;
				getchar();
				return 0;
			}
		}
		else 
		{
			cout<<"Insufficient parameters,press any key to exit..."<<endl;
			getchar();
			return 0;
		}
	}
	cout<<"native start success..."<<endl;
	
    try
    {
        ServerSocket server(port);
        Socket newSocket;
        server.Accept(newSocket);//waiting client to connect
        server.Send(newSocket, "CLIENT_CONNECT_SUCCESS\n");//send a connect success message 
        cout<<"CLIENT_CONNECT_SUCCESS"<<endl;

        msg_handle msg = msg_handle();
        
        int faile_time = 0;
        while(true)
        {
			string message = "";
			server.Receive(newSocket,message);
			//cout<<"ffffffffffffffffff"<<endl;
			//message = message.substr(0,message.length()-1);
			
			vector< string > msg_vect;
			string_rlv::split(message, " ", &msg_vect);
			vector<string>::iterator iter = msg_vect.begin();
			
			if(*iter == "endserver") 
			{
				cout<<"ENDSERVER_SUCCESS\n";
				server.Send(newSocket, "ENDSERVER_SUCCESS\n");
				//sleep(2000);
				return 0;
			}
			else if(*iter == "setpid" && msg_vect.size() == 2)
			{
				msg.set_pid(string_o_types::stoi(*(iter+1)));
				server.Send(newSocket, "SETPID_SUCCESS\n");
			}
				
			else if(*iter == "dump" && msg_vect.size() == 4)
			{
				if(msg.msg_hangle_(msg_vect))
				{
					server.Send(newSocket, "DUMP_SUCCESS\n");
				}
				else
					server.Send(newSocket, "DUMP_FAIL\n");
			}
			else if(*iter == "mm" && msg_vect.size() == 4)
			{
				if(msg.msg_hangle_(msg_vect))
				{
					server.Send(newSocket, "MM_SUCCESS\n");
				}
				else
					server.Send(newSocket, "MM_FAIL\n");
			}
			else if(*iter == "maps" && msg_vect.size() == 1)
			{
				
				if(msg.msg_hangle_(msg_vect))
				{
					string msg_s = msg.maps_ret +"SUCCESS\n";
					server.Send(newSocket, msg_s);
					//cout<<msg.maps_ret<<endl;
				}
				else 
					server.Send(newSocket, "MAPS_FAIL\n");
			}
			else if(*iter == "pids" && msg_vect.size() == 1)
			{
				if(msg.msg_hangle_(msg_vect))
				{
					server.Send(newSocket, msg.pid_ret+"SUCCESS\n");
					//cout<<msg.pid_ret;
				}	
				else
					server.Send(newSocket, "PIDS_FAIL\n");
			}
			else if(*iter == "sm" && msg_vect.size() == 3)
			{
				if(msg.msg_hangle_(msg_vect))
				{
					string mg = "";
					for (vector<long>::iterator iter = msg.ret_addr.begin(); iter!= msg.ret_addr.end(); iter++)
					{
						mg += string_o_types::ltohs(*iter)+"|";
						//cout<< *iter<<endl;
					}
					server.Send(newSocket, mg+"SUCCESS\n");
				}
				else
					server.Send(newSocket, "SM_FAIL\n");
			}else
			{
				faile_time++;
				server.Send(newSocket, (*iter)+" COMMAND_FAIL\n");
				//cout<<"COMMAND_FAIL"<<endl;
				if(faile_time>=10)
					break;
			}      
        }
    }
    catch(SocketException& ex)
    {
         cout << "Exception was caught:" << ex.Description() << "\nExiting.\n";
    }
    return 0;
}
