var is_getting_books = false
const app = new Vue({
	el: "#root",
	data: {
		key_word: "",
		books: [],
		pageSize: 2,
		pageCount: 1,
		order: 0
	},
	methods: {
		onSubmit: function(e) {
			window.location.href = `/search_result?pageCount=${this.pageCount}&key_word=${this.key_word}`
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
		set_order: function(e) {
			this.order = e.target.getAttribute("index")
			window.location.href = this.url()
		},
		url: function() {
			return `/search_result?pageCount=${this.pageCount}&key_word=${this.key_word}&order=${this.order}`
		},
		get: function() {
			let order
			switch(this.order) {
				case "0":
					 order = "time_asc";
					break;
				case "1": 
					order = "time_desc";
					break;
				case "2":
					order = "sold_asc"
					break;
				case "3":
					order = "sold_desc"
					break;
				default:
					order = "time_asc"
					break;
			}
			return `/books?from=${this.pageSize * (this.pageCount - 1)}&count=${this.pageSize}&key_word=${this.key_word}&orderby=${order}`
		}
	},
	created: function() {
		const urlParams = new URLSearchParams(window.location.search)
		this.key_word = urlParams.get("key_word")
		this.pageCount = urlParams.get("pageCount")
		this.order = urlParams.get("order")
		if (this.order == null) {
			this.order = 0
		}
		if (this.pageCount == null) {
			this.pageCount = 1
		}
		this.get_books(this.pageSize * (this.pageCount - 1), this.pageSize, (books) => {
			this.books = books
		})
	}
})

// ░