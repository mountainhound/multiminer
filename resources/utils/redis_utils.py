import json 
import uuid
import time

def redis_predictor(rd,img_str):
	try: 
		if rd.ping():
			k = str(uuid.uuid4())
			d = {"id": k, "image": img_str,"timestamp":time.time()}
			rd.rpush("image_queue", json.dumps(d))
			rd_ts = time.time()
			current_time = rd_ts
			max_wait = 8 #seconds
			time_break = False
			while True and not time_break: 
				output = rd.get(k)

				# check to see if our model has classified the input
				# image
				if output is not None:
					# add the output predictions to our data
					# dictionary so we can return it to the client
					output = output.decode("utf-8")

					# delete the result from the database and break
					# from the polling loop
					rd.delete(k)
					break
				time.sleep(0.25)

				if int(current_time - rd_ts) < max_wait:
					time_break = True

			if not time_break: 
				# indicate that the request was a success
				prediction = float(json.loads(output)[0].get('prediction'))
				return True, prediction
			elif time_break: 
				rd.delete(k)
				return True, None
		else: 
			return False, None
	except Exception as err:
		print "Redis Connection Error: {}".format(err)
		return False, None
