from werkzeug.security import safe_str_cmp
from models.user import UserModel
import email_utility
from data_utils import purge_dict

def required_args(parser, args_list = [],sec_group = 0,key_required = True,login_required = False, class_model = None):
	def decorator(func):
		def wrapper(*args,**kwargs):

			def json_shutdown(messasge,*args,**kwargs):
				return {'message':message}, 401
			
			data = parser.parse_args()
			api_key = data.get('api_key')
			if not api_key: 
				api_key = data.get('X-api-key')
			model = None
			user = None
			if key_required:
				user = UserModel.find_by_key(api_key)
				if not user or not user.verify_key(api_key) or not (user.security_group <= sec_group):
					message = "Not Authenticated"
					return json_shutdown(message,*args,**kwargs)
			
			elif login_required:
			
				username = data.get('username')
				password = data.get('password')
				print password
				print username

				user = UserModel.find_by_username(username)
				
				if not user or not password:
					message = "Password or User"
					return json_shutdown(message,*args,**kwargs)
				if not user.verify_password(password):
					message =  "Verify Password"
					return json_shutdown(message,*args,**kwargs)
				if not user.security_group <= sec_group:
					message =  "Security Group"
					return json_shutdown(message,*args,**kwargs)
				
			
			if data.get('id') is None: 
				for arg in args_list:
					key = None
					if type(arg) is list:
						for option in arg: 
							if option in data.keys(): 
								if data.get(option) is not None:
									key = option
					else: 
						if arg in data.keys(): 
							key = arg

					if data.get(key) is None: 
						message = "Required argument: {} not included".format(arg)
						return json_shutdown(message,*args,**kwargs)

			elif class_model: 
				model = class_model.find_by_id(data.get('id'))

			data = purge_dict(data)
			data.pop('id',None)
			data.pop('api_key',None)
			data.pop('X-api-key',None)

			return func(data = data,request_user = user,model = model,*args,**kwargs)
		return wrapper
	return decorator






	