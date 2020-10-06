var is_getting_books = false
const app = new Vue({
	el: "#root",
	data: {
		books: [],
		pageSize: 4,
		pageCount: 1,
	},
	methods: {
		onSubmit: function(e) {
			window.location.href = `/sold_history?pageCount=${this.pageCount}`
		},
		nextPage: function(e) {
			this.pageCount = parseInt(this.pageCount) + 1
		},
		previousPage: function(e) {
			if (this.pageCount == 1) {
				e.defaultPrevented = true
				return
			}
			this.pageCount -= 1
		},
		get_books: function(from, count, callback=()=>{}) {
			if (is_getting_books) {
				return 
			}
			else {
				is_getting_books = true;
			}
			let xhttp = new XMLHttpRequest()
			xhttp.open("GET", this.get())
			xhttp.onreadystatechange = () => {
				if (xhttp.readyState == 4 && xhttp.status == 200) {
					is_getting_books = false
					try{
						let books = JSON.parse(xhttp.responseText)
						books = books["content"]
						callback(books)
					} catch(e) {
						console.error(e)						
					}
				} else if (xhttp.status >= 400){
					is_getting_books = false
				}
			}
			xhttp.send()
		},
		get: function() {
			let order
			return `/get_history?from=${this.pageSize * (this.pageCount - 1)}&count=${this.pageSize}`
		},
	},
	created: function() {
		const urlParams = new URLSearchParams(window.location.search)
		this.pageCount = urlParams.get("pageCount")
		if (this.pageCount == null) {
			this.pageCount = 1
		}
		this.get_books(this.pageSize * (this.pageCount - 1), this.pageSize, (books) => {
			this.books = books
		})
	}
})
