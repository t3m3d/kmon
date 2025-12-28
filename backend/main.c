#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>

#include "cap.h"
#include "par.h"
#include "stats.h"
#include "protocol.h"
#include "server.h"
#include "util.h"

static int running = 1;

// Called by cap.c for every captured packet
static void packet_callback(const uint8_t* data, size_t len) {
    packet_info_t pkt;

    // Parse raw packet
    if (par_parse(data, len, &pkt) == 0) {
        // Update statistics
        stats_update(&pkt);

        // Serialize packet JSON
        char json[512];
        size_t n = proto_packet_json(&pkt, json, sizeof(json));

        // Send to frontend
        server_send(json, n);
    }
}

// Sends stats snapshot every second
static void send_stats_loop(void) {
    static uint64_t last = 0;
    uint64_t now = util_timestamp_ns();

    if ((now - last) >= 1000000000ULL) { // 1 second
        last = now;

        stats_snapshot_t snap;
        stats_get(&snap);

        char json[512];
        size_t n = proto_stats_json(&snap, json, sizeof(json));

        server_send(json, n);
    }
}

static void handle_sigint(int sig) {
    running = 0;
    cap_stop();
    server_stop();
}

int main(int argc, char** argv) {
    printf("kmon backend starting...\n");

    if (argc < 2) {
        printf("Usage: %s <network-interface>\n", argv[0]);
        return 1;
    }

    const char* iface = argv[1];

    signal(SIGINT, handle_sigint);

    // Start TCP server for frontend
    if (server_start() != 0) {
        fprintf(stderr, "Failed to start server\n");
        return 1;
    }

    // Initialize statistics engine
    stats_init();

    // Initialize packet capture
    if (cap_init(iface) != 0) {
        fprintf(stderr, "Failed to initialize capture on %s\n", iface);
        return 1;
    }

    // cap_set_filter("tcp");

    printf("Capturing on interface: %s\n", iface);
    printf("Press Ctrl+C to stop.\n");

    // Start capture loop (blocking)
    while (running) {
        cap_start(packet_callback);
        send_stats_loop();
    }

    printf("Shutting down...\n");

    cap_cleanup();
    server_stop();

    return 0;
}