#ifndef SOCKET_H
#define SOCKET_H

#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string>
#include <unistd.h>

const int MAXCONNECTION=5;
const int MAXRECEIVE = 5000*10;

class Socket
{
    public:
        Socket();
        //virtual destructior
        virtual ~Socket();

        // Server initialization
        bool Create(); //create a socket
        bool Bind(const int port);
        bool Listen() const;
        bool Accept(Socket& clientSocket) const;

        // Client initialization
        bool Connect(const std::string& host,const int port);

        // Data Transmission
        bool Send(Socket& socket,const std::string& message) const;
        int Receive(Socket& socket,std::string& message) const;

        void SetNonBlocking(const bool flag);
        bool IsValid() const;
        //bool SocketConnected(int sock) const;

    private:
        //use m_sockfd to record the result of function socket
        int m_sockfd;
        struct sockaddr_in m_address;
};

#endif
