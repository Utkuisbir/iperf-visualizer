This python code has written to analyze iperf3 throughput results with visualizing every minute.

Create virtual environment and install requirement libraries:
1) python3 -m venv env (This command creates environment which named "env")
2) source env/bin/activate (This command activates "env" environment)
3) pip install -r requirements.txt 

You can use the following links to use virtual environment on your PC:

https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/ 
https://learnpython.com/blog/python-requirements-file/


How to run:
1) python3 <iperf3_json_visualizer.py> -i <jsonfilename.json> -w <iwconfigfilename.txt>  -l <limit_for_Mbit_to_show_on_table> 
* Type the json file name that you want it to be read.
* Type the iwconfig file name that you want it to be read. (Optional)
* Type the Mbit limit which speed you run with iperf3
2) Excel file will be created automatically.
3) Table will be created automatically.
4) deactivate (for virtual environment)
