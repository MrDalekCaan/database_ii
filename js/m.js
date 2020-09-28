var isSubmitting = false
const app = new Vue({
    el: '#root',
    data: {
        user_id: '',
        passwd:''
    },
    methods: {
        submit() {
            if (isSubmitting) {
                return
            } else {
                isSubmitting = true
            }
            const xhttp = new XMLHttpRequest()
            xhttp.open("POST", 'mobile_login')
            xhttp.onreadystatechange = () => {
                if (xhttp.readyState === 4 && xhttp.status === 200) {
                    if (JSON.parse(xhttp.responseText).state) {
                        alert("login success")
                    } else if (!JSON.parse(xhttp.responseText).state) {
                        alert("login failed")
                    }
                    submitting = false
                }
            }
            xhttp.send( `user_id=${this.user_id}&password=${this.passwd}`)
        }
    }
})


