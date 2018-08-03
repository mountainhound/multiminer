import sqlite3
from db import db
from passlib.apps import custom_app_context as pwd_context
from binascii import hexlify
from models.client import ClientModel
from sqlalchemy.dialects.postgresql import TIME
from datetime import datetime
import os

class SoftwareModel(db.Model): 
	__tablename__ = 'Softwares'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	mining_command = db.Column(db.String(60))

	algos = db.relationship("AlgoModel",back_populates = "software")
	
	def __init__(self,name,mining_command = None,**data):
		self.name = name.lower()
		self.mining_command = mining_command

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

	@classmethod
	def software_check(cls,data,model):
		software = model
		client = None

		if not software:
			software = cls.find_by_name(data.get('software_name'))

		data['name'] = data.get('software_name')

		return software,data

	def update_data(self,input_dict):
		var_dict = self.__dict__
		for key,value in input_dict.items():
			if key in var_dict and value is not None:
				if type(value) is str:
					value = value.strip().lower()
				setattr(self,key,value)

	def json(self):
		return {'id':self.id,,'name':self.name}

	def return_client(self):
		return self.client

	@classmethod
	def find_by_name(cls,name):
		return cls.query.filter_by(name=name.strip().lower()).first()

	@classmethod
	def find_by_name_or_id(cls,name,iD):
		software = None
		if type(name) is str:
			software = cls.query.filter_by(name=name.lower()).first()
		if not software and iD is not None : 
			software = cls.query.filter_by(id = iD).first()

		return software

	@classmethod
	def find_by_id(cls,iD):
		return cls.query.filter_by(id=iD).first()



