from build_database import main
import e_shop_user as eu
import json


main()
user_id = eu.register("flor", "123456")
eu.e_shop_cursor.execute(f"INSERT INTO user(user_name, user_id, password, type) VALUES('admin', '000000', '000000', '0000')")
with open("defaultuser.json". 'w') as file:
	json.dump(file, {"customer": {
			"username": "flor",
			"password": "123456",
			"userid": user_id
		},
		"admin": {
			"username": "admin",
			"password": "000000",
			"userid": "000000"
		}
	})

