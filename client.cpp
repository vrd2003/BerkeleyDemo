#include <iostream>
#include <cstring>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "ws2_32.lib")

using namespace std;

#define PORT 5000

int main() {

    // 1. Initialize Winsock
    WSADATA wsaData;

    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        cerr << "WSAStartup failed\n";
        return 1;
    }

    SOCKET clientSocket;
    struct sockaddr_in serverAddr;
    char buffer[1024];

    // 2. socket()
    clientSocket = socket(AF_INET, SOCK_STREAM, 0);

    if (clientSocket == INVALID_SOCKET) {
        cerr << "Socket creation failed\n";
        WSACleanup();
        return 1;
    }

    // Server address
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(PORT);

    // Convert IP address
    inet_pton(AF_INET, "127.0.0.1", &serverAddr.sin_addr);

    // 3. connect()
    if (connect(clientSocket,(struct sockaddr*)&serverAddr,sizeof(serverAddr)) == SOCKET_ERROR) {

        cerr << "Connection failed\n";

        closesocket(clientSocket);
        WSACleanup();

        return 1;
    }

    cout << "Connected to server!\n";

    // 4. send()
    string message = "Hello from Client!";

    send(
        clientSocket,
        message.c_str(),
        message.length(),
        0
    );

    cout << "Message sent to server!\n";

    // 5. receive()
    memset(buffer, 0, sizeof(buffer));

    int bytesReceived = recv(clientSocket,buffer,sizeof(buffer) - 1,0);

    if (bytesReceived > 0) {
        buffer[bytesReceived] = '\0';
        cout << "Server reply: " << buffer << endl;
    }
    else {
        cout << "No response received from server.\n";
    }

    // 6. Close socket
    closesocket(clientSocket);

    // 7. Cleanup Winsock
    WSACleanup();

    return 0;
}