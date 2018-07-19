#!/usr/bin/sh

if [ ! -f liblinear/train ]; then
    echo "Could not find LIBLINEAR executables!"
    echo "Please compile them in liblinear/"
    exit
fi

for f in "train_456.json" "test_0_83.json" "test_1_83.json" "test_2_83.json" "test_3_83.json" "test_4_83.json"
do
    if [ ! -f $f ]; then
	echo "Could not find data file $f"
	echo "Please put them in the current directory"
	exit
    fi
done

# run surfaceLR baseline
perl surfaceLR.pl
# fix scores in JSON output (string -> double)
sed -i 's/simpleLR":"\([^"]*\)"/simpleLR":\1/g' *.withLRscores.json

# remove temporary model/features/prediction files
rm -f multRC_train.feats.model *.preds *.feats
