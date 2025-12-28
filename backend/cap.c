#include "cap.h"
#include "util.h"
#include <pcap.h>
#include <stdio.h>

static pcap_t* handle = NULL;
static volatile int running = 0;

static void internal_handler(u_char* user, const struct pcap_pkthdr* hdr, const u_char* pkt) {
    cap_packet_cb cb = (cap_packet_cb)user;
    if (cb) cb(pkt, hdr->len);
}

int cap_init(const char* iface) {
    char errbuf[PCAP_ERRBUF_SIZE];

    handle = pcap_open_live(iface, 65536, 1, 1000, errbuf);
    if (!handle) {
        fprintf(stderr, "cap_init: %s\n", errbuf);
        return -1;
    }
    return 0;
}

int cap_set_filter(const char* filter) {
    struct bpf_program fp;

    if (pcap_compile(handle, &fp, filter, 1, PCAP_NETMASK_UNKNOWN) < 0)
        return -1;

    if (pcap_setfilter(handle, &fp) < 0)
        return -1;

    pcap_freecode(&fp);
    return 0;
}

int cap_start(cap_packet_cb callback) {
    running = 1;
    return pcap_loop(handle, 0, internal_handler, (u_char*)callback);
}

void cap_stop(void) {
    running = 0;
    if (handle) pcap_breakloop(handle);
}

void cap_cleanup(void) {
    if (handle) {
        pcap_close(handle);
        handle = NULL;
    }
}