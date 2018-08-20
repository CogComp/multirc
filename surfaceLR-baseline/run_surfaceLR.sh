#!/usr/bin/sh

if [ ! -f liblinear/train ]; then
    echo "Could not find LIBLINEAR executables!"
    echo "Please compile them in liblinear/"
    exit
fi

# train surfaceLR baseline
echo "Training surfaceLR baseline ..."
perl surfaceLR_train.pl train_456-fixedIds.json
# remove temporary model/features/prediction files
rm -f *.preds *.feats

# run surfaceLR baseline
echo "Generating surfaceLR predictions ..." 
perl surfaceLR_predict.pl dev_83-fixedIds.json dev_83-fixedIds.withLRscores.json
# remove temporary model/features/prediction files
rm -f *.preds *.feats
