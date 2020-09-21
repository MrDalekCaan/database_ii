var app = new Vue({
	el: '#app',
	data: {
		books: [],
		selected: [0, 0],
		 titles:[
		 	{
		 		cat:'摄影服务',
		 		titles:['人像写真', '静物拍摄', '产品摄影', '创意婚纱照', '儿童成长记录']
		 	},
		 	{
		 		cat: '创意摄影',
		 		titles: ['水下拍摄', '高空航拍', '旅途跟拍', '星空摄影', '可爱宝宝']
		 	},
		 	{
		 		cat: '记录时光',
		 		titles:['儿童成长记录', '定格婚礼瞬间', '仪式全纪实', '老年结婚照']
		 	}
		 ],
		 pagesize: 21,
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
			var cat = this.curTitle()
			var newbooks = xmlRequest(cat, (this.pagecount - 1) * this.pagesize, this.pagesize)
			if (newbooks.length == 0) {
				return false;
			}
			this.books = newbooks
			return true;
		},
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

function xmlRequest(cat=null, from=0, count=30, code=null) {
	var xhttp = new XMLHttpRequest()
	if (cat != null){
		xhttp.open("GET", `books?cat=${cat}&from=${from}&count=${count}`, false)
	}
	else if (code != null) {
		xhttp.open("GET", `book?code=${code}`, false)
	}
	else return [];
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

(async function(){
	var ele = document.getElementById('aspace2')
	if (ele == null)
		return;

	var count = 0;

	while (ele.clientHeight == ele.scrollHeight) {
		count++;
		// app.books.push(...xmlRequest('xxx', 0, 3))
		app.books.push(...xmlRequest(app.curTitle(), app.books.length, 1))
		await new Promise(r => setTimeout(r, 80));
	}
	app.pagesize = count;
})();











