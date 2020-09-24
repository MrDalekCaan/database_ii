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
		pageSize: null,
		titles:{},
		order:'time_desc',
		lastValue: {
			"low": "",
			"high": ""
		}
	},
	methods: {
		fuzzy_search_on: function() {
			this.fuzzy_mode = true
            this.books = this.get_books_by(0, this.pageSize)
		},
		fuzzy_search_off: function (){
			this.fuzzy_mode = false
			this.books = this.get_books_by(0, this.pageSize)
		},
		boundChange: function(e){
			console.log('changed')
			this.lastValue.low = this.low
			this.lastValue.high = this.high
			var id = e.target.id
		 	if (this.high == null || this.high == "")
		 		this.high = 0
		 	if (this.low == null || this.low == "")
		 		this.low = 0

		 	var high = parseFloat(this.high)
		 	var low = parseFloat(this.low)

		 	high = high < 0 ? 0 : high
		 	low = low < 0 ? 0 : low

		 	this.high = high
		 	this.low = low

		 	if (id == 'low' && low > high) {
		 		this.high = this.low
		 	} else if (id == 'high' && high < low) {
		 		this.low = this.high
		 	}

		},
		chosecat: function(e) {
		    // set current subcat
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

			const newbooks = this.get_books_by(0, this.pageSize);
			this.books = newbooks
		},
		scroll: function (e) {
			let ele = e.target
			const maxScrolltop = ele.scrollHeight - ele.clientHeight;
			if (maxScrolltop - ele.scrollTop >= 10)
				return

			let other_books;
			// if (!this.filter) {
				other_books = this.get_books_by(this.books.length, this.pageSize)
			// } else {
				other_books = this.get_books_by(this.books.length, this.pageSize)
			// }
			this.books.push(...other_books)
		},
		curTitle: function() {
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
			this.books = this.get_books_by( 0, this.pageSize)
		},
		 get_books_by: function(from=0, count=30) {
			const xhttp = new XMLHttpRequest();
			let request_parameters = `books?subcat=${this.curTitle()}&from=${from}&count=${count}&orderby=${this.order}`
			 if (this.filter) {
			 	request_parameters += `&low=${this.low}&high=${this.high}`
			 }
			 if (this.fuzzy_mode) {
			 	request_parameters += `&key_word=%${this.key_word}%`
			 }
			xhttp.open("GET", request_parameters, false)
			xhttp.send()
			let obj;
			try {
				obj = JSON.parse(xhttp.responseText)
			} catch(e) {
				console.log("xml json parse error")
				return [];
			}
			return obj.content
		},
		update: function(){
			this.books = this.get_books_by(0, this.pageSize)
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
		let xhttp = new XMLHttpRequest()
		xhttp.open("GET", "cats", false)
		xhttp.send()
		let resp
		try{
			resp = JSON.parse(xhttp.responseText)
			let result = []
			for (const cat in resp) {
				let obj = {"subcat": resp[cat], "cat": cat}
				result.push(obj)
			}
            this.titles = result
		} catch (e) {
			console.log("cats json parse error")
		}
	}
});


(async function(){
	const ele = document.getElementById('aspace2');
	if (ele == null)
		return;
	let pageSize = 0;
	while (ele.clientHeight == ele.scrollHeight) {
		pageSize += 3
		app.books.push(...app.get_books_by(app.books.length, 3))
		await new Promise(r => setTimeout(r, 100));
	}
	app.pageSize = pageSize
})();


function quit() {
	const user_id = getCookie('user_id');
	if (user_id) {
		setCookie("user_id", user_id, 0)
		window.location.reload()
	}
}







