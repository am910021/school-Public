$("#createCode").on('click', function(e) {
	var num=32;
    var sp = [33, 64, 35, 36, 37, 94, 38, 42, 95, 43, 45, 61];
    var n = 0,
        l = 0,
        u = 0,
        s = 0,
        i = 0;
    var t = "";
    var m = Math.floor(num / 4);
    while (true) {
        var r = randint(1, 4);
        if (r == 1 && (n < m || i > 0)) {
            n++;
            t += String.fromCharCode(randint(48, 57));
        }
        if (r == 2 && (l < m || i > 0)) {
            l++;
            t += String.fromCharCode(randint(97, 122));
        }
        if (r == 3 && (u < m || i > 0)) {
            u++;
            t += String.fromCharCode(randint(65, 90));
        }
        if (r == 4 && (s < m || i > 0)) {
            s++;
            t += String.fromCharCode(sp[randint(1, 11)]);
        }
        if (n + l + u + s >= m * 4)
            i++;
        if (n + l + u + s >= num)
            break
    }
    document.getElementById("id_key").value = t;
});

function randint(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}