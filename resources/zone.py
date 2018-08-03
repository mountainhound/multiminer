from flask_restful import Resource, reqparse
from models.zone import ZoneModel
from models.stall import StallModel
from models.lot import LotModel
from models.api import ApiModel
from security import login_required,key_required
from utils.data_utils import purge_dict
import time
from operator import itemgetter
from multiprocessing.dummy import Pool as ThreadPool
from utils.restful_resource_utils import create_request_parser, fopark_type_time, fopark_type_datetime
from utils.wrapper_utils import required_args
import requests
from datetime import datetime

default_argument_list = [
			{"argument_name":"client_name",
				"required": False,
				"help":"Camera Name, Required",
				"type": str
			},
			{"argument_name":"zone_name",
				"required": False,
				"help":"Zone Name/Descriptor",
				"type": str
			},
			{"argument_name":"id",
				"required": False,
				"help":"Zone Unique ID",
				"type": int
			},
			{"argument_name":"api_key",
				"required": False,
				"help":"API_KEY for Authentication",
				"type": str
			},
			{"argument_name":"api-key",
				"required": False,
				"help":"API_KEY for Authentication",
				"type": str,
				"location": "headers"
			}
	]

class Zone(Resource):

	argument_list = [
			{"argument_name":"time_limit",
				"required": False,
				"help":"Parking Time Limit i.e. 120 (minutes)",
				"type": int
			},
			{"argument_name":"start_time",
				"required": False,
				"help":"Start Time for Zone i.e. 08:00:00+00",
				"type": fopark_type_time
			},
			{"argument_name":"end_time",
				"required": False,
				"help":"Status for Camera Network, i.e 200,300,400,500,",
				"type": fopark_type_time
			},
			{"argument_name":"weekend_flag",
				"required": False,
				"help":"Whether or Not Rules are enforced on Weekends",
				"type": int
			},
			{"argument_name":"color",
				"required": False,
				"help":"rgb(255,255,255)",
				"type": str
			}
		]

	args_parser = create_request_parser((argument_list+default_argument_list),location = "args")
	parser = create_request_parser((argument_list+default_argument_list))

	@required_args(args_parser, args_list = ['client_name','zone_name'], sec_group = 2, key_required = True, class_model = ZoneModel)
	def get(self,data,request_user = None, model = None):

		client,zone,data = ZoneModel.zone_check(data,model)

		if not client: 
			return {"message": "A client with that name does not exist, please create clients first."}, 404

		if not zone: 
			return {"message": "A zone with that name does not exist"}, 404
		
		if request_user.client.id == client.id or request_user.security_group < 1:
			return zone.json()

		return {"message":"User Not Authorized"},404

	@required_args(parser, args_list = ['client_name','zone_name'], sec_group = 1, key_required = True, class_model = ZoneModel)
	def post(self,data,request_user = None, model = None):
		
		client,zone,data = ZoneModel.zone_check(data,model)

		if not client: 
			return {"message": "A client with that name does not exist, please create client first."}, 404

		if zone: 
			return {"message": "A Zone with that name already exists"}, 404
		
		data = purge_dict(data)
		data.pop('api_key',None)
		data.pop('client_name',None)
		
		if request_user.client.id == client.id or request_user.security_group < 1:
			zone = ZoneModel(client.id,**data)
			zone.save_to_db()
			return zone.json()

		return {"message":"User Not Authorized"},404

	@required_args(parser, args_list = ['client_name','zone_name'], sec_group = 1, key_required = True, class_model = ZoneModel)
	def put(self,data,request_user = None, model = None):
				
		client,zone,data = ZoneModel.zone_check(data,model)

		if not client: 
			return {"message": "A lot with that name does not exist, please create lot first."}, 404

		if not zone: 
			return {"message": "A zone with that name does not exist"}, 404

		data = purge_dict(data)
		data.pop('api_key',None)
		data.pop('client_name',None)

		if request_user.client.id == client.id or request_user.security_group < 1:
			zone.update_data(data)
			
			zone.save_to_db()
			return zone.json()

		return {"message":"User Not Authorized"},404

	@required_args(parser, args_list = ['client_name','zone_name'], sec_group = 1, key_required = True, class_model = ZoneModel)
	def delete(self,data,request_user = None, model = None):
		
		client,zone,data = ZoneModel.zone_check(data,model)

		if not client: 
			return {"message": "A client with that name does not exist, please create client first."}, 404

		if not zone: 
			return {"message": "A zone with that name does not exist"}, 404

		if request_user.client.id == client.id or request_user.security_group < 1:
			zone_name = zone.name
			zone.delete_from_db()
			return {'message':'Zone: {} has been removed from database.'.format(zone_name)}

		return {"message":"User Not Authorized"},404

