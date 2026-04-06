// kmon_utils.k — string field helpers + hex parsing

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

// Convert single hex character to decimal value
func hexCharVal(c) {
    if c == "0" { emit "0" }
    if c == "1" { emit "1" }
    if c == "2" { emit "2" }
    if c == "3" { emit "3" }
    if c == "4" { emit "4" }
    if c == "5" { emit "5" }
    if c == "6" { emit "6" }
    if c == "7" { emit "7" }
    if c == "8" { emit "8" }
    if c == "9" { emit "9" }
    if c == "a" { emit "10" }
    if c == "b" { emit "11" }
    if c == "c" { emit "12" }
    if c == "d" { emit "13" }
    if c == "e" { emit "14" }
    if c == "f" { emit "15" }
    if c == "A" { emit "10" }
    if c == "B" { emit "11" }
    if c == "C" { emit "12" }
    if c == "D" { emit "13" }
    if c == "E" { emit "14" }
    if c == "F" { emit "15" }
    emit "0"
}

// Convert hex string to decimal integer string
func hexToDec(hex) {
    let result = 0
    let i = 0
    while i < len(hex) {
        let c = substring(hex, i, i + 1)
        result = result * 16 + toInt(hexCharVal(c))
        i += 1
    }
    emit result + ""
}

// Read 1-byte value from hex packet data at byte offset
func capByte(hex, offset) {
    let hoff = toInt(offset) * 2
    if hoff + 2 > len(hex) { emit "0" }
    emit hexToDec(substring(hex, hoff, hoff + 2))
}

// Read 2-byte big-endian value from hex packet data at byte offset
func capU16(hex, offset) {
    let hoff = toInt(offset) * 2
    if hoff + 4 > len(hex) { emit "0" }
    emit hexToDec(substring(hex, hoff, hoff + 4))
}

// Read 4-byte big-endian value from hex packet data at byte offset
func capU32(hex, offset) {
    let hoff = toInt(offset) * 2
    if hoff + 8 > len(hex) { emit "0" }
    emit hexToDec(substring(hex, hoff, hoff + 8))
}
