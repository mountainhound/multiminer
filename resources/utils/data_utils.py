def purge_dict(input_dict):
	output_dict = input_dict
	for key,value in input_dict.items():
		if value is None:
			output_dict.pop(key)

	return output_dict