var window = global;
var n = 8;
function u(n, t, u, c, f, o) {
    return a((i = a(a(t, n), a(c, o))) << (h = f) | i >>> 32 - h, u);
    var i, h
}
function c(n, t, c, f, o, a) {
    return u(c & f | ~c & t, n, 0, o, a, 0)
}
function t(n, t) {
    n[t >> 5] |= 128 << t % 32,
    n[14 + (t + 64 >>> 9 << 4)] = t;
    for (var u = 1732584193, i = -271733879, h = -1732584194, v = 271733878, d = 0; d < n.length; d += 16) {
        var l = u
          , A = i
          , _ = h
          , b = v;
        i = o(i = o(i = o(i = o(i = f(i = f(i = f(i = f(i = c(i = c(i = c(i = c(i, h = c(h, v = c(v, u = c(u, i, h, v, n[d + 0], 3), i, h, n[d + 1], 7), u, i, n[d + 2], 11), v, u, n[d + 3], 19), h = c(h, v = c(v, u = c(u, i, h, v, n[d + 4], 3), i, h, n[d + 5], 7), u, i, n[d + 6], 11), v, u, n[d + 7], 19), h = c(h, v = c(v, u = c(u, i, h, v, n[d + 8], 3), i, h, n[d + 9], 7), u, i, n[d + 10], 11), v, u, n[d + 11], 19), h = c(h, v = c(v, u = c(u, i, h, v, n[d + 12], 3), i, h, n[d + 13], 7), u, i, n[d + 14], 11), v, u, n[d + 15], 19), h = f(h, v = f(v, u = f(u, i, h, v, n[d + 0], 3), i, h, n[d + 4], 5), u, i, n[d + 8], 9), v, u, n[d + 12], 13), h = f(h, v = f(v, u = f(u, i, h, v, n[d + 1], 3), i, h, n[d + 5], 5), u, i, n[d + 9], 9), v, u, n[d + 13], 13), h = f(h, v = f(v, u = f(u, i, h, v, n[d + 2], 3), i, h, n[d + 6], 5), u, i, n[d + 10], 9), v, u, n[d + 14], 13), h = f(h, v = f(v, u = f(u, i, h, v, n[d + 3], 3), i, h, n[d + 7], 5), u, i, n[d + 11], 9), v, u, n[d + 15], 13), h = o(h, v = o(v, u = o(u, i, h, v, n[d + 0], 3), i, h, n[d + 8], 9), u, i, n[d + 4], 11), v, u, n[d + 12], 15), h = o(h, v = o(v, u = o(u, i, h, v, n[d + 2], 3), i, h, n[d + 10], 9), u, i, n[d + 6], 11), v, u, n[d + 14], 15), h = o(h, v = o(v, u = o(u, i, h, v, n[d + 1], 3), i, h, n[d + 9], 9), u, i, n[d + 5], 11), v, u, n[d + 13], 15), h = o(h, v = o(v, u = o(u, i, h, v, n[d + 3], 3), i, h, n[d + 11], 9), u, i, n[d + 7], 11), v, u, n[d + 15], 15),
        u = a(u, l),
        i = a(i, A),
        h = a(h, _),
        v = a(v, b)
    }
    return Array(u, i, h, v)
}


function f(n, t, c, f, o, a) {
    return u(t & c | t & f | c & f, n, 0, o, a, 1518500249)
}
function o(n, t, c, f, o, a) {
    return u(t ^ c ^ f, n, 0, o, a, 1859775393)
}
function a(n, t) {
    var u = (65535 & n) + (65535 & t);
    return (n >> 16) + (t >> 16) + (u >> 16) << 16 | 65535 & u
}
function i(t) {
    for (var u = Array(), c = 0; c < t.length * n; c += n)
        u[c >> 5] |= (255 & t.charCodeAt(c / n)) << c % 32;
    return u
}


function h(n) {
    for (var t = "", u = 0; u < 4 * n.length; u++)
        t += "0123456789abcdef".charAt(n[u >> 2] >> u % 4 * 8 + 4 & 15) + "0123456789abcdef".charAt(n[u >> 2] >> u % 4 * 8 & 15);
    return t
}

function  get_sign(page) {
    var xxxxx = (new Date).getTime();
    var mmm = page+ ":" + xxxxx;
    var rest= h(t(i(mmm), mmm.length * n));
    return xxxxx + "-" + rest
}


