// util.k — timestamp and IP formatting

import "windows.krh"

func timestampNs() {
    let freq = structNew("LARGE_INTEGER")
    let counter = structNew("LARGE_INTEGER")
    QueryPerformanceFrequency(freq)
    QueryPerformanceCounter(counter)
    let f = toInt(structGet(freq, "QuadPart"))
    let c = toInt(structGet(counter, "QuadPart"))
    emit (c * 1000000000 / f) + ""
}

func ipToStr(ip) {
    let n = toInt(ip)
    let a = n % 256
    let b = n / 256 % 256
    let c2 = n / 65536 % 256
    let d = n / 16777216 % 256
    emit a + "." + b + "." + c2 + "." + d
}
