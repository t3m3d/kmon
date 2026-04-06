// stats.k — packet statistics tracking
// State passed explicitly as "total,tcp,udp,icmp,bytesDown,lastTimeMs"

func statsInit(tsNow) {
    emit "0,0,0,0,0," + tsNow
}

func statField(state, idx) {
    let s = state
    let i = 0
    while i < toInt(idx) {
        let pos = indexOf(s, ",")
        if pos < 0 { emit "" }
        s = substring(s, pos + 1, len(s))
        i += 1
    }
    let pos = indexOf(s, ",")
    if pos < 0 { emit s }
    emit substring(s, 0, pos)
}

func statsUpdate(state, protocol, length) {
    let total     = toInt(statField(state, "0")) + 1
    let tcp       = toInt(statField(state, "1"))
    let udp       = toInt(statField(state, "2"))
    let icmp      = toInt(statField(state, "3"))
    let bytesDown = toInt(statField(state, "4")) + toInt(length)
    let lastTime  = statField(state, "5")

    if protocol == "6"  { tcp  = tcp  + 1 }
    if protocol == "17" { udp  = udp  + 1 }
    if protocol == "1"  { icmp = icmp + 1 }

    emit total + "," + tcp + "," + udp + "," + icmp + "," + bytesDown + "," + lastTime
}

func formatMbps(kbpsH) {
    let whole = toInt(kbpsH) / 100000
    let frac  = toInt(kbpsH) / 100 - whole * 1000
    let fracStr = frac + ""
    while len(fracStr) < 3 { fracStr = "0" + fracStr }
    emit whole + "." + fracStr
}

// Returns "newState|mbps,total,tcp,udp,icmp"
func statsSnapshot(state, tsNow) {
    let total     = statField(state, "0")
    let tcp       = statField(state, "1")
    let udp       = statField(state, "2")
    let icmp      = statField(state, "3")
    let bytesDown = toInt(statField(state, "4"))
    let lastTime  = toInt(statField(state, "5"))

    let elapsedMs = (toInt(tsNow) - lastTime) / 1000000
    let mbpsStr = "0.000"
    if elapsedMs > 0 {
        let kbpsH = bytesDown * 800000 / toInt(elapsedMs)
        mbpsStr = formatMbps(kbpsH + "")
    }

    let newState  = total + "," + tcp + "," + udp + "," + icmp + ",0," + tsNow
    let snap      = mbpsStr + "," + total + "," + tcp + "," + udp + "," + icmp
    emit newState + "|" + snap
}
