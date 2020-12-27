#!/bin/bash
echo  "Hello sample-bash.sh"

echo "..."
echo "......"

echo "done"

# if you are just echoing some string without actually doing anything
# put a sleep statement to print out the string to OLED, else
# if wont be printed out (it's weird I know)
sleep 1

# Always return 0 before exiting (please...)
return 0
