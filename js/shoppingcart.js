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
			const self = this
			const isbn = self.books[index].ISBN;
			const obj = self.books[index];
			let count = parseInt(obj.count) + 1
			changeCartContent(isbn, count, function() {
				self.update(index)
			})
		},
		subone:function (index) {
			const self = this
			var isbn = self.books[index].ISBN
			var obj = self.books[index]
			let count = parseInt(obj.count) - 1
			if (count <= 0) {
				return
			}
			changeCartContent(isbn, count, function () {
				self.update(index)
			})
		},
		update: function(index) {
			const self = this
			xmlRequest(cart => {
				if (cart.length > index) {
					self.$set(self.books, index, cart[index])
				}
			})
		},
		updateAll: function() {
			const self = this
			xmlRequest(cart => {
				self.books = cart
			})
		},
		del: function (index) {
			var isbn = this.books[index].ISBN
			 changeCartContent(isbn, 0, function() {
			 	this.updateAll()
			 })
		},
		buyThisOne: function(index) {
			if (changingCartContent) {
				alert("您操作的太快了")
			} else {
				changingCartContent = true
			}
			const isbn = this.books[index].ISBN
			const count = this.books[index].count
			let xhttp = new XMLHttpRequest()
			xhttp.open("GET", `purchase?isbn=${isbn}&count=${count}`)
			xhttp.onreadystatechange = function () {
				if (this.readyState == 4 && this.status == 200) {
					const obj = JSON.parse(this.responseText)
					if (obj.state){
						this.del(index)
						alert("purchase success")
					}
					else {
						alert("purchase failed")
					}
				}
			}
            xhttp.send()
		},

		changeCartContent: function (isbn, num, callback) {
		    const self = this
			if (changingCartContent) {
				alert("您操作的太快了")
				return
			}
			else {
				changingCartContent = true
			}
			const xhttp = new XMLHttpRequest();
			xhttp.open('GET', `shoppingcart/change?isbn=${isbn}&num=${num}`)
			xhttp.onreadystatechange = function () {
				if (this.readyState == 4 && this.status == 200) {
					changingCartContent = false
					callback()
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

function xmlRequest(callback) {
	var xhttp = new XMLHttpRequest()
	xhttp.open("GET", "shoppingcart")
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			var obj;
			try {
				obj = JSON.parse(xhttp.responseText)
			} catch(e) {
				console.log("xml json parse error")
				return [];
			}
			callback(obj.content)
		}
	}
	xhttp.send()
}




