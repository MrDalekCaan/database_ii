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




