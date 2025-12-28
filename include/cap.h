#ifndef CAP_H
#define CAP_H

#include <stdint.h>
#include <stddef.h>

// Callback type for delivering raw packets to the parser
typedef void (*cap_packet_cb)(const uint8_t* data, size_t len);

// Initialize capture on a given interface
int cap_init(const char* iface);

// Set a BPF filter (e.g., "tcp", "udp", "port 53")
int cap_set_filter(const char* filter);

// Start capture loop (blocking)
int cap_start(cap_packet_cb callback);

// Stop capture loop
void cap_stop(void);

// Cleanup resources
void cap_cleanup(void);

#endif