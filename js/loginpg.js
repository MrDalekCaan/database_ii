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

function xxx() {
	console.log('a')
}

// $('form button').on("click",function(e){
//     e.preventDefault();
// });
