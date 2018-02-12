csv_iterator reads every row of the csv file and passes it to the iterator action for processing. It is intended to be utility so you dont have to copy and paste the code of simply iterating over a file and creating an output csv. The iterator action must in turn return a row that will go on the output file.

Simply call the function iterate_over in your code with your custom iterator action. 

An iterator action can inherit the iterator_action class. You can write your own using that as a template

TODO
* No output file, only input file: Support for scenario where output file is None. Although a better solution is to pass along a row-wise status using the row key 