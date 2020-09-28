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

function get_single_book(isbn, sync=false, success= ()=>{}, failed=()=>{}) {
	let xhttp = new XMLHttpRequest()
	xhttp.open("GET", `get_single_book?isbn=${isbn}`, sync)
	if (sync) {
		xhttp.onreadystatechange = () => {
			if (xhttp.readyState === 4 && xhttp.status === 200) {
				try {
					let obj = JSON.parse(xhttp.responseText)
					success(obj)
				} catch (e) {
					failed()
				}
			} else if (xhttp.status >= 400) {
				failed()
			}
		}
	}
	xhttp.send()
	return JSON.parse(xhttp.responseText)
}



// module.exports = {
// 	formatPrice,
// 	setCookie}