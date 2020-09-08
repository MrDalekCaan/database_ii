username = document.getElementById("username")
password = document.getElementById("password")


function submit() {

	var xhttp = new XMLHttpRequest()
	xhttp.open('POST', 'login',false)
	xhttp.send(`username=${username.value}&password=${password.value}`)
	if (xhttp.responseText == 0) {
		alert("incorrect username or password")
		username.value = ""
		password.value = ""
	}
	else {
		window.location.href = xhttp.responseText
	}

}

console.log('loginpg.js loaded')
function xxx() {
	console.log('a')
}

// $('form button').on("click",function(e){
//     e.preventDefault();
// });
