import sqlite3
from db import db
from passlib.apps import custom_app_context as pwd_context
from binascii import hexlify
from models.algo import algoModel
from sqlalchemy.dialects.postgresql import TIME
from datetime import datetime
import os

class CoinModel(db.Model): 
	__tablename__ = 'Coins'

	id = db.Column(db.Integer, primary_key=True)
	algo_id = db.Column(db.Integer,db.ForeignKey('Algos.id'))
	name = db.Column(db.String(20))
	url = db.Column(db.String(50))

	algo = db.relationship("AlgoModel",back_populates = "coins")
	
	def __init__(self,algo_id,name,**data):
		self.algo_id = algo_id
		self.name = name.lower()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

	@classmethod
	def coin_check(cls,data,model):
		coin = model
		algo = None

		if not coin:
			coin = cls.find_by_name(algo.id,data.get('coin_name'))
	
		data['name'] = data.get('coin_name')

		return coin,data

	def update_data(self,input_dict):
		var_dict = self.__dict__
		for key,value in input_dict.items():
			if key in var_dict and value is not None:
				if type(value) is str:
					value = value.strip().lower()
				setattr(self,key,value)

	def json(self):
		return {'id':self.id,'algo_name': self.algo.name, 'algo_id':self.algo.id, 'name':self.name}

	def return_algo(self):
		return self.algo

	@classmethod
	def find_by_name(cls,name):
		return cls.query.filter_by(name=name.strip().lower()).first()

	@classmethod
	def find_by_name_or_id(cls,name,iD):
		coin = None
		if type(name) is str:
			coin = cls.query.filter_by(name=name.lower()).first()
		if not coin and iD is not None : 
			coin = cls.query.filter_by(id = iD).first()

		return coin

	@classmethod
	def find_by_id(cls,iD):
		return cls.query.filter_by(id=iD).first()



