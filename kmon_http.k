// kmon_http.k — HTTP + SSE server (winsock2)
//
// Serves kmonHttpInit's HTML payload on :8080, streams events on /events.
// Implementation lives in a `cfunc` block below so the kmon source tree
// stays all-Krypton. Link line is supplied by build.bat (-lws2_32).

jxt {
    func kmonHttpInit(htmlPath)
    func kmonHttpPoll()
    func kmonHttpBroadcast(data)
    func kmonHttpStop()
}

cfunc {
    #include <winsock2.h>
    #include <windows.h>
    #include <stdio.h>
    #include <string.h>
    #include <stdlib.h>

    #define KMON_HTTP_PORT 8080
    #define KMON_SSE_MAX_CLIENTS 8

    static SOCKET kmon_http_sock    = INVALID_SOCKET;
    static SOCKET kmon_sse_clients[KMON_SSE_MAX_CLIENTS];
    static int    kmon_sse_count    = 0;
    static char   kmon_html_buf[1024*512];
    static int    kmon_html_len     = 0;

    char* kmonHttpInit(char* htmlPath) {
        FILE* f = fopen(htmlPath, "rb");
        if (!f) { fprintf(stderr, "kmon_http: cannot open %s\n", htmlPath); return (char*)"0"; }
        kmon_html_len = (int)fread(kmon_html_buf, 1, sizeof(kmon_html_buf)-1, f);
        fclose(f);
        kmon_html_buf[kmon_html_len] = 0;

        WSADATA wsa;
        WSAStartup(MAKEWORD(2,2), &wsa);

        kmon_http_sock = socket(AF_INET, SOCK_STREAM, 0);
        int opt = 1;
        setsockopt(kmon_http_sock, SOL_SOCKET, SO_REUSEADDR, (char*)&opt, sizeof(opt));

        struct sockaddr_in addr;
        memset(&addr, 0, sizeof(addr));
        addr.sin_family      = AF_INET;
        addr.sin_port        = htons(KMON_HTTP_PORT);
        addr.sin_addr.s_addr = inet_addr("127.0.0.1");

        bind(kmon_http_sock, (struct sockaddr*)&addr, sizeof(addr));
        listen(kmon_http_sock, 8);

        u_long nb = 1;
        ioctlsocket(kmon_http_sock, FIONBIO, &nb);

        memset(kmon_sse_clients, 0xFF, sizeof(kmon_sse_clients));
        kmon_sse_count = 0;

        fprintf(stderr, "kmon: HTTP UI on http://127.0.0.1:%d\n", KMON_HTTP_PORT);
        return (char*)"1";
    }

    static void kmon_http_handle(SOCKET client) {
        char req[4096] = {0};
        recv(client, req, sizeof(req)-1, 0);

        int is_sse  = (strstr(req, "GET /events") != NULL);
        int is_root = (strstr(req, "GET / ") != NULL || strstr(req, "GET /index") != NULL);

        if (is_sse) {
            const char* hdr =
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/event-stream\r\n"
                "Cache-Control: no-cache\r\n"
                "Access-Control-Allow-Origin: *\r\n"
                "Connection: keep-alive\r\n\r\n";
            send(client, hdr, (int)strlen(hdr), 0);

            u_long nb = 1;
            ioctlsocket(client, FIONBIO, &nb);

            if (kmon_sse_count < KMON_SSE_MAX_CLIENTS) {
                kmon_sse_clients[kmon_sse_count++] = client;
            } else {
                closesocket(client);
            }
        } else if (is_root) {
            char hdr[256];
            snprintf(hdr, sizeof(hdr),
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                "Content-Length: %d\r\n"
                "Connection: close\r\n\r\n",
                kmon_html_len);
            send(client, hdr, (int)strlen(hdr), 0);
            send(client, kmon_html_buf, kmon_html_len, 0);
            closesocket(client);
        } else {
            const char* r404 = "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n";
            send(client, r404, (int)strlen(r404), 0);
            closesocket(client);
        }
    }

    char* kmonHttpPoll(void) {
        if (kmon_http_sock == INVALID_SOCKET) return (char*)"";
        SOCKET c = accept(kmon_http_sock, NULL, NULL);
        while (c != INVALID_SOCKET) {
            kmon_http_handle(c);
            c = accept(kmon_http_sock, NULL, NULL);
        }
        return (char*)"";
    }

    char* kmonHttpBroadcast(char* data) {
        if (kmon_sse_count == 0) return (char*)"";
        char msg[1024*64];
        int mlen = snprintf(msg, sizeof(msg), "data: %s\n", data);

        int i = 0;
        while (i < kmon_sse_count) {
            int r = send(kmon_sse_clients[i], msg, mlen, 0);
            if (r == SOCKET_ERROR) {
                closesocket(kmon_sse_clients[i]);
                kmon_sse_clients[i] = kmon_sse_clients[--kmon_sse_count];
            } else {
                i++;
            }
        }
        return (char*)"";
    }

    char* kmonHttpStop(void) {
        int i;
        for (i = 0; i < kmon_sse_count; i++) closesocket(kmon_sse_clients[i]);
        kmon_sse_count = 0;
        if (kmon_http_sock != INVALID_SOCKET) { closesocket(kmon_http_sock); kmon_http_sock = INVALID_SOCKET; }
        WSACleanup();
        return (char*)"";
    }
}
