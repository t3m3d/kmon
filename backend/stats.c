#include "stats.h"
#include "util.h"
#include "par.h"
#include <string.h>
#include <stdint.h>

#ifdef __linux__
#include <dirent.h>
#endif

// Internal counters
static uint64_t last_time = 0;
static uint64_t bytes_down = 0;
static uint64_t bytes_up = 0;

static uint64_t tcp = 0, udp = 0, icmp = 0;
static uint64_t total = 0;

// VPN Detection
static void detect_vpn(vpn_info_t* out) {
    memset(out, 0, sizeof(*out));

#ifdef __linux__
    DIR* d = opendir("/sys/class/net");
    if (!d) {
        return;
    }

    struct dirent* entry;
    while ((entry = readdir(d)) != NULL) {
        const char* name = entry->d_name;

        if (name[0] == '.') continue;

        // WireGuard
        if (strncmp(name, "wg", 2) == 0) {
            out->active = 1;
            strcpy(out->type, "WireGuard");
            strcpy(out->iface, name);
            break;
        }

        // OpenVPN / generic tun/tap
        if (strncmp(name, "tun", 3) == 0 || strncmp(name, "tap", 3) == 0) {
            out->active = 1;
            strcpy(out->type, "OpenVPN");
            strcpy(out->iface, name);
            break;
        }

        // Tailscale
        if (strcmp(name, "tailscale0") == 0) {
            out->active = 1;
            strcpy(out->type, "Tailscale");
            strcpy(out->iface, name);
            break;
        }

        // ZeroTier
        if (strncmp(name, "zt", 2) == 0) {
            out->active = 1;
            strcpy(out->type, "ZeroTier");
            strcpy(out->iface, name);
            break;
        }

        // ProtonVPN
        if (strncmp(name, "pvpn", 4) == 0) {
            out->active = 1;
            strcpy(out->type, "ProtonVPN");
            strcpy(out->iface, name);
            break;
        }

        // NordVPN (WireGuard)
        if (strcmp(name, "nordlynx") == 0) {
            out->active = 1;
            strcpy(out->type, "NordVPN");
            strcpy(out->iface, name);
            break;
        }

        // Mullvad (WireGuard or OpenVPN)
        if (strstr(name, "mullvad") != NULL) {
            out->active = 1;
            strcpy(out->type, "Mullvad");
            strcpy(out->iface, name);
            break;
        }

        // Tor (rare tun interfaces)
        if (strcmp(name, "tor0") == 0 ||
            strcmp(name, "anon0") == 0 ||
            strcmp(name, "tunTor") == 0) {
            out->active = 1;
            strcpy(out->type, "Tor");
            strcpy(out->iface, name);
            break;
        }
    }

    closedir(d);

#else
    // Windows stub
    out->active = 0;
#endif
}

// Stats Core
void stats_init(void) {
    last_time = util_timestamp_ns();
}

void stats_update(const packet_info_t* pkt) {
    total++;

    switch (pkt->protocol) {
        case 6:  tcp++;  break;
        case 17: udp++;  break;
        case 1:  icmp++; break;
    }

    // TODO: Determine direction (up/down)
    bytes_down += pkt->length;
}

void stats_get(stats_snapshot_t* out) {
    memset(out, 0, sizeof(*out));

    uint64_t now = util_timestamp_ns();
    double seconds = (now - last_time) / 1e9;

    out->mbps_down = (bytes_down * 8.0) / (seconds * 1e6);
    out->mbps_up   = (bytes_up   * 8.0) / (seconds * 1e6);

    out->total_packets = total;
    out->tcp_count = tcp;
    out->udp_count = udp;
    out->icmp_count = icmp;

    // Add VPN info
    detect_vpn(&out->vpn);

    // Reset counters for next interval
    bytes_down = bytes_up = 0;
    last_time = now;
}