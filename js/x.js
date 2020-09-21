var app = new Vue({
	el: '#app',
	data: {
		books: [],
		selected: [0, 0],
		low: null,
		high:null,
		filter: false,
		pageSize: null,
		titles:[
		 	{
		 		cat:'摄影服务',
		 		titles:['林业', '人工智能', '音乐', '摄影', '变态心理学']
		 	},
		 	{
		 		cat: '创意摄影',
		 		titles: ['早教-亲子互动', '旅游随笔', '旅途跟拍', '星空摄影', '可爱宝宝']
		 	},
		 	{
		 		cat: '记录时光',
		 		titles:['儿童成长记录', '定格婚礼瞬间', '仪式全纪实', '老年结婚照']
		 	}
		],
		lastValue: {
			"low": null,
			"high": null
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

		 	high = high < 0 ? 0 : highl
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
			if (!this.filter) {
				other_books = xmlRequest(this.curTitle(), this.books.length, this.pageSize, null, null)
			} else {
				other_books = xmlRequest(this.curTitle(), this.books.length, this.pageSize, this.low, this.high)
			}
			this.books.push(...other_books)
		},
		curTitle: function() {
			return this.titles[this.selected[0]].titles[this.selected[1]];
		},
		startFilter: function (){
			if (this.filter)
				return
			this.filter = true
			this.updatePage()
		},
		cancleFilter: function() {
			if (!this.filter)
				return
			this.filter = false
			this.low = null;
			this.high = null;
			this.updatePage()
		},
		updatePage: function () {
			this.books = xmlRequest(this.curTitle(), 0, this.pageSize, this.low, this.high)
		}
	},	
	created() {
		let xhttp = new XMLHttpRequest()
		xhttp.open("GET", "cats", false)
		xhttp.send()
		let resp
		try{
			resp = JSON.parse(xhttp.responseText)
            this.titles = resp
		} catch (e) {
			console.log("cats json parse error")
		}
	}
});

function xmlRequest(cat, from=0, count=30, low=null, high=null) {
	var xhttp = new XMLHttpRequest()
	// if (cat != null){
	xhttp.open("GET", `books?cat=${cat}&from=${from}&count=${count}&low=${low}&high=${high}`, false)
	// }
	// else if (code != null) {
	// 	xhttp.open("GET", `book?code=${code}`, false)
	// }
	// else return [];
	xhttp.send()
	var obj;
	try {
		obj = JSON.parse(xhttp.responseText)
	} catch(e) {
		console.log("xml json parse error")
		return [];
	}

	return obj.content

}

// (async function(){
// 	var ele = document.getElementById('aspace2')
// 	if (ele == null)
// 		return;

// 	var pageSize = 0

// 	while (ele.clientHeight == ele.scrollHeight) {
// 		pageSize += 3
// 		// app.books.push(...xmlRequest('xxx', 0, 3))
// 		app.books.push(...xmlRequest(app.curTitle(), app.books.length, 3))
// 		await new Promise(r => setTimeout(r, 100));
// 	}
// 	app.pageSize = pageSize
// })();

var obj;

function quit() {
	var username = getCookie('username')
	if (username) {
		setCookie("username", username, 0)
		window.location.reload()
	}
}







