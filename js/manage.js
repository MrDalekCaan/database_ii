var app = new Vue({
	el: '#app',
	data: {
		books: [],
		selected: [0, 0],
		 titles:[],
		 // pagesize: 21,
        pageSize: 2,
		pagecount:1,
		editable_columns: null,
		all_now: false
	},
	methods: {
		change: function(e) {
			var target = e.path[2]
			var index = parseInt(target.rowIndex) - 1
			// var id = target.id;
			var inputs = target.getElementsByTagName("input")
			// var bookname = inputs[1].value
			// var author = inputs[2].value
			// var price = inputs[3].value
			// var imgurl = inputs[4].value
			// build request
			let url = `ISBN=${this.books[index].ISBN}&`
			for (let i = 0; i < inputs.length; i++) {
				url += `&${this.editable_columns[i]}=${inputs[i].value}`	
			}
			// const book = this.books[index]
			const self = this
			// for (let key in book) {
			// 	url += `${key}=${book[key]}&`
			// }
			let xhttp = new XMLHttpRequest()
			xhttp.open("GET", `manage/change?${url}`)
			xhttp.onreadystatechange = () => {
				if (xhttp.readyState == 4 && xhttp.status == 200) {
					let resp = JSON.parse(xhttp.responseText)
					if (resp.state) {
						alert("update success")
						self.updatePage()
					} else {
						alert("update failed")
					}
				}
			}
			xhttp.send()

			//send change request
			// var obj = sendChangeReq(id, bookname, author, price, imgurl)
			// var newbook = {
			// 	"id": obj.id,
			// 	"bookname": obj.bookname,
			// 	"author": obj.author,
			// 	"imgurl": obj.imgurl,
			// 	"price": obj.price
			// }
			// this.$set(this.books, index, newbook)
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
		all: function() {
			this.all_now = true
			this.$set(this.selected, 0, -1)
			this.$set(this.selected, 1, -1)
			this.updatePage()
		},
		chosecat: function(e) {
			this.all_now = false
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
			this.pagecount = 1
			this.updatePage()
			// var cat = this.titles[tempsplit[1]].titles[tempsplit[2]]
			// console.log("selected cat is " + cat)
		},
		lastpage: function(e) {
			if (this.pagecount == 1) {
				return
			}
			this.pagecount = this.pagecount - 1
			this.updatePage(()=>{}, ()=>{
				this.pagecount = this.pagecount - 1
			})

		},
		nextpage: function (e) {
			this.pagecount = this.pagecount + 1

			this.updatePage(()=>{}, ()=>{
				this.pagecount = this.pagecount - 1
			})
		},
		curTitle: function() {
			if (this.all_now) {
				return ''
			}
			return this.titles[this.selected[0]].subcat[this.selected[1]];
		},
		updatePage: function(success=()=>{}, fail=()=>{}) {
			this.get_books_by(books => {
				if (books.length > 0){
					this.books = books
					success()
				}
				else {
					fail()
				}
			}, fail)
		},
		get_books_by: function(success=()=>{}, fail=()=>{}) {
			const xhttp = new XMLHttpRequest()
			const subcat = this.curTitle()
			xhttp.open("GET", `books?subcat=${subcat}&from=${(this.pagecount - 1) * this.pageSize}&count=${this.pageSize}`)
            xhttp.onreadystatechange = () => {
				if (xhttp.readyState === 4 && xhttp.status === 200) {
					try{
						let books = JSON.parse(xhttp.responseText).content
						success(books)
					}
					catch (e){
						fail()
					}
				}
				else if (xhttp.status >= 400){
					fail()
				}
			}
			xhttp.send()
			// var obj;
			// try {
			// 	obj = JSON.parse(xhttp.responseText)
			// } catch(e) {
			// 	console.log("xml json parse error")
			// 	return [];
			// }
			// return obj.content
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
					let xmlReadColumns = new  XMLHttpRequest()
					xmlReadColumns.open("GET", "read_columns")
					xmlReadColumns.onreadystatechange = () => {
						if (xmlReadColumns.readyState == 4 && xmlReadColumns.status == 200) {
							let editable_columns = JSON.parse(xmlReadColumns.responseText).content
							for (let i = editable_columns.length - 1; i >= 0; i--) {
								if (editable_columns[i] == "ISBN") {
									editable_columns.splice(i, 1)
								}
								if (editable_columns[i] == "sold_count") {
									editable_columns.splice(i, 1)
								}
								if (editable_columns[i] == "img_url") {
									editable_columns.splice(i, 1)
								}
							}	
							self.editable_columns = editable_columns
							self.updatePage()
						}
					}
					xmlReadColumns.send()
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

function quit() {
	const user_id = getCookie('user_id');
	if (user_id) {
		setCookie("user_id", user_id, 0)
		window.location.reload()
	}
}










