user_id = document.getElementById("user_id")
password = document.getElementById("password")


function submit() {
	const xhttp = new XMLHttpRequest()
	xhttp.open('POST', 'login',false)
	xhttp.send(`user_id=${user_id.value}&password=${password.value}`)
    let resp = JSON.parse(xhttp.responseText)
	if (resp.state) {
		window.location.href = "/"
	} else {
		alert("wrong password or user_id")
	}
}


(function check_login_state () {
	const xhttp = new XMLHttpRequest()
	xhttp.open('GET', "login_state")
	xhttp.onreadystatechange = async () => {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			const obj = JSON.parse(xhttp.responseText)
			if (obj.error == 1) {
				alert("token expired")
			}else if (obj.login_state) {
				setCookie("user_id", obj.user_info.user_id, 60 * 60)
				setCookie("user_name", obj.user_info.user_name, 60 * 60)
				setCookie("user_type", obj.user_info.user_type, 60 * 60)
				window.location.href = "/"
			} else if (!obj.login_state) {
				await new Promise(r => setTimeout(r, 2000))
				check_login_state()
			}
		}
	}
	xhttp.send()
})()

// $('form button').on("click",function(e){
//     e.preventDefault();
// });
