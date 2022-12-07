make : run
	
run : 
	python3 main.py

run_input :
	python3 input.py

setup :
	pip install eel

clean :
	__pycache__