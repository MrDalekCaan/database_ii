import unittest
import e_shop_user as eu
import backend as B

user = eu.login('1898048', 123456)


class TestUser(unittest.TestCase):

	# def test_purchase(self):
	# 	user.purchase('23439608', '20200202020202', 1)
	#
	# def test_add_shopping_cart(self):
	# 	user.add_shopping_cart('232', '20200202020202')

	def test_recommendation(self):
		print(B.get_personal_recommendation("1898048", 's', 's'))


if __name__ == "__main__":
	unittest.main()
