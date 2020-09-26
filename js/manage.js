var app = new Vue({
	el: '#app',
	data: {
		books: [],
		selected: [0, 0],
		 titles:[],
		 // pagesize: 21,
        pageSize: 15,
		 pagecount:1
	},
	methods: {
		change: function(e) {
			var target = e.path[2]
			var index = e.index
			var id = target.id;
			var inputs = target.getElementsByTagName("input")
			var bookname = inputs[1].value
			var author = inputs[2].value
			var price = inputs[3].value
			var imgurl = inputs[4].value

			//send change request
			var obj = sendChangeReq(id, bookname, author, price, imgurl)
			var newbook = {
				"id": obj.id,
				"bookname": obj.bookname,
				"author": obj.author,
				"imgurl": obj.imgurl,
				"price": obj.price
			}
			this.$set(this.books, index, newbook)
		},
		del: function(e) {
			var target = e.path[2]
			var id = target.id
			var xhttp = new XMLHttpRequest()
			xhttp.open("POST", "manage/delete", false)
			xhttp.send(`id=${id}`)
			console.log(xhttp.responseText)
			if (xhttp.responseText == "0") {
				// failed
				return
			}
			// else 
			this.updatePage()
		},
		chosecat: function(e) {
			var howMuchBookDoYouWant = this.pagesize
			var target = e.target;
			// if (target.tagName == 'LI') {
			// 	console.log("id: " + target.id)
			// } else 
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
			this.updatePage()
			// var cat = this.titles[tempsplit[1]].titles[tempsplit[2]]
			// console.log("selected cat is " + cat)
		},
		lastpage: function(e) {
			if (this.pagecount == 1) {
				return
			}
			this.pagecount = this.pagecount - 1
			if (!this.updatePage()) {
				// update failed
				this.pagecount = this.pagecount + 1
			}
		},
		nextpage: function (e) {
			this.pagecount = this.pagecount + 1
			if (!this.updatePage()) {
				// update failed
				this.pagecount = this.pagecount - 1
			}
		},
		curTitle: function() {
			return this.titles[this.selected[0]].titles[this.selected[1]];
		},
		updatePage: function() {
			const newbooks = self.get_books((this.pagecount - 1) * this.pageSize, this.pageSize);
			if (newbooks.length == 0) {
				return false;
			}
			this.books = newbooks
			return true;
		},
		get_books: function(from=0, count=30, isbn=null, success, fail) {
			const xhttp = new XMLHttpRequest();
			const subcat = this.curTitle()
			if (subcat != null){
				xhttp.open("GET", `books?subcat=${subcat}&from=${from}&count=${count}`)
			}
			else if (isbn != null) {
				xhttp.open("GET", `book?code=${isbn}`)
			}
			else return [];
			xhttp.onreadystatechange = () => {
				if (xhttp.readyState == 4 && xhttp.status == 200) {
					success(JSON.parse(xhttp.responseText).content)
				} else if (xhttp.status >= 400) {
					fail()	
				}
			}
			xhttp.send()
			var obj;
			try {
				obj = JSON.parse(xhttp.responseText)
			} catch(e) {
				console.log("xml json parse error")
				return [];
			}
			return obj.content
		},
	},
	created() {
		let self = this
		let xhttp = new XMLHttpRequest()
		xhttp.open("GET", "cats")
		xhttp.onreadystatechange = () => {
	    	if (xhttp.readyState == 4 && xhttp.status == 200) {
				let resp
				try {
					resp = JSON.parse(xhttp.responseText)
					let result = []
					for (const cat in resp) {
						let obj = {"subcat": resp[cat], "cat": cat}
						result.push(obj)
					}
					self.titles = result
				}catch (e) {
					console.log("cats json parse error")
				}
	    	}
		}
		xhttp.send()
	}
});

// change if there is a book
//create  new book if there is  no book
function sendChangeReq(id, bookname, author, price, imgurl) {
	var xhttp = new XMLHttpRequest()
	xhttp.open("POST", 'manage/change', false)
	xhttp.send(`id=${id}&bookname=${bookname}&author=${author}&price=${price}&imgurl=${imgurl}`)
	var obj = JSON.parse(xhttp.responseText)
	return obj.content
}


// (async function(){
// 	var ele = document.getElementById('aspace2')
// 	if (ele == null)
// 		return;
//
// 	var count = 0;

	// while (ele.clientHeight == ele.scrollHeight) {
	// 	count++;
		// app.books.push(...xmlRequest('xxx', 0, 3))
		// app.books.push(...xmlRequest(app.curTitle(), app.books.length, 1))
		// await new Promise(r => setTimeout(r, 80));
// 	}
// 	app.pagesize = count;
// })();











