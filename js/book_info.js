var addingToCart = false
var app = new Vue({
	el: "#root",
	data: {
		isbn: "",
	},
	methods:{
		addToCart: function () {
			if (addingToCart) return
			else {
				alert("too quick, please wait")
				addingToCart = true
			}
			if (hasUser()) {
				const xhttp = new XMLHttpRequest();
				xhttp.open("GET", `/addToCart?isbn=${this.isbn}`)
				xhttp.onreadystatechange = () => {
					addingToCart = false	
					alert("add to cart successfully")
				}
				xhttp.send()
			} else {
				window.location.href = "/loginpg"
			}
		}
	},
	created() {
		this.isbn = getId()
	}
})


function getId() {
	const urlParams = new URLSearchParams(window.location.search)
	return urlParams.get("isbn")
}

function hasUser() {
	return getCookie("user_id") != null;
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function setCookie(cname, cvalue, second) {
  var d = new Date();
  d.setTime(d.getTime() + (second * 1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}