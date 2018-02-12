import pandas as pd
import logging
import time
from iterator_action import iterator_action

def iterate_over(iterator_action,
		input_filename = "data/input.csv", output_filename = 'data/output.csv', 
		row_key_fieldname = 'Address', SKIP_STATUS = "SKIP", WAIT_STATUS = 'OVER_QUERY_LIMIT', 
		BACKOFF_TIME = 30, PRINT_STATUS_FOR = 10, SAVE_FILE_FOR = 50):
	# Set the basics 

	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger(__name__)

	#--------------------TESTING----------------------

	# Test the iterator action before we start
	logger.info("Testing the %s iterator action"% iterator_action.get_action_verb())
	test_result = iterator_action.test_iterator_action()
	if (test_result['status'] != 'OK'):
	    logger.warning("There was an error when testing the %s iterator."% iterator_action.get_action_verb())
	    return
	logger.debug("completed testing: {}: {}".format(test_result, test_result['status']))
	#------------------ DATA LOADING --------------------------------
	logger.info("Begining %s all rows in file"% iterator_action.get_action_verb())
	# Read the data to a Pandas Dataframe
	data = pd.read_csv(input_filename, encoding='utf8')
	# Create a list to hold results
	results = []
	# Go through each row in turn
	for index, row in data.iterrows():
		
		completed = False
		while completed is not True:
	# Run the iterator action
			try:
				if row_key_fieldname and row.get(row_key_fieldname):
					logger.debug("Attempting: {}".format(row[row_key_fieldname]))
				else:
					logger.debug("Attempting: {}: {}".format("Row index: " , index))
				single_result = iterator_action.run_iterator_action(row)			
			except Exception as e:
	#------------------	DEFINITIONS -------------------------------
				logger.exception(e)
				logger.error("Major error with {}".format(row))
				logger.error("Skipping!")				
			completed = True
			# If the status is to wait for a certain period of time, then wait for the backoff time
		if single_result['status'] == WAIT_STATUS:
			logger.info("Hit wait status! Backing off for a bit. %s seconds"% BACKOFF_TIME)

			time.sleep(BACKOFF_TIME) # sleep for x seconds
			completed = False
		else:
			# Save the results
            # Note that the results might be empty / non-ok - log this
			if single_result['status'] != 'OK':
				single_result['status'] = SKIP_STATUS
				logger.warning("Error {} Row index: {}: {}".format(iterator_action.get_action_verb(),index, single_result['status']))
			if row_key_fieldname and row.get(row_key_fieldname):
				logger.debug("completed: {}: {}".format(row[row_key_fieldname], single_result['status']))
			else:
				logger.debug("completed: {}: {}".format(row, single_result['status']))
			results.append(single_result)
			completed = True

# Print status every 100 addresses
	if len(results) % PRINT_STATUS_FOR == 0:
		logger.info("Completed {} {} of {}".format(iterator_action.get_action_verb(), len(results), len(data)))
# Every 500 addresses, save progress to file(in case of a failure so you have something!)
	if len(results) % SAVE_FILE_FOR == 0:
		pd.DataFrame(results).to_csv("{}_bak".format(output_filename))

# All done
	logger.info("Finished {} all addresses".format(iterator_action.get_action_verb()))
# Write the full results to csv using the pandas library.
	pd.DataFrame(results).to_csv(output_filename, encoding='utf8')


def main():
	from iterator_action import iterator_action
	iterate_over(iterator_action())

if __name__ == '__main__':
	main()