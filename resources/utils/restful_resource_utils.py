from flask_restful import Resource, reqparse
from dateutil import parser as dtparser


def create_request_parser(argument_list,location = ['values','json']):
	parser = reqparse.RequestParser()
	for argument_dict in argument_list:
		parser.add_argument(argument_dict.get('argument_name'),
			location = argument_dict.get('location',location),
			required = argument_dict.get('required'),
			action = argument_dict.get('action'),
			type = argument_dict.get('type'),
			help = argument_dict.get('help')
			)
	return parser

def fopark_type_datetime(value):
	fopark_time = None

	try: 
		fopark_time = dtparser.parse(str(value))
	except Exception as err:
		print err
		print "Error: {}".format(err)
		raise ValueError("Could not parse value into datetime object")

	return fopark_time

def fopark_type_time(value):
	fopark_time = fopark_type_datetime(value)

	return fopark_time.time()

