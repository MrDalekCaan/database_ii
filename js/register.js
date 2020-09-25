var submitting = false
const app = new Vue({
	el: "#root",
	data: {
		username: "",
		password: "",
		password_again: "",
		showError: false,
		errorMsg: ""
	},
	methods: {
		submit: function (e) {
		    if (submitting) {
		    	this.logError("too quick, wait please")
				return
			}
		    else {
		    	submitting = false
			}
			if (this.password != this.password_again) {
				this.logError("两次密码不相同")
				this.password = ""
				this.password_again = ""
				return
			}
			const xhttp = new XMLHttpRequest();
			xhttp.open("POST", "register")
			xhttp.onreadystatechange = () => {
				if (xhttp.readyState == 4 && xhttp.status == 200) {
					submitting = false
					try {
						let obj = JSON.parse(xhttp.responseText)
						let user_id = obj.user_id
						alert(`Your user id is ${user_id}`)
                        // TODO: redirect to a page that show infomation about new account
					}
					catch {
						alert("Unknown error")
					}
				}
			}
			xhttp.send(`username=${this.username}&password=${this.password}`)
			console.log(`username: ${this.username}, password: ${this.password}, password_again: ${this.password_again}`)
			console.log(xhttp.responseText)
		},
		closePanel: function () {
			this.showError = false
		},
		logError: function (msg) {
			this.showError = true
			this.errorMsg = msg
		}
	},
});