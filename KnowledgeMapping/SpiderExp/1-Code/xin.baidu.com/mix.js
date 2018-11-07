function mix(tk, bid) {
    var tkLen = tk.length;
    tk = tk.split('');
    var bdLen = bid.length;
    bid = bid.split('');
    for (var i = 0; i < bdLen; i++) {
        bid[i] = parseInt(bid[i]) + parseInt(tkLen - bdLen);
    }
    var one = tk[bid[bdLen - 1]];
    for (var i = bdLen - 1; i >= 0; i -= 1) {
        tk[bid[i]] = tk[bid[i - 1]];
        if ((i - 2) < 0) {
            tk[bid[i - 1]] = one;
            break;
        }
    }
    return tk.join("");
}


var tk = "82vlWR4oaiSw4ymn59ALGH5OXNpyJcxk7wnl";
var baiducode = "464926647992";
r = mix(tk, baiducode);

console.log(r);