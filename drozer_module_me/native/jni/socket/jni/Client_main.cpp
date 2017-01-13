//============================================================================
// Name        : Client_main.cpp
// Author      : Lihailin
// Version     :
// Copyright   : 
// Description : Client_main in C++, Ansi-style
//============================================================================
#include <iostream>
#include <string>
#include "stdio.h"
#include "stdlib.h"
#include "ClientSocket.h"
#include "SocketException.h"
using namespace std;

int main(int argc,char *argv[])
{
    cout<<"Running client...."<<endl;
    try
    {
        ClientSocket clientSocket("127.0.0.1",atoi(argv[1]));//connect server
		string message;
		clientSocket.Receive(message);
		cout<<"Response from server: "<<message<<endl;
		
        while(true)
        {
			string sendMSG;
			cout<<"input a message to send: ";
			getline(cin,sendMSG);
     		clientSocket.Send(sendMSG);
			clientSocket.Receive(message);
			cout<<"Response from server: "<<message<<endl;
		}
    }
    catch(SocketException& ex)
    {
        cout << "Exception was caught:" << ex.Description() << "\n";
    }
    return 0;
}
