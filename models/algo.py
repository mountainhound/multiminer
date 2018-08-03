import sqlite3
from db import db
from passlib.apps import custom_app_context as pwd_context
from binascii import hexlify
from models.client import ClientModel
from sqlalchemy.dialects.postgresql import TIME
from datetime import datetime
import os

class AlgoModel(db.Model): 
	__tablename__ = 'Algos'

	id = db.Column(db.Integer, primary_key=True)
	software_id = db.Column(db.Integer,db.ForeignKey('Sofwares.id'))
	name = db.Column(db.String(20))
	hashrate = db.Column(db.Float)
	hashrate_unit = db.Column(db.String(10))

	software = db.relationship("SoftwareModel",back_populates = "algos")
	coins = db.relationship("CoinsModel",back_populates = "algo")

	def __init__(self,software_id,name,**data):
		self.software_id = software_id
		self.name = name.lower()
		self.hashrate = hashrate
		self.hashrate_unit = "MH/s"

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

	@classmethod
	def algo_check(cls,data,model):
		algo = model
		software = None

		if not algo:
			software = SoftwareModel.find_by_name_or_id(data.get('software_name'),data.get('software_id'))
			
			if software: 
				algo = cls.find_by_name(data.get('algo_name'))
		else: 
			software = algo.software

		data['name'] = data.get('algo_name')

		return software,algo,data

	def update_data(self,input_dict):
		var_dict = self.__dict__
		for key,value in input_dict.items():
			if key in var_dict and value is not None:
				if type(value) is str:
					value = value.strip().lower()
				setattr(self,key,value)

	def json(self):
		return {'id':self.id,'software_name': self.software.name, 'software_id':self.software.id, 'hashrate':self.hashrate, 'hashrate_unit':self.hashrate_unit }

	def return_client(self):
		return self.software

	@classmethod
	def find_by_name(cls,name):
		return cls.query.filter_by(name=name.strip().lower()).first()

	@classmethod
	def find_by_name_or_id(cls,name,iD):
		algo = None
		if type(name) is str:
			algo = cls.query.filter_by(name=name.lower()).first()
		if not algo and iD is not None : 
			algo = cls.query.filter_by(id = iD).first()

		return algo

	@classmethod
	def find_by_id(cls,iD):
		return cls.query.filter_by(id=iD).first()



