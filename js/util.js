function formatPrice(price) {
	const res = price.split("¥");
	return res.length == 2? res[1]: null
}

function setCookie(cname, cvalue, second) {
	const d = new Date();
	d.setTime(d.getTime() + (second * 1000));
	const expires = "expires=" + d.toUTCString();
	document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(name) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(';').shift();
}



// module.exports = {
// 	formatPrice,
// 	setCookie}