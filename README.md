# simgen

Little python script to generate random Euroscope scenario files.

# Installation
1. Install Python: https://www.python.org/downloads/
2. Navigate to the simgen folder in a command line window
3. Install the dependencies with the following command: pip install -r requirements.txt

# Usage
1. Navigate to the simgen folder in a command line window
2. Execute eddf.py for Frankfurt or edds.py for Stuttgart, (python eddf.py -h | python edds.py -h) outputs the required parameters.
3. Choose runway in use [7,25] and ACFT/hr for all fixes given by the help flag.
4. Run the file with the parameters from above, the program will write the sim to the output file, which can then be used in Euroscope. The program prints the total amount of aircraft over the two hour long sim in the console.
