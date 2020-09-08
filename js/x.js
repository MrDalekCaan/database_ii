var app = new Vue({
	el: '#app',
	data: {
		books: [],
		selected: [0, 0],
		// threebook:[{name:'幼儿绘本', price:'¥29.70', image:'http://img3m4.ddimg.cn/58/18/1179371614-1_b_14.jpg', author:''},
		//  {name:'全5册早教书籍', price:'¥29.80', image:'http://img3m4.ddimg.cn/37/3/1202388004-1_b_2.jpg', author:''},
		//  {name:'幼儿绘本', price:'¥29.70', image:'http://img3m4.ddimg.cn/58/18/1179371614-1_b_14.jpg', author:''},],
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
		 ]
	},
	methods: {
		chosecat: function(e) {

			var howMuchBookDoYouWant = 9
			obj = e;
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

			// var cat = this.titles[tempsplit[1]].titles[tempsplit[2]]
			var cat = this.curTitle()
			var newbooks = xmlRequest(cat, 0, howMuchBookDoYouWant)
			this.books = newbooks
			// console.log("selected cat is " + cat)


		},
		scroll: function (e) {
			// console.log(e.target)
			// console.log('current array size: ' + this.books.length)

			ele = e.target
			var maxScrolltop = ele.scrollHeight - ele.clientHeight
			if (maxScrolltop - ele.scrollTop >= 10)
				return

			// reach the end
			// other_books = xmlRequest('xxx', 0, 9)
			other_books = xmlRequest(this.curTitle(), 0, 9)
			this.books.push(...other_books)
		},
		curTitle: function() {
			return this.titles[this.selected[0]].titles[this.selected[1]];
		},
	}
		
	// data() {
	// 	return {
	// 		content:'this is vue'
	// 	}
	// }
	
});

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

	while (ele.clientHeight == ele.scrollHeight) {
		// app.books.push(...xmlRequest('xxx', 0, 3))
		app.books.push(...xmlRequest(app.curTitle(), 0, 3))
		await new Promise(r => setTimeout(r, 100));
	}

})();

var obj;










