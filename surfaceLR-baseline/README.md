# SurfaceLR: Simple Logistic Regression Based QA

This is a simple baseline that makes use of our small training set, we reimplemented and trained a logistic regression model using word-based overlap
features. As described in (Merkhofer et al., 2018), this baseline takes into account the lengths of a text, question and each answer candidate,
as well as indicator features regarding the (co-)occurrences of any words in them.

## Usage
 
 Follow the instructions below: 
 
 - Unzip the folder which contains the liblinear files `liblinear.zip`. 
 - Download the training dataset forom the [website](http://cogcomp.org/multirc/) and train the system with the training data. 
 - To evaluate the system on the test data, run the command below: 
 
 
 
 
 