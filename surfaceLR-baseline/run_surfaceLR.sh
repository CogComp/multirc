#!/usr/bin/sh

if [ ! -f liblinear/train ]; then
    echo "Could not find LIBLINEAR executables!"
    echo "Please compile them in liblinear/"
    exit
fi

# run surfaceLR baseline
perl surfaceLR.pl
# fix scores in JSON output (string -> double)
sed -i 's/simpleLR":"\([^"]*\)"/simpleLR":\1/g' *.withLRscores.json

# remove temporary model/features/prediction files
rm -f multRC.model *.preds *.feats
