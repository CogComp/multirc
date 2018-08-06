# SurfaceLR: Simple Logistic Regression Based QA

This is a simple baseline that makes use of our small training set, we reimplemented and trained a logistic regression model using word-based overlap
features. As described in (Merkhofer et al., 2018), this baseline takes into account the lengths of a text, question and each answer candidate,
as well as indicator features regarding the (co-)occurrences of any words in them.

## Usage
 
 Follow the instructions below: 
 
 - Unzip the folder which contains the liblinear files `liblinear.zip`. 
 - Compile liblinear by running make in the `liblinear/` subdirectory.
 - Download the training dataset forom the [website](http://cogcomp.org/multirc/) and train the system with the training data. 
 - To run the system on the train/dev/test data, use the command `sh run_surfaceLR.sh`.
    - Note: The files have to be in the Same directory as the scripts, they must end in ".json", and train file must contain "train" (similar pattern for test and dev).
 - The system will create one output .JSON file (`.withLRscores.json`) for each dev/test file in the current directory.
 
 
