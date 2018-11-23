var yzmWait = 2;
var retrycount = 0;
function yzmTime(o) {
	if (yzmWait == 0) {
		$('#yzm_unuse_img').hide();
		$('#yzm_img').show();
		yzmWait = 60
	} else {
		if (yzmWait == 2) {
			$('#yzm_unuse_img').show();
			$('#yzm_img').hide()
		}
		yzmWait--;
		setTimeout(function() {
			yzmTime(o)
		},
		1000)
	}
}
function getYzmXx() {
	show_yzm = "1";
	var fpdm = $("#fpdm").val().trim();
	var swjginfo = getSwjg(fpdm, 0);
	var url = swjginfo[1] + "/yzmQuery";
	var nowtime = showTime().toString();
	var fpdmyzm = $("#fpdm").val().trim();
	var kjje = $("#kjje").val().trim();
	var rad = Math.random();
	var area = swjginfo[2];
	var param = {
		'fpdm': fpdmyzm,
		'r': rad,
		'v': VVV,
		'nowtime': nowtime,
		'area': area,
		'publickey': $.ckcode(fpdmyzm, nowtime)
	};
	$.ajaxSetup({
		cache: false
	});
	yzmFlag = 1;
	$.ajax({
		type: "post",
		url: url,
		data: param,
		dataType: "jsonp",
		jsonp: "callback",
		success: function(jsonData) {
			delayFlag = "1";
			var key1 = jsonData.key1;
			var key2 = jsonData.key2;
			var key3 = jsonData.key3;
			var key4 = jsonData.key4;
			var key5 = jsonData.key5;
			if (typeof key5 === "undefined") {
				oldweb = 1
			} else {
				oldweb = 0
			}
			if (key1 == "003") {
				jAlert("验证码请求次数过于频繁，请1分钟后再试！", "警告");
				$('#yzm_img').hide()
			} else if (key1 == "005") {
				jAlert("非法请求!", "警告")
			} else if (key1 == "010") {
				jAlert("网络超时，请重试！(01)", "警告")
			} else if (key1 == "fpdmerr") {
				jAlert("请输入合法发票代码!", "警告")
			} else if (key1 == "024") {
				jAlert("24小时内验证码请求太频繁，请稍后再试！", "警告");
				$('#yzm_img').hide()
			} else if (key1 == "016") {
				jAlert("服务器接收的请求太频繁，请稍后再试！", "警告");
				$('#yzm_img').hide()
			} else if (key1 == "020") {
				jAlert("由于查验行为异常，涉嫌违规，当前无法使用查验服务！", "提示")
			} else if (key1 == "errv") {
				jAlert("当前页面版本较低，请按CTRL-F5刷新页面！", "提示")
			} else if (key1 != "") {
				$("#yzm_img").attr("src", "data:image/png;base64," + key1);
				$("#yzm_unuse_img").attr("src", "data:image/png;base64," + key1);
				if (key4 == '00') {
					$("#yzminfo").text("请输入验证码文字")
				} else if (key4 == '01') {
					$("#yzminfo").html("请输入验证码图片中<font color=\"red\" size=\"4\" style=\"background:#C0C0C0\">红色</font>文字")
				} else if (key4 == '02') {
					$("#yzminfo").html("请输入验证码图片中<font color=\"yellow\" size=\"4\" style=\"background:#C0C0C0\">黄色</font>文字")
				} else if (key4 == '03') {
					$("#yzminfo").html("请输入验证码图片中<font color=\"blue\" size=\"4\" style=\"background:#C0C0C0\">蓝色</font>文字")
				}
				yzmSj = key2;
				jmmy = key3
			}
		},
		timeout: 5000,
		error: function(XMLHttpRequest, textStatus, errorThrown) {
			if (retrycount == 9) {} else {
				retrycount = retrycount + 1;
				getYzmXx()
			}
		}
	});
	yzmWait = 2;
	yzmTime($('#yzm_img'))
}
function showTime() {
	var myDate = new Date();
	var time = myDate.getTime();
	return time
}