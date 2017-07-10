import os
import sys

args = sys.argv
if len(args) != 4:
    print("python GrepTheWeb.py <inputFile> <outputDirectory> <regex>")
    sys.exit(1)
os.system("/usr/local/hadoop/bin/hadoop jar \
     /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -D mapred.reduce.tasks=1 \
    -input " + args[1] +" \
    -mapper grepmapper.py \
    -reducer grepreducer.py \
    -file grepmapper.py \
    -output " + args[2] +" \
    -cmdenv SEARCH_STRING=" + args[3])
sys.exit(1)
