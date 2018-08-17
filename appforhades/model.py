from sklearn.externals import joblib
import os
import pickle
from models import Pipe
import datetime



class Model():
	_model = None
	_instance = None
	_sub_areas = []

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = object.__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		pass

	def load(self, file_name):
		__class__._model = joblib.load(file_name)

	def predict(self, form):
		try:
			sub_area = form.sub_area.choices[int(form.sub_area.data)][1]
			params = [(form.full_sq.data, form.life_sq.data, form.floor.data,
					   form.max_floor.data, form.num_room.data, form.build_year.data,
					   form.timestamp.data, sub_area )]
			return int(__class__._model.predict(params)[0])
		except Exception as e:
			print(e)
			return 0

	def get_sub_area_list(self):
		if not __class__._sub_areas:
			__class__._sub_areas = sorted(self._model.get_sub_areas())
		return __class__._sub_areas


if __name__ == '__main__':
	model = Model()
	model.load('model.jlib')
	print(Model().get_sub_area_list())
	print(Model()._model.predict([(55,50,3,2,1,2016,datetime.date(2018, 8, 17),'Cheremushki')]))
	print(Model()._model.predict([(55,50,3,2,1,2016,datetime.date(2010, 8, 17),'Cheremushki')]))
	print(Model()._model.predict([(55,50,3,2,1,2016,'2016-08-08','Ostankinskoe')]))
	print(Model()._model.predict([(55,50,3,2,10,2016,'2016-08-08','Ostankinskoe')]))
	print(Model()._model.predict([(55,50,3,2,100,2016,'2016-08-08','Ostankinskoe')]))

