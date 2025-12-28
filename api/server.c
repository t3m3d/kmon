#include "server.h"
#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdio.h>

static SOCKET client = INVALID_SOCKET;

int server_start(void) {
    WSADATA wsa;
    WSAStartup(MAKEWORD(2,2), &wsa);

    SOCKET s = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(9000);
    addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    bind(s, (struct sockaddr*)&addr, sizeof(addr));
    listen(s, 1);

    printf("kmon backend: waiting for frontend...\n");
    client = accept(s, NULL, NULL);

    printf("kmon backend: frontend connected.\n");
    return 0;
}

void server_send(const char* msg, size_t len) {
    if (client == INVALID_SOCKET)
        return;

    send(client, msg, (int)len, 0);
}

void server_stop(void) {
    if (client != INVALID_SOCKET) closesocket(client);
    WSACleanup();
}