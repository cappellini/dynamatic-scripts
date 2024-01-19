# Indicate the path to Dynamatic's top-level directory here (leave unchanged if
# running the frontend from the top-level directory)
set-dynamatic-path  ./dynamatic

# Indicate the path the legacy Dynamatic's top-level directory here (required
# for write-hdl and simulate)
set-legacy-path     ./dynamatic-utils/legacy-dynamatic/dhls/etc/dynamatic

# Set the source file to run (kernel must have the same name as the filename,
# without the extension)
set-src             ./dynamatic/integration-test/fir/fir.c

# Compile (from source to Handshake IR/DOT)
# Remove the flag to run smart buffer placement (requires Gurobi)
compile


write-smv

# Simulate using Modelsim
# simulate

# Exit the frontend
exit

