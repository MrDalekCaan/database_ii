var app  =new Vue({
	el: "#root",
	data: {
		username:"",
		password: "",
		password_again:"",
		showError: false,
		errorMsg: ""
	},
	methods: {
		submit: function (e) {
			if (this.password != this.password_again) {
				this.logError("两次密码不相同")
				this.password = ""
				this.password_again = ""
				return
			}
			var xhttp = new XMLHttpRequest()
			xhttp.open("POST", "register", false)
			xhttp.send(`username=${this.username}&password=${this.password}`)
			console.log(`username: ${this.username}, password: ${this.password}, password_again: ${this.password_again}`)
			console.log(xhttp.responseText)
		},
		closePanel: function() {
			this.showError = false
		},
		logError: function(msg) {
			this.showError = true
			this.errorMsg = msg
		}
	},
})