var app = new Vue({
	el: '#aspace2',
	data: {
		books: [
					{bookname: "nnnnnn",
					count: "222",
					id: "ppppp", price: 100,
					imgurl: "http://img3m3.ddimg.cn/51/25/23977653-1_b_12.jpg"},
					{bookname: "nnnnnn",
					count: "222",
					id: "dd", price: 100,
					imgurl: "http://img3m3.ddimg.cn/51/25/23977653-1_b_12.jpg"},
					{bookname: "nnnnnn",
					count: "222",
					id: "ww", price: 100,
					imgurl: "http://img3m3.ddimg.cn/51/25/23977653-1_b_12.jpg"},
					{bookname: "nnnnnn",
					count: "222",
					id: " fd", price: 100,
					imgurl: "http://img3m3.ddimg.cn/51/25/23977653-1_b_12.jpg"},

					{bookname: "nnnnnn",
					count: "222",
					id: "gdh", price: 100,
					imgurl: "http://img3m3.ddimg.cn/51/25/23977653-1_b_12.jpg"},
					],
		pageName: "cart"
	},
	computed:{
		totalPrice: function () {
			var total = 0;
			for (var i = 0; i < this.books.length; i++) {
				total += parseFloat(this.books[i].price) * parseFloat(this.books[i].count);
			}
			return total;
		}		
	},
	methods: {
		curTitle: function() {
			return this.titles[this.selected[0]].titles[this.selected[1]];
		},
		addone: function (index) {
			var id = this.books[index].id
			var obj = this.books[index]
			obj.count = parseInt(obj.count) + 1
			changeCartContent(id, obj.count)
			this.update(index)
		},
		subone:function (index) {
			var id = this.books[index].id
			var obj = this.books[index]
			obj.count = obj.count - 1
			if (obj.count <= 0) { return }
			changeCartContent(id, obj.count)
			this.update(index)
		},
		update: function(index) {
			var cart = xmlRequest()
			if (cart.length > index) {
				this.$set(this.books, index, cart[index])
			}
		},
		updateAll: function() {
			var cart = xmlRequest()
			this.books = cart
		},
		del: function (index) {
			var id = this.books[index].id
			 changeCartContent(id, 0)
			 this.updateAll()
		}
	},
	created() {
		this.updateAll()
	},
		
});

function changeCartContent(id, num) {
	var xhttp = new XMLHttpRequest()
	xhttp.open('GET', `shoppingcartChange?id=${id}&num=${num}`, false)
	xhttp.send()
}

// change if there is a book
//create new book if there is  no book
function sendChangeReq(oldid, newid, bookname, author, price, imgurl) {
	var xhttp = new XMLHttpRequest()
	xhttp.open("POST", 'manage/change', false)
	xhttp.send(`oldid=${oldid}&newid=${newid}&bookname=${bookname}&author=${author}&price=${price}&imgurl=${imgurl}`)
	var obj = JSON.parse(xhttp.responseText)
	return obj.content
}

function xmlRequest() {
	var xhttp = new XMLHttpRequest()
	xhttp.open("GET", "shoppingcart", false)
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



