// stats.k — packet statistics tracking

let statTotal    = "0"
let statTcp      = "0"
let statUdp      = "0"
let statIcmp     = "0"
let statBytesDown = "0"
let statLastTime = "0"

func statsInit(tsNow) {
    statTotal     = "0"
    statTcp       = "0"
    statUdp       = "0"
    statIcmp      = "0"
    statBytesDown = "0"
    statLastTime  = tsNow
    emit ""
}

func statsUpdate(protocol, length) {
    statTotal     = toInt(statTotal) + 1 + ""
    statBytesDown = toInt(statBytesDown) + toInt(length) + ""
    if protocol == "6"  { statTcp  = toInt(statTcp)  + 1 + "" }
    if protocol == "17" { statUdp  = toInt(statUdp)  + 1 + "" }
    if protocol == "1"  { statIcmp = toInt(statIcmp) + 1 + "" }
    emit ""
}

// Returns "mbps_down,total,tcp,udp,icmp" and resets interval counters
func statsSnapshot(tsNow) {
    let elapsed = toInt(tsNow) - toInt(statLastTime)
    let mbpsDown = "0.000"
    if elapsed > 0 {
        let bits = toInt(statBytesDown) * 8
        let mbps = bits / (elapsed / 1000000)
        let whole = mbps / 1000
        let frac  = mbps - whole * 1000
        mbpsDown  = whole + "." + frac
    }
    let result = mbpsDown + "," + statTotal + "," + statTcp + "," + statUdp + "," + statIcmp
    statBytesDown = "0"
    statLastTime  = tsNow
    emit result
}
