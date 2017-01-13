//============================================================================
// Name        : Server_main.cpp
// Author      : Lihailin
// Version     :
// Copyright   : 
// Description : Server_main in C++, Ansi-style
//============================================================================

#include <iostream>
#include <string>
#include "ServerSocket.h"
#include "SocketException.h"
using namespace std;

int main()
{
    cout<<"Running server..."<<endl;
    try
    {
        ServerSocket server(8080);
        Socket newSocket;
        server.Accept(newSocket);

        while(true)
        {
            try
            {
                string message;
                server.Receive(newSocket,message);
                cout<<"Receive message: "<<message<<endl;
                message="Here is server";
                server.Send(newSocket,message);
            }
            catch(SocketException&){}
        }
    }
    catch(SocketException& ex)
    {
         cout << "Exception was caught:" << ex.Description() << "\nExiting.\n";
    }
    return 0;
}
