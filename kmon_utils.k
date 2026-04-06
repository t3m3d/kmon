// kmon_utils.k — string field helpers

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
