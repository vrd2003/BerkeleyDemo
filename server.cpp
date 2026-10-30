#include <iostream>
#include <cstring>
#include <winsock2.h>
#include <ws2tcpip.h>

using namespace std;

#define PORT 5000

int main() {

    // 1. Initialize Winsock
    WSADATA wsaData;

    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        cerr << "WSAStartup failed\n";
        return 1;
    }

    SOCKET serverSocket, clientSocket;
    struct sockaddr_in serverAddr, clientAddr;

    int clientLen = sizeof(clientAddr);

    char buffer[1024];

    // 2. socket()
    serverSocket = socket(AF_INET, SOCK_STREAM, 0);  //For TCP, use SOCK_STREAM and for UDP, use SOCK_DGRAM

    if (serverSocket == INVALID_SOCKET) {
        cerr << "Socket creation failed\n";
        WSACleanup();
        return 1;
    }

    // Server address
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(PORT);

    // 3. bind()
    if (bind(serverSocket,(struct sockaddr*)&serverAddr,sizeof(serverAddr)) == SOCKET_ERROR) {

        cerr << "Bind failed\n";

        closesocket(serverSocket);
        WSACleanup();

        return 1;
    }

    // 4. listen()
    if (listen(serverSocket, 5) == SOCKET_ERROR) {

        cerr << "Listen failed\n";

        closesocket(serverSocket);
        WSACleanup();

        return 1;
    }

    cout << "Server waiting for connection on port " << PORT << "...\n";

    // 5. accept()
    clientSocket = accept(serverSocket,(struct sockaddr*)&clientAddr,&clientLen);

    if (clientSocket == INVALID_SOCKET) {

        cerr << "Accept failed\n";

        closesocket(serverSocket);
        WSACleanup();

        return 1;
    }

    cout << "Client connected!\n";

    // 6. recv()
    memset(buffer, 0, sizeof(buffer));

    int bytesReceived = recv(clientSocket,buffer,sizeof(buffer) - 1,0);

    if (bytesReceived > 0) {

        buffer[bytesReceived] = '\0';

        cout << "Client request: " << buffer << endl;

    } else {

        cerr << "Failed to receive data\n";
    }

    // 7. send()
    string response = "Hello from Server!";

    send(
        clientSocket,
        response.c_str(),
        response.length(),
        0
    );

    cout << "Response sent to client!\n";

    // 8. Close sockets
    closesocket(clientSocket);
    closesocket(serverSocket);

    // 9. Cleanup Winsock
    WSACleanup();

    return 0;
}