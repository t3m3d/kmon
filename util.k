// util.k — timestamp and IP formatting

import "windows.krh"

// Returns timestamp in milliseconds (GetTickCount64 * 1000000 = nanoseconds approx)
func timestampNs() {
    let ms = GetTickCount64()
    emit toInt(ms) * 1000000 + ""
}

func ipToStr(ip) {
    let n = toInt(ip)
    let a = n % 256
    let b = n / 256 % 256
    let c2 = n / 65536 % 256
    let d = n / 16777216 % 256
    emit a + "." + b + "." + c2 + "." + d
}
