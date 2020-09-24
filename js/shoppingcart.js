var changingCartContent = false
var app = new Vue({
	el: '#aspace2',
	data: {
		books: [],
		pageName: "cart"
	},
	computed:{
		totalPrice: function () {
			let total = 0;
			for (let i = 0; i < this.books.length; i++) {
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
			const isbn = this.books[index].ISBN;
			const obj = this.books[index];
			obj.count = parseInt(obj.count) + 1
			changeCartContent(isbn, obj.count)
			this.update(index)
		},
		subone:function (index) {
			var isbn = this.books[index].ISBN
			var obj = this.books[index]
			obj.count = obj.count - 1
			if (obj.count <= 0) {
				obj.count = obj.count + 1
				return
			}
			changeCartContent(isbn, obj.count)
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
			var isbn = this.books[index].ISBN
			 changeCartContent(isbn, 0)
			 this.updateAll()
		},
		buyThisOne: function(index) {
			const isbn = this.books[index].ISBN
			const count = this.books[index].count
			let xhttp = new XMLHttpRequest()
			xhttp.open("GET", `purchase?isbn=${isbn}&count=${count}`, false)
            xhttp.send()
			const obj = JSON.parse(xhttp.responseText)
			if (obj.state){
				this.del(index)
				alert("purchase success")
			}
			else {
				alert("purchase failed")
			}
		},

		changeCartContent: function (isbn, num, callback) {
		    const self = this
			if (changingCartContent) return
			else {
				changingCartContent = true
			}
			const xhttp = new XMLHttpRequest();
			xhttp.open('GET', `shoppingcart/change?isbn=${isbn}&num=${num}`)
			xhttp.onreadystatechange = function () {
				if (this.readyState == 4 && this.status == 200) {
					changingCartContent = false
					callback()
					// TODO:xxx
				}
			}
			xhttp.send()
		}
	},
	created() {
		this.updateAll()
	},

});


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




