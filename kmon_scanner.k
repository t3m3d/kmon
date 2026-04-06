// kmon_scanner.k — Network scanner in Krypton
// Replaces network_scanner.py — outputs JSON array of devices to stdout
// Usage: kmon_scanner.exe

import "winsock.krh"

// ── String helpers ────────────────────────────────────────────────

func firstpart(s, delim) {
    let pos = indexOf(s, delim)
    if pos < 0 { emit s }
    emit substring(s, 0, pos)
}

func afterpart(s, delim) {
    let pos = indexOf(s, delim)
    if pos < 0 { emit "" }
    emit substring(s, pos + len(delim), len(s))
}

func trimStr(s) {
    emit trim(s)
}

func containsStr(s, sub) {
    if indexOf(s, sub) >= 0 { emit "1" }
    emit "0"
}

// ── IP helpers ────────────────────────────────────────────────────

func getLocalIp() {
    let output = shellRun("ipconfig")
    let localIp = ""
    let inWifi = "0"
    let lineIdx = 0
    let lineCount = 0

    // Count lines
    let i = 0
    while i < len(output) {
        if substring(output, i, i+1) == "\n" { lineCount += 1 }
        i += 1
    }
    lineCount += 1

    i = 0
    while i < lineCount {
        let line = trimStr(nthLine(output, i + ""))
        if containsStr(line, "Wireless LAN adapter Wi-Fi") == "1" { inWifi = "1" }
        if inWifi == "1" {
            if containsStr(line, "IPv4 Address") == "1" {
                let colon = indexOf(line, ": ")
                if colon >= 0 {
                    localIp = trimStr(substring(line, colon + 2, len(line)))
                }
            }
        }
        i += 1
    }

    // Fallback: any IPv4 line
    if localIp == "" {
        i = 0
        while i < lineCount {
            let line = trimStr(nthLine(output, i + ""))
            if containsStr(line, "IPv4 Address") == "1" {
                let colon = indexOf(line, ": ")
                if colon >= 0 {
                    localIp = trimStr(substring(line, colon + 2, len(line)))
                    break
                }
            }
            i += 1
        }
    }

    emit localIp
}

func getGateway() {
    let output = shellRun("ipconfig")
    let gw = ""
    let lineCount = 0
    let i = 0
    while i < len(output) {
        if substring(output, i, i+1) == "\n" { lineCount += 1 }
        i += 1
    }
    lineCount += 1
    i = 0
    while i < lineCount {
        let line = trimStr(nthLine(output, i + ""))
        if containsStr(line, "Default Gateway") == "1" {
            let colon = indexOf(line, ": ")
            if colon >= 0 {
                let candidate = trimStr(substring(line, colon + 2, len(line)))
                if candidate != "" && candidate != "0.0.0.0" { gw = candidate }
            }
        }
        i += 1
    }
    emit gw
}

// ── ARP table ─────────────────────────────────────────────────────

// Returns newline-separated "ip|mac" pairs from arp -a
func getArpTable() {
    let output = shellRun("arp -a")
    let result = ""
    let lineCount = 0
    let i = 0
    while i < len(output) {
        if substring(output, i, i+1) == "\n" { lineCount += 1 }
        i += 1
    }
    lineCount += 1
    i = 0
    while i < lineCount {
        let line = trimStr(nthLine(output, i + ""))
        // Lines look like: "  192.168.1.1   aa-bb-cc-dd-ee-ff  dynamic"
        // First field = IP, second = MAC
        let parts = line
        // Skip header/empty lines
        if len(line) < 20 {
            i += 1
            continue
        }
        // Extract IP (first word)
        let spacePos = indexOf(parts, " ")
        if spacePos < 0 {
            i += 1
            continue
        }
        let ip = substring(parts, 0, spacePos)
        // Validate looks like an IP
        if containsStr(ip, ".") == "0" {
            i += 1
            continue
        }
        // Extract MAC (second non-space field)
        let rest = trimStr(substring(parts, spacePos, len(parts)))
        let macEnd = indexOf(rest, " ")
        let mac = rest
        if macEnd >= 0 { mac = substring(rest, 0, macEnd) }
        // Skip broadcast/invalid
        if mac == "ff-ff-ff-ff-ff-ff" || mac == "00-00-00-00-00-00" {
            i += 1
            continue
        }
        if containsStr(mac, "-") == "1" {
            if result != "" { result = result + "\n" }
            result = result + ip + "|" + mac
        }
        i += 1
    }
    emit result
}

// ── Hostname resolution ───────────────────────────────────────────

func resolveHost(ip) {
    // Use nslookup — works without admin
    let out = shellRun("nslookup " + ip)
    let lineCount = 0
    let i = 0
    while i < len(out) {
        if substring(out, i, i+1) == "\n" { lineCount += 1 }
        i += 1
    }
    lineCount += 1
    i = 0
    while i < lineCount {
        let line = trimStr(nthLine(out, i + ""))
        if containsStr(line, "Name:") == "1" {
            let colon = indexOf(line, ":")
            if colon >= 0 {
                emit trimStr(substring(line, colon + 1, len(line)))
            }
        }
        i += 1
    }
    emit "Unknown"
}

// ── Line reader helper ────────────────────────────────────────────

func nthLine(s, idx) {
    let target = toInt(idx)
    let cur = 0
    let start = 0
    while "1" == "1" {
        let nlPos = indexOf(substring(s, start, len(s)), "\n")
        if nlPos < 0 {
            if cur == target { emit trim(substring(s, start, len(s))) }
            emit ""
        }
        if cur == target { emit trim(substring(s, start, start + nlPos)) }
        start = start + nlPos + 1
        cur += 1
    }
    emit ""
}

// ── JSON builder ──────────────────────────────────────────────────

func deviceJson(ip, mac, hostname) {
    emit "{\"ip\":\"" + ip + "\",\"mac\":\"" + mac + "\",\"hostname\":\"" + hostname + "\"}"
}

// ── Main ──────────────────────────────────────────────────────────

just run {
    let localIp = getLocalIp()
    let gateway = getGateway()

    // Ping broadcast to populate ARP cache
    shellRun("ping -n 1 -w 100 255.255.255.0")

    let arpTable = getArpTable()
    let lineCount = 0
    let i = 0
    while i < len(arpTable) {
        if substring(arpTable, i, i+1) == "\n" { lineCount += 1 }
        i += 1
    }
    if arpTable != "" { lineCount += 1 }

    let json = "["
    let first = "1"

    // Add local machine
    if localIp != "" {
        let hostname = shellRun("hostname")
        hostname = trim(hostname)
        if first == "0" { json = json + "," }
        json = json + deviceJson(localIp, "local", hostname)
        first = "0"
    }

    // Add gateway
    if gateway != "" && gateway != localIp {
        if first == "0" { json = json + "," }
        json = json + deviceJson(gateway, "gateway", "Default Gateway")
        first = "0"
    }

    // Add ARP entries
    i = 0
    while i < lineCount {
        let entry = nthLine(arpTable, i + "")
        if entry != "" {
            let ip = firstpart(entry, "|")
            let mac = afterpart(entry, "|")
            if ip != localIp && ip != gateway {
                let hostname = resolveHost(ip)
                if first == "0" { json = json + "," }
                json = json + deviceJson(ip, mac, hostname)
                first = "0"
            }
        }
        i += 1
    }

    json = json + "]"
    kp(json)
    emit 0
}
