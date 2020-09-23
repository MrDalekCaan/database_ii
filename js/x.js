var app = new Vue({
	el: '#app',
	data: {
		books: [],
		selected: [0, 0],
		low: "",
		high:"",
		filter: false,
		pageSize: null,
		titles:{},
		lastValue: {
			"low": "",
			"high": ""
		}
	},
	methods: {
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
			var howMuchBookDoYouWant = 9
			obj = e;
			var target = e.target;
			if (target.tagName == 'SPAN') {
				target = target.parentNode
				// console.log("id: " + target.id)
			}
			var tempsplit = target.id.split('-')

			if (this.selected[0] == tempsplit[1] && this.selected[1] == tempsplit[2])
				return 					// no need to change anything

			if (tempsplit.length == 3) {
				this.$set(this.selected, 0, tempsplit[1])
				this.$set(this.selected, 1, tempsplit[2])
			}

			var cat = this.curTitle()
			var newbooks = xmlRequest(cat, 0, howMuchBookDoYouWant)
			this.books = newbooks
		},
		scroll: function (e) {

			ele = e.target
			var maxScrolltop = ele.scrollHeight - ele.clientHeight
			if (maxScrolltop - ele.scrollTop >= 10)
				return

			// reach the end
			// other_books = xmlRequest('xxx', 0, 9)
			let other_books;
			if (!this.filter) {
				other_books = xmlRequest(this.curTitle(), this.books.length, this.pageSize)
			} else {
				other_books = xmlRequest(this.curTitle(), this.books.length, this.pageSize, this.low, this.high)
			}
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
			this.books = xmlRequest(this.curTitle(), 0, this.pageSize, this.low, this.high)
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

function xmlRequest(subcat, from=0, count=30, low='', high='') {
	const xhttp = new XMLHttpRequest();
	xhttp.open("GET", `books?subcat=${subcat}&from=${from}&count=${count}&low=${low}&high=${high}`, false)
	xhttp.send()
	let obj;
	try {
		obj = JSON.parse(xhttp.responseText)
	} catch(e) {
		console.log("xml json parse error")
		return [];
	}

	return obj.content

}

(async function(){
	const ele = document.getElementById('aspace2');
	if (ele == null)
		return;
	let pageSize = 0;
	while (ele.clientHeight == ele.scrollHeight) {
		pageSize += 3
		app.books.push(...xmlRequest(app.curTitle(), app.books.length, 3))
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







