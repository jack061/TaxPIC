//===========replace jquery ....===========
var jQuery = {}

jQuery.extend = function(fs){

	for (f in fs){
		Object.defineProperty(jQuery, f, {
                value: fs[f]
            })
	}

}

//==========t.q.e.min===========

!
function(t) {
	var r = new Array(1, 3, 7, 10, 11, 12, 17),
	n = new Array(1, 3, 5, 7, 9, 10, 14, 16, 22),
	o = new Array(1, 5, 10, 17, 22, 24, 28),
	e = new Array(1, 3, 7, 11, 12, 16, 17),
	i = new Array(1, 3, 7, 11, 12, 15, 16),
	g = new Array(1, 3, 5, 7, 8, 11, 13),
	a = new Array(1, 3, 7, 11, 12, 15, 16),
	S = new Array(1, 10, 11, 20, 24, 28),
	s = new Array(1, 2),
	l = new Array("01", "02", "03", "04", "10", "11", "14", "15"),
	p = function(t) {
		return "01" == t ? r: "02" == t ? n: "03" == t ? o: "04" == t ? e: "10" == t ? i: "11" == t ? g: "14" == t ? a: "15" == t ? S: s
	},
	u = function(r, n) {
		var o = r.split("≡");
		return t.encrypt(t.ben(o[0]) + t.moveTo(n)).toUpperCase()
	},
	F = function(r, n) {
		var n = t.ben(n),
		o = r.substring(n.substring(0, n.length - 2).length, r.length);
		return r = t.dde16(o)
	},
	f = function(r, n, o) {
		if ( - 1 != t.inArray(n, l)) {
			for (var e = r.split("≡"), i = F(e[0], o).split(","), g = 0, a = p(n), g = 0; g < a.length; g++) e[a[g] + 1] = i[g];
			r = "";
			for (g = 1; g < e.length; g++) r = r + e[g] + "≡";
			r = r.substring(0, r.length - 1)
		} else {
			e = r.split("≡");
			r = "";
			for (g = 1; g < e.length; g++) r = r + e[g] + "≡";
			r = r.substring(0, r.length - 1)
		}
		return r
	},
	c = function(t, r) {
		var n = t.split("≡");
		t = "";
		for (var o = 1; o < n.length; o++) t = t + n[o] + "≡";
		return t = t.substring(0, t.length - 1)
	},
	v = function(r, n, o) {
		var e = t.ctr(t.ben(o + n));
		return r = r.substring(e.length, r.length),
		r = t.dde16(r)
	},
	h = function(t) {
		return t.toFixed(2)
	};
	t.extend({
		endetail: function(t, r, n) {
			var o = n.split("≡");
			n = "";
			var e = parseFloat("0"),
			i = parseFloat("0"),
			g = parseFloat("0");
			"01" == t && (e = parseFloat(o[10]), i = parseFloat(o[11]), g = parseFloat(o[12]), e > 10100 && e < 11100 && (o[1] = (parseInt(o[1]) + 1e4).toString(), o[10] = h(e - 100).toString(), o[11] = h(i - 10).toString(), o[12] = h(g - 110).toString()), e > 990 && e < 1090 && (o[10] = h(e + 10).toString(), o[11] = h(i + 10).toString(), o[12] = h(g + 20).toString()), e > 110 && e < 120 && (o[10] = h(e - 10).toString(), o[11] = h(i - 10).toString(), o[12] = h(g - 20).toString())),
			"02" == t && (e = parseFloat(o[10]), i = parseFloat(o[14]), g = parseFloat(o[16]), e > 11110 && e < 12110 && (o[10] = h(e - 110).toString(), o[14] = h(i - 10).toString(), o[16] = h(g - 120).toString()), e > 1090 && e < 1190 && (o[1] = parseInt(o[1]) - 1e4, o[10] = h(e + 10).toString(), o[14] = h(i + 10).toString(), o[16] = h(g + 20).toString()), e > 110 && e < 120 && (o[10] = h(e - 10).toString(), o[14] = h(i - 10).toString(), o[16] = h(g - 20).toString())),
			"03" == t && (e = parseFloat(o[10]), i = parseFloat(o[22]), g = parseFloat(o[24]), e > 201e3 && e < 211e3 && (o[10] = h(e - 1e3).toString(), o[22] = h(i - 100).toString(), o[24] = h(g - 1100).toString()), e > 99900 && e < 109900 && (o[10] = h(e + 100).toString(), o[22] = h(i + 10).toString(), o[24] = h(g + 110).toString()), e > 30010 && e < 40010 && (o[10] = h(e - 10).toString(), o[22] = h(i - 10).toString(), o[24] = h(g - 20).toString())),
			"04" == t && (e = parseFloat(o[16]), i = parseFloat(o[11]), g = parseFloat(o[12]), e > 11e3 && e < 13e3 && (o[16] = h(e - 1e3).toString(), o[11] = h(i - 100).toString(), o[12] = h(g - 1100).toString()), e > 1100 && e < 1300 && (o[16] = h(e - 100).toString(), o[11] = h(i - 10).toString(), o[12] = h(g - 110).toString())),
			"10" == t && (e = parseFloat(o[15]), i = parseFloat(o[11]), g = parseFloat(o[12]), e > 2100 && e < 2200 && (o[15] = h(e - 100).toString(), o[11] = h(i - 10).toString(), o[12] = h(g - 110).toString()), e > 2900 && e < 3e3 && (o[15] = h(e + 100).toString(), o[11] = h(i + 10).toString(), o[12] = h(g + 110).toString()), e > 9890 && e < 10990 && (o[15] = h(e + 110).toString(), o[11] = h(i + 10).toString(), o[12] = h(g + 120).toString())),
			"11" == t && (e = parseFloat(o[11]), i = parseFloat(o[7]), g = parseFloat(o[8]), e > 1110 && e < 1300 && (o[11] = h(e - 100).toString(), o[7] = h(i - 10).toString(), o[8] = h(g - 110).toString()), e > 2910 && e < 3100 && (o[11] = h(e + 100).toString(), o[7] = h(i + 10).toString(), o[8] = h(g + 110).toString())),
			"14" == t && (e = parseFloat(o[15]), i = parseFloat(o[11]), g = parseFloat(o[12]), e > 2100 && e < 3100 && (o[15] = h(e - 100).toString(), o[11] = h(i - 10).toString(), o[12] = h(g - 110).toString()), e > 110 && e < 160 && (o[15] = h(e - 10).toString(), o[11] = h(i - 10).toString(), o[12] = h(g - 20).toString())),
			"15" == t && (e = parseFloat(o[10])) > 30100 && e < 32100 && (o[10] = h(e - 100).toString(), "O" == o[28] && (o[28] = "Y"));
			for (var a = 0; a < o.length; a++) n = n + o[a] + "≡";
			return n = n.substring(0, n.length - 1)
		},
		vsign: function(t, r, n, o) {
			return u(n, t) == o
		},
		deinv: function(t, r, n) {
			return f(n, t, r)
		},
		deinvkey: function(t, r, n) {
			return c(n)
		},
		deinvrm: function(t, r, n) {
			return v(n, t, r)
		}
	})
} (jQuery);




//========t.q.z==================
!
function(e) {
	var o = function(e) {
		return 12 == e.length ? dqdm = e.substring(1, 5) : dqdm = e.substring(0, 4),
		"2102" != dqdm && "3302" != dqdm && "3502" != dqdm && "3702" != dqdm && "4403" != dqdm && (dqdm = dqdm.substring(0, 2) + "00"),
		dqdm
	},
	r = function(e) {
		return e.length >= 12 ? e.substring(0, 10) : e.substring(0, 2)
	},
	p = function(e) {
		return e.length + 5 * e.length
	};
	e.extend({
		prijm: function(r, p, a, t, s, c, n) {
			var m = o(r);
			switch (m) {
			case "1100":
				n = e.encrypt(r + e.moveTo(n)).toUpperCase();
				break;
			case "1200":
				n = e.encrypt(r + e.moveTo(n) + p).toUpperCase();
				break;
			case "1300":
				n = e.encrypt(a + e.moveTo(n) + e.moveTo(r)).toUpperCase();
				break;
			case "1400":
				n = e.encrypt(e.moveTo(n) + s).toUpperCase();
				break;
			case "1500":
				n = e.encrypt(e.moveTo(n) + e.moveTo(r) + p).toUpperCase();
				break;
			case "2100":
				n = e.encrypt(r + p + n).toUpperCase();
				break;
			case "2102":
				n = e.encrypt(r + e.moveTo(p) + n).toUpperCase();
				break;
			case "2200":
				n = e.encrypt(r + n + e.moveTo(n)).toUpperCase();
				break;
			case "2300":
				n = e.encrypt(s + n).toUpperCase();
				break;
			case "3100":
				n = e.encrypt(e.moveTo(n)).toUpperCase();
				break;
			case "3200":
				n = e.encrypt(r + n).toUpperCase();
				break;
			case "3300":
				n = e.encrypt(p + n).toUpperCase();
				break;
			case "3302":
				n = e.encrypt(e.moveTo(p) + n).toUpperCase();
				break;
			case "3400":
				n = e.encrypt(r + e.moveTo(a) + n).toUpperCase();
				break;
			case "3500":
				n = e.encrypt(m + e.moveTo(a) + n).toUpperCase();
				break;
			case "3502":
				n = e.encrypt(m + e.moveTo(n) + r).toUpperCase();
				break;
			case "3600":
				n = e.encrypt(e.encrypt(n) + p + a).toUpperCase();
				break;
			case "3700":
				n = e.encrypt(n + e.moveTo(m) + r).toUpperCase();
				break;
			case "3702":
				n = e.encrypt(e.encrypt(p) + e.moveTo(n) + r).toUpperCase();
				break;
			case "4100":
				n = e.encrypt(e.moveTo(n) + e.moveTo(r) + n).toUpperCase();
				break;
			case "4200":
				n = e.encrypt(a + e.moveTo(a) + n).toUpperCase();
				break;
			case "4300":
				n = e.encrypt(e.moveTo(a) + n + p).toUpperCase();
				break;
			case "4400":
				n = e.encrypt(e.moveTo(r) + e.moveTo(s) + n).toUpperCase();
				break;
			case "4403":
				n = e.encrypt(m + e.moveTo(n) + n).toUpperCase();
				break;
			case "4500":
				n = e.encrypt(m + e.moveTo(r) + n + a).toUpperCase();
				break;
			case "4600":
				n = e.encrypt(p + e.moveTo(r) + n + a).toUpperCase();
				break;
			case "5000":
				n = e.encrypt(r + e.moveTo(r) + r + n).toUpperCase();
				break;
			case "5100":
				n = e.encrypt(a + e.moveTo(r) + p + n).toUpperCase();
				break;
			case "5200":
				n = e.encrypt(t + e.moveTo(r) + n).toUpperCase();
				break;
			case "5300":
				n = e.encrypt(a + e.moveTo(r) + n).toUpperCase();
				break;
			case "5400":
				n = e.encrypt(m + e.moveTo(r) + n).toUpperCase();
				break;
			case "6100":
				n = e.encrypt(m + n + e.moveTo(p) + e.moveTo(r)).toUpperCase();
				break;
			case "6200":
				n = e.encrypt(a + e.moveTo(p) + n).toUpperCase();
				break;
			case "6300":
				n = e.encrypt(r + e.moveTo(m) + n).toUpperCase();
				break;
			case "6400":
				n = e.encrypt(p + e.moveTo(s) + n).toUpperCase();
				break;
			case "6500":
				n = e.encrypt(t + e.moveTo(n) + n).toUpperCase()
			}
			return n
		},
		pricd: function(a, t, s) {
			var c = o(a);
			switch (c) {
			case "1100":
				s = e.encrypt(a + e.moveTo(t) + s).toUpperCase();
				break;
			case "1200":
				s = e.encrypt(a + e.moveTo(a + t) + s).toUpperCase();
				break;
			case "1300":
				s = e.encrypt(a + e.moveTo(a.substring(2, 3) + t) + s).toUpperCase();
				break;
			case "1400":
				s = e.encrypt(a + e.moveTo(t) + s).toUpperCase();
				break;
			case "1500":
				s = e.encrypt(t + e.moveTo(t + s) + s.length).toUpperCase();
				break;
			case "2100":
				s = e.encrypt(s + e.moveTo(c) + s.toLowerCase()).toUpperCase();
				break;
			case "2102":
				s = e.encrypt(e.moveTo(a + t) + e.moveTo(a) + s).toUpperCase();
				break;
			case "2200":
				s = e.encrypt(a.length + t.length + e.moveTo(s) + s).toUpperCase();
				break;
			case "2300":
				s = e.encrypt(e.encrypt(a) + e.moveTo(c) + e.moveTo(s.substring(10, 15))).toUpperCase();
				break;
			case "3100":
				s = e.encrypt(t + e.moveTo(a) + s + a).toUpperCase();
				break;
			case "3200":
				s = e.encrypt(e.moveTo(c) + e.moveTo(c) + s).toUpperCase();
				break;
			case "3300":
				s = e.encrypt(r(a) + e.moveTo(c) + s).toUpperCase();
				break;
			case "3302":
				s = e.encrypt(e.moveTo(a) + e.moveTo(r(c)) + s).toUpperCase();
				break;
			case "3400":
				s = e.encrypt(a + r(e.moveTo(c)) + r(s)).toUpperCase();
				break;
			case "3500":
				s = e.encrypt(r(a) + e.moveTo(c) + s).toUpperCase();
				break;
			case "3502":
				s = e.encrypt(r(a + e.moveTo(c)) + e.moveTo(s)).toUpperCase();
				break;
			case "3600":
				s = e.encrypt(p(a) + e.moveTo(s) + p(s)).toUpperCase();
				break;
			case "3700":
				s = e.encrypt(p(a) + e.moveTo(c) + r(s + a)).toUpperCase();
				break;
			case "3702":
				s = e.encrypt(e.moveTo(a + e.moveTo(c)) + s).toUpperCase();
				break;
			case "4100":
				s = e.encrypt(a + e.moveTo(e.moveTo(c) + s) + p(t)).toUpperCase();
				break;
			case "4200":
				s = e.encrypt(t + e.moveTo(e.moveTo(r(s)) + s) + r(t)).toUpperCase();
				break;
			case "4300":
				s = e.encrypt(e.moveTo(a) + e.moveTo(c) + s + p(s)).toUpperCase();
				break;
			case "4400":
				s = e.encrypt(e.encrypt(a + e.moveTo(c)) + e.moveTo(s)).toUpperCase();
				break;
			case "4403":
				s = e.encrypt(e.moveTo(a + e.moveTo(s)) + e.encrypt(s)).toUpperCase();
				break;
			case "4500":
				s = e.encrypt(e.moveTo(e.moveTo(a) + e.moveTo(c) + s)).toUpperCase();
				break;
			case "4600":
				s = e.encrypt(e.moveTo(r(a) + p(t)) + e.moveTo(a) + s).toUpperCase();
				break;
			case "5000":
				s = e.encrypt(e.moveTo(a) + p(a) + e.moveTo(t) + s).toUpperCase();
				break;
			case "5100":
				s = e.encrypt(p(a) + e.moveTo(s + a) + r(s)).toUpperCase();
				break;
			case "5200":
				s = e.encrypt(e.moveTo(s) + e.moveTo(s + t) + s).toUpperCase();
				break;
			case "5300":
				s = e.encrypt(e.moveTo(a + e.moveTo(t)) + s).toUpperCase();
				break;
			case "5400":
				s = e.encrypt(p(e.moveTo(a)) + e.moveTo(c) + s).toUpperCase();
				break;
			case "6100":
				s = e.encrypt(r(a + e.moveTo(c)) + e.moveTo(s) + r(a + t)).toUpperCase();
				break;
			case "6200":
				s = e.encrypt(e.moveTo(a + e.moveTo(a + t + s)) + s).toUpperCase();
				break;
			case "6300":
				s = e.encrypt(e.moveTo(e.moveTo(r(a) + c)) + a + p(a + t)).toUpperCase();
				break;
			case "6400":
				s = e.encrypt(e.moveTo(a) + s + e.moveTo(c + p(a)) + s).toUpperCase();
				break;
			case "6500":
				s = e.encrypt(e.moveTo(t) + e.moveTo(e.moveTo(a + s)) + s).toUpperCase()
			}
			return s
		}
	})
} (jQuery);