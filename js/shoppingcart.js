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
			this.changeCartContent(isbn, count, function() {
				// self.update(index)
				self.updateAll()
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
			this.changeCartContent(isbn, count, function () {
				// self.update(index)
				self.updateAll()
			})
		},
		// update: function(index) {
		// 	const self = this
		// 	requestAllShoppingCart(cart => {
		// 		if (cart.length > index) {
		// 			self.$set(self.books, index, cart[index])
		// 		}
		// 	})
		// },
		updateAll: function() {
			const self = this
			requestAllShoppingCart(async cart => {
				self.books = cart
                for (let i = 0; i < self.books.length; i++) {
                	// await new Promise(r => setTimeout(r, 100))
					// get_single_book(self.books[i].ISBN, true, book => {
					// 	self.$set(self.books, i, Object.assign(self.books[i], book))
					// })
                    let book = get_single_book(self.books[i].ISBN, false)
					self.$set(self.books, i, Object.assign(self.books[i], book))
				}
			})
		},
		del: function (index) {
			var isbn = this.books[index].ISBN
            const self = this
			 self.changeCartContent(isbn, 0, function() {
			 	self.updateAll()
			 })
		},
		buyThisOne: function(index) {
			if (changingCartContent) {
				alert("您操作的太快了")
                return
			} else {
				changingCartContent = true
			}
			const isbn = this.books[index].ISBN
			const count = this.books[index].count
			let xhttp = new XMLHttpRequest()
			const self = this
			xhttp.open("GET", `purchase?isbn=${isbn}&count=${count}`)
			xhttp.onreadystatechange = function () {
				if (xhttp.readyState == 4 && xhttp.status == 200) {
				    changingCartContent = false
					const obj = JSON.parse(xhttp.responseText)
					if (obj.state){
						self.del(index)
						alert("purchase success")
					}
					else {
						alert("purchase failed")
					}
				}
				else if (xhttp.status == 500) {
					changingCartContent = false
					alert("purchase failed")
				}
			}
            xhttp.send()
		},

		changeCartContent: function (isbn, num, callback=()=>{}) {
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
				if (xhttp.readyState == 4 && xhttp.status == 200) {
					callback()
				}
				else if (xhttp.status >= 400) {
					console.log("change cart content failed")
				}
				changingCartContent = false
			}
			xhttp.send()
		},
		onChange: function(index, event) {
			let count = parseInt(event.target.value)
			if (count < 0) {
				this.$set(this.books, index, this.books[index])
				return
			}
			var isbn = this.books[index].ISBN
			this.changeCartContent(isbn, count, ()=>{
				this.updateAll()
			})
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

function requestAllShoppingCart(callback) {
	const xhttp = new XMLHttpRequest();
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




