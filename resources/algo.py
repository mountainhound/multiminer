from flask_restful import Resource, reqparse
from models.algo import AlgoModel
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
			{"argument_name":"name",
				"required": False,
				"help":"Camera Name, Required",
				"type": str
			},
			{"argument_name":"id",
				"required": False,
				"help":"algo Unique ID",
				"type": int
			},
			{"argument_name":"software_name",
				"required": False,
				"help":"software for mining algo",
				"type": str
			},
			{"argument_name":"software_id",
				"required": False,
				"help":"software_id for mining algo",
				"type": str
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

class Algo(Resource):

	argument_list = [
			{"argument_name":"hashrate",
				"required": False,
				"help":"Hashrate in MH/s",
				"type": float
			}
		]

	args_parser = create_request_parser((argument_list+default_argument_list),location = "args")
	parser = create_request_parser((argument_list+default_argument_list))

	default_required_args = ['name',['software_id','software_name']]

	@required_args(args_parser, args_list = default_required_args, sec_group = 2, key_required = True, class_model = AlgoModel)
	def get(self,data,request_user = None, model = None):

		software,algo,data = AlgoModel.algo_check(data,model)

		if not software: 
			return {"message": "A software with that name does not exist, please create softwares first."}, 404

		if not algo: 
			return {"message": "A algo with that name does not exist"}, 404
		
		if request_user.software.id == software.id or request_user.security_group < 1:
			return algo.json()

		return {"message":"User Not Authorized"},404

	@required_args(parser, args_list = default_required_args, sec_group = 1, key_required = True, class_model = AlgoModel)
	def post(self,data,request_user = None, model = None):
		
		software,algo,data = AlgoModel.algo_check(data,model)

		if not software: 
			return {"message": "A software with that name does not exist, please create software first."}, 404

		if algo: 
			return {"message": "A algo with that name already exists"}, 404
		
		data = purge_dict(data)
		data.pop('api_key',None)
		data.pop('software_name',None)
		
		if request_user.software.id == software.id or request_user.security_group < 1:
			algo = AlgoModel(software.id,**data)
			algo.save_to_db()
			return algo.json()

		return {"message":"User Not Authorized"},404

	@required_args(parser, args_list = default_required_args, sec_group = 1, key_required = True, class_model = AlgoModel)
	def put(self,data,request_user = None, model = None):
				
		software,algo,data = AlgoModel.algo_check(data,model)

		if not software: 
			return {"message": "A lot with that name does not exist, please create lot first."}, 404

		if not algo: 
			return {"message": "A algo with that name does not exist"}, 404

		data = purge_dict(data)
		data.pop('api_key',None)
		data.pop('software_name',None)

		if request_user.software.id == software.id or request_user.security_group < 1:
			algo.update_data(data)
			
			algo.save_to_db()
			return algo.json()

		return {"message":"User Not Authorized"},404

	@required_args(parser, args_list = default_required_args, sec_group = 1, key_required = True, class_model = AlgoModel)
	def delete(self,data,request_user = None, model = None):
		
		software,algo,data = AlgoModel.algo_check(data,model)

		if not software: 
			return {"message": "A software with that name does not exist, please create software first."}, 404

		if not algo: 
			return {"message": "A algo with that name does not exist"}, 404

		if request_user.software.id == software.id or request_user.security_group < 1:
			algo_name = algo.name
			algo.delete_from_db()
			return {'message':'algo: {} has been removed from database.'.format(algo_name)}

		return {"message":"User Not Authorized"},404

