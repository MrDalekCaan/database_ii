var app = new Vue({
	el: "#root",
	data: {
		id: "",
	},
	methods:{
		addToCart: function () {
			if (hasUser()) {
				var xhttp = new XMLHttpRequest()
				xhttp.open("GET", `/addToCart?id=${this.id}`)
				xhttp.send()
			} else {
				window.location.href = "/loginpg"
			}
		}
	},
	created() {
		this.id = getId()
	}
})


function getId() {
	const urlParams = new URLSearchParams(window.location.search)
	return urlParams.get("id")
}

function hasUser() {
	return getCookie("username") != null;
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