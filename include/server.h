#ifndef SERVER_H
#define SERVER_H

#include <stddef.h>

// Start the TCP server (listens on 127.0.0.1:9000)
// Returns 0 on success, nonzero on failure.
int server_start(void);

// Stop the TCP server and close sockets.
void server_stop(void);

// Send a JSON message to the connected frontend.
void server_send(const char* data, size_t len);

#endif