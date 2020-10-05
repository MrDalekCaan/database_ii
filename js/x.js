var gettingBooks = false
var app = new Vue({
	el: '#app',
	data: {
		books: [],
		selected: [0, 0],
		low: "",
		high:"",
		key_word:'',
		filter: false,
		fuzzy_mode: false,
		pageSize: 6,
		titles:{},
		order:'time_desc',
		all_now: false,
		lastValue: {
			"low": "",
			"high": ""
		}
	},
	methods: {
		fuzzy_search_on: function() {
			this.fuzzy_mode = true
            // this.books = this.get_books_by(0, this.pageSize)
            this.update()
		},
		fuzzy_search_off: function (){
			this.fuzzy_mode = false
			// this.books = this.get_books_by(0, this.pageSize)
            this.update()
		},
		boundChange: function(e){
			// this.lastValue.low = this.low
			// this.lastValue.high = this.high
			// const id = e.target.id;
			if (this.high < 0)
				this.high = ""
			if (this.low < 0)
				this.low = ""
			if (this.high == "" || this.low == "")
				return
			if (this.low > this.high) {
				let temp = this.low
				this.low = this.high
				this.high = temp
			}
			// if (this.high == null || this.high == "")
		 	// 	this.high = 0
		 	// if (this.low == null || this.low == "")
		 	// 	this.low = 0

		 	// var high = parseFloat(this.high)
		 	// var low = parseFloat(this.low)
			//
		 	// high = high < 0 ? 0 : high
		 	// low = low < 0 ? 0 : low
			//
		 	// this.high = high
		 	// this.low = low

		 	// if (id == 'low' && low > high) {
		 	// 	this.high = this.low
		 	// } else if (id == 'high' && high < low) {
		 	// 	this.low = this.high
		 	// }

		},
		all: function() {
			this.all_now = true
			this.$set(this.selected, 0, -1)
			this.$set(this.selected, 1, -1)
			this.updatePage()
		},
		chosecat: function(e) {
		    // set current subcat
			this.all_now = false
			let target = e.target;
			if (target.tagName == 'SPAN') {
				target = target.parentNode
			}
			const tempsplit = target.id.split('-');

			if (this.selected[0] == tempsplit[1] && this.selected[1] == tempsplit[2])
				return 					// no need to change anything

			if (tempsplit.length == 3) {
				this.$set(this.selected, 0, tempsplit[1])
				this.$set(this.selected, 1, tempsplit[2])
			}
			const self = this
			this.get_books_by(0, this.pageSize, books => {
				self.books = books
			});
			// this.books = newbooks
		},
		scroll: function (e) {
			let ele = e.target
			const maxScrolltop = ele.scrollHeight - ele.clientHeight;
			if (maxScrolltop - ele.scrollTop >= 10)
				return

			const self = this
            this.get_books_by(this.books.length, this.pageSize, books => {
            	self.books.push(...books)
			})
		},
		curTitle: function() {
			if (this.all_now) {
				return ''
			}
			return this.titles[this.selected[0]].subcat[this.selected[1]];
		},
		startFilter: function (){
			this.filter = true
			this.updatePage()
		},
		cancleFilter: function() {
			if (!this.filter)
				return
			this.filter = false
			this.low = "";
			this.high = "";
			this.updatePage()
		},
		updatePage: function () {
			this.get_books_by( 0, this.pageSize, books => {
				this.books = books
			})
		},
		 get_books_by: function(from=0, count=30, callback) {
		 	/*
			callback have parameter of books get from server
		 	*/	
			if (gettingBooks) {
				return
			} else {
				gettingBooks = true
			}
			const xhttp = new XMLHttpRequest();
			let request_parameters = `books?subcat=${this.curTitle()}&from=${from}&count=${count}&orderby=${this.order}`
			 if (this.filter) {
			 	request_parameters += `&low=${this.low}&high=${this.high}`
			 }
			 if (this.fuzzy_mode) {
			 	request_parameters += `&key_word=%${this.key_word}%`
			 }
			xhttp.open("GET", request_parameters)
			xhttp.onreadystatechange = () => {
				if (xhttp.readyState == 4 && xhttp.status == 200) {
					gettingBooks = false	
					let obj
					try {
						obj = JSON.parse(xhttp.responseText)
						callback(obj.content)
					} catch (e) {
						console.error("xml json parse error")	
					}
				}
				else if (xhttp.status >= 400) {
					gettingBooks = false
					console.error("get books failed")
				}
			}
			xhttp.send()
		},
		update: function(){
			// this.books = this.get_books_by(0, this.pageSize)
			const self = this
			self.get_books_by(0, self.pageSize, books => {
				self.books = books
			})
		},
		set_order: function(event) {
			if (this.order != event.target.id) {
				this.order = event.target.id
				this.update()
			}
		}
	},
	created() {
	    // get category
	    let self = this
		let xhttp = new XMLHttpRequest()
		xhttp.open("GET", "cats")
		xhttp.onreadystatechange = () => {
	    	if (xhttp.readyState == 4 && xhttp.status == 200) {
				let resp
				try{
					resp = JSON.parse(xhttp.responseText)
					let result = []
					for (const cat in resp) {
						let obj = {"subcat": resp[cat], "cat": cat}
						result.push(obj)
					}
					self.titles = result
					// books
                   	const ele = document.getElementById('aspace2');
					if (ele == null)
						return;
					self.get_books_by(0, self.pageSize, books => {
						self.books.push(...books)
					})
				} catch (e) {
					console.log("cats json parse error")
				}
			}
			}
		xhttp.send()
	}
});


// (async function(){
// 	const ele = document.getElementById('aspace2');
// 	if (ele == null)
// 		return;
// 	let pageSize = 0;
// 	while (ele.clientHeight == ele.scrollHeight) {
// 		pageSize += 3
// 		app.books.push(...app.get_books_by(app.books.length, 3))
// 		await new Promise(r => setTimeout(r, 100));
// 	}
// 	app.pageSize = pageSize
// })();


function quit() {
	const user_id = getCookie('user_id');
	if (user_id) {
		setCookie("user_id", user_id, 0)
		window.location.reload()
	}
}







