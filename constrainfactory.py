import log
import re
from collections.abc import Iterable


class Constrain:
	def __init__(self):
		self.constraints = ""
		self._where = False
		self._from = False
		self._to = False
		self._like = False
		self._order = False
		self._where_change_last_time = False

	def __str__(self):
		result = re.sub(r"^ *AND *", "", self.constraints)
		result = re.sub(r" *AND *$", "", result)
		if self._where:
			result = " WHERE " + result
		return result

	def _where_check(self):
		self.where_change_last_time = False
		if not self._where:
			self._where_change_last_time = True
			self._where = True
			# log.debug("where add here")
			# self.constraints += ' WHERE '


	def _revert_where_check(self):
		if self.where_change_last_time:
			self._where = False
		

	def apply_constraint_region(self, property_name: str, region: list = None):
		"""
		:param property_name: str of property_name(column name)
		:param region: list of two number | None. Default None
		:return: condition for property_name
		"""
		if region is None or (region[0] is None and region[1] is None):
			return self
		try:
			self._where_check()
			if self._where:
				log.debug("where add apply_constraint_region")
			if None not in region:
				high = float(max(region))
				low = float(min(region))
				self.constraints += f" AND {low}<={property_name} AND {property_name}<={high}"
			elif region[0] is None:
				high = float(region[1])
				self.constraints += f" AND {property_name}<={high}"
			elif region[1] is None:
				low = float(region[0])
				self.constraints += f" AND {low}<={property_name}"
		except ValueError as e:
			self._revert_where_check()
			log.fatal(f"Invalid region constraint for {property_name}, get {region}.\nError: {e}")
		finally:
			return self

	def apply_constraint_value(self, property_names: [str], values=None):
		"""
		:param property_name:str of property_name(column name)
		:param values:
		:return: condition for property_name
		"""
		if values is None:
			return self
		try:
			self._where_check()
			# if type(values) == list:
			# 	if len(values) == 0:
			# 		return self
			if not isinstance(values, Iterable) or type(values) == str:
				values = [values]
			if not isinstance(property_names, Iterable) or type(property_names) == str:
				property_names = [property_names]
			for property_name in property_names:
				cons = ""
				for value in values:
					if type(value) == int or type(value) == float:
						cons += f" {property_name}={value} OR"
					else:
						cons += f" {property_name}='{value}' OR"
					# cons = f" {property_name}={value} OR"
				cons = re.sub(r"^ *OR *", "", cons)
				cons = re.sub(r" *OR *$", "", cons)
				self.constraints += f" AND {cons} "

			# if self._where:
			# 	log.debug("where add apply_constraint_value")
			# else:
			# 	if type(values) == int or type(values) == float:
			# 		self.constraints += f" AND {property_name}={values}"
			# 	else:
			# 		self.constraints += f" AND {property_name}='{values}'"

		except ValueError as e:
			self._revert_where_check()
			log.fatal(f"Invalid value constraint for {property_name}, get {values}.\nError: {e}")
		finally:
			return self

	def like(self, property_names: [str], pattern=None):
		if pattern is None:
			return self
		pattern = f"%pattern%"
		if not isinstance(property_names, Iterable) or type(property_names) == str:
			property_names = [property_names]
		self._where_check()
		if self._where:
			log.debug("where add like")
		cons = ""
		for property_name in property_names:
			cons += f" {property_name} LIKE '{pattern}' OR "
		cons = re.sub(r"^ *OR *", "", cons)
		cons = re.sub(r" *OR *$", "", cons)
		self.constraints += f" AND {cons} "
		return self

	def _check_integer(self, integer):
		if type(integer) == int:
			return True
		if type(integer) == str:
			return integer.isdigit()
		if type(integer) == float:
			return integer.is_integer()

	def from_(self, value):
		if not self._check_integer(value) or self._from:
			return self
		self._from = True
		self.constraints += f" LIMIT {value}"
		return self

	def limit(self, value):
		if not self._check_integer(value) or self._to:
			return self
		if not self._from:
			self.constraints += f" LIMIT 0, {value}"
			self._from = True
		else:
			self.constraints += f" ,{value}"
		self._to = True
		return self

	def order_by(self, property_name, way=None):
		if way is None:
			return self
		self.constraints += f" ORDER BY {property_name} {way}"
		return self




