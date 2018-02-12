class iterator_action():

	def get_action_verb(self):
		return "Showing"

	def test_iterator_action(self):
		input = {"iterator_name":self.get_action_verb()}
		return self.run_iterator_action(input)

	def run_iterator_action(self, input):		
		input['status'] = "OK"
		print(input)
		return input
def main():
	iterator_action().test_iterator_action()

if __name__ == '__main__':
	main()