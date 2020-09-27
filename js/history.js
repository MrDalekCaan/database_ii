var gettingShoppingCart = false
var app = new Vue({
	el: '#aspace2',
	data: {
		books: [],
		pageName: "history"
	},
	methods: {
		curTitle: function() {
			return this.titles[this.selected[0]].titles[this.selected[1]];
		},
		update: function(index) {
			const self = this
			var cart = xmlRequest( ()=> {
				if (cart.length > index) {
					self.$set(self.books, index, cart[index])
				}
			})
		},
		updateAll: function() {
			var cart = xmlRequest()
			this.books = cart

		},
		del: function (index) {
			var id = this.books[index]
			 changeCartContent(id, 0)
			 this.updateAll()
		}
	},
	created() {
		var xhttp = new XMLHttpRequest()
		xhttp.open("GET", "history", false)
        xhttp.send()
		var obj = JSON.parse(xhttp.responseText)
		this.books = obj.content
	},
		
});

// TODO: refact this function name
function xmlRequest(callback) {
	if (gettingShoppingCart) {
		return
	}
	else {
		gettingShoppingCart = false
	}
	var xhttp = new XMLHttpRequest()
	xhttp.open("GET", "shoppingcart", false)
	xhttp.onreadystatechange = () => {
		if (this.readyState == 4 && this.status == 200) {
			var obj;
			try {
				obj = JSON.parse(xhttp.responseText)
				callback(obj.content)
			} catch(e) {
				console.error("xml json parse error")
			}
			gettingShoppingCart = false
		} else if (this.status >= 400) {
			gettingShoppingCart = false
		}	
	}
	xhttp.send()
}




