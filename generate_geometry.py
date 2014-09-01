from gla import *
from model_parse import *
import time

# Get information about which mesh to use:
INPUT_FILE = "Resources/kamCube.mesh.xml"
OUTPUT_FILE = "./Run.txt"
FILE_DATA = Parse(INPUT_FILE)
NUM_RUNS = 25000 # Number of times to run algorithm
PRINT_FREQ = 5000 # Print every nth run to file
POPULATION_SIZE = 150
ELITE = True
MUTATE_RATE = 0.0008
CROSS_RATE = 0.7
IMMIGRATION_RATE = 0.28
SPECIAL_CONSIDERATIONS = "Added minimizing volume factor to scoring function."

# For debugging purposes only:
PRINT_PERCENT = True
PERCENT_EPSILON = 0.05 # In percent

begin_time = time.time()

# Create our genetic learning algorithm:
final = gla(Score_Brute, FILE_DATA, POPULATION_SIZE, ELITE, MUTATE_RATE, CROSS_RATE, IMMIGRATION_RATE)

fout = open(OUTPUT_FILE, 'w')
fout.write("---BEGIN GLA---\n\nNUM_RUNS: " + str(NUM_RUNS) + "\nREPORT_FREQUENCY: " + str(PRINT_FREQ) + "\nMESH_FILE: " + INPUT_FILE)
fout.write("\nPOPULATION_SIZE: " + str(POPULATION_SIZE) + "\nELITISM: ")
fout.write("Yes") if ELITE else fout.write("No")
fout.write("\nCROSSOVER_RATE: " + str(CROSS_RATE) + "\nMUTATE_RATE: " + str(MUTATE_RATE) + "\nIMMIGRATION_RATE: " + str(IMMIGRATION_RATE))
fout.write("\nSPECIAL CONSIDERATIONS: " + str(SPECIAL_CONSIDERATIONS))
fout.write("\n\n\n")

for i in xrange(1, NUM_RUNS + 1):
	final.Generation()
	if (i % PRINT_FREQ == 1):
		fout.write("---------ITERATION " + str(i) + "---------\n")
		fout.write(str(final))
		fout.write("\n\n\n")
	if PRINT_PERCENT:
		if i % (NUM_RUNS * (PERCENT_EPSILON / 100.)) < 1.:
			print (float(i) / float(NUM_RUNS)) * 100,"%"

print "\n------------WINNER-------------"
fout.write("\n------------WINNER-------------\n")
print str(final.genes[0][0]),"with a score of:",str(final.genes[0][1])
fout.write(str(final.genes[0][0]) + " with a score of: " + str(final.genes[0][1]) + "\n")
for i in range(0, final.genes[0][0].GetNumObjects()):
	print final.genes[0][0].getString(i)
	fout.write(final.genes[0][0].getString(i) + "\n")

end_time = time.time()
elapsed = end_time - begin_time

print secondsToElapsed(elapsed)
fout.write("\n\n" + secondsToElapsed(elapsed))