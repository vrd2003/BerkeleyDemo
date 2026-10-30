# Berkeley Socket Programming – TCP & UDP Demonstration

## 📌 Overview

This project demonstrates network communication using socket programming in Python and C++. It explores the working of TCP and UDP protocols through client-server applications.

The project implements message exchange, arithmetic and trigonometric calculations, and file transfer to understand how data is transmitted between devices over a network.

## 🎯 Objectives

- Understand the fundamentals of Berkeley Socket Programming.
- Implement client-server communication using TCP and UDP.
- Explore socket creation, binding, listening, accepting, sending, and receiving.
- Understand reliable and connectionless data transmission.
- Demonstrate file transfer using network sockets.
- Compare socket programming implementations in Python and C++.

## 🛠️ Technologies Used

- **Programming Languages:** Python, C++
- **Networking:** TCP, UDP
- **Libraries:** Python `socket`, `math`, `os`, `json`, `struct`; C++ Winsock2
- **Platform:** Windows

## 📂 Project Structure

```text
BerkeleyDemo/
│
├── client.cpp
├── server.cpp
│
├── client.py
├── server.py
│
├── sender.py
├── receiver.py
│
├── client.exe
└── server.exe
```

## ⚙️ Features

### 1. TCP Client-Server Communication
- Establishes a reliable connection between client and server.
- Exchanges messages using TCP sockets.
- Supports a greeting message between client and server.

### 2. Arithmetic Calculator
- Performs addition, subtraction, multiplication, and division.
- Sends mathematical expressions from the client to the server.
- Returns calculated results to the client.

### 3. Trigonometric Calculator
- Supports sine, cosine, and tangent operations.
- Accepts angles in degrees.
- Processes calculations on the server and returns results.

### 4. TCP File Transfer
- Transfers files between client and server.
- Uses file size information to manage data transmission.
- Saves received files on the server.

### 5. UDP File Transfer
- Demonstrates connectionless communication using UDP.
- Transfers files in smaller data chunks.
- Uses sequence numbers and acknowledgements to support reliable delivery.
- Implements timeout and retransmission mechanisms.

## 🚀 How to Run

### Prerequisites
- Python 3.x
- C++ compiler supporting Winsock2
- Windows operating system

### Running the Python TCP Application

**Terminal 1 – Start the server:**

```bash
python server.py
```

**Terminal 2 – Start the client:**

```bash
python client.py
```

Follow the menu displayed on the client to test messaging, file transfer, and calculator operations.

### Running the Python UDP Application

**Terminal 1 – Start the receiver:**

```bash
python receiver.py
```

**Terminal 2 – Start the sender:**

```bash
python sender.py
```

Enter the receiver's IPv4 address and the paths of the files to transfer.

### Running the C++ Application

Compile using a Windows C++ compiler with Winsock2 support.

```bash
g++ server.cpp -o server.exe -lws2_32
g++ client.cpp -o client.exe -lws2_32
```

Run the server first, followed by the client.

## 📚 Concepts Demonstrated

- Socket creation and configuration
- IP addressing and port numbers
- TCP connection-oriented communication
- UDP connectionless communication
- Client-server architecture
- Data transmission and reception
- File handling and transfer
- Acknowledgement and retransmission
- Winsock and Berkeley socket concepts

## 🎓 Learning Outcomes

Through this project, we gain practical knowledge of network programming and understand how applications communicate over computer networks. It provides hands-on experience with TCP and UDP protocols, socket operations, file transfer, and client-server architecture.

## 🏁 Conclusion

The Berkeley Socket Programming demonstration successfully illustrates the practical implementation of TCP and UDP communication using Python and C++. By implementing messaging, mathematical operations, and file transfer, the project provides a better understanding of network communication, reliability, and data transmission mechanisms.

---

**Repository:** [BerkeleyDemo – GitHub](https://github.com/vrd2003/BerkeleyDemo.git)
