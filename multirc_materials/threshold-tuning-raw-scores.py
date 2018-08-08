## A utility function to binarize the real-valued scores
import json
import numpy as np
from measures import Measures

# this is the location of your data; has to be downloaded from http://cogcomp.org/multirc/
inputFile = '/Users/daniel/ideaProjects/hard-qa/splitv1/dev_83-with-lucene.json'

measures = Measures()

def main():
    # tune_threshold('/Users/daniel/ideaProjects/multirc/baseline-scores/raw/simpleLR-raw.json')
    # convert_to_binary('/Users/daniel/ideaProjects/multirc/baseline-scores/raw/simpleLR-raw.json',
    #                   '/Users/daniel/ideaProjects/multirc/baseline-scores/simpleLR.json', -0.76)
    # tune_threshold('/Users/daniel/ideaProjects/multirc/baseline-scores/raw/lucene_paragraphs-raw.json')
    # convert_to_binary('/Users/daniel/ideaProjects/multirc/baseline-scores/raw/lucene_paragraphs-raw.json',
    #                   '/Users/daniel/ideaProjects/multirc/baseline-scores/lucene_paragraphs.json', 0.0499)
    # tune_threshold('/Users/daniel/ideaProjects/multirc/baseline-scores/raw/lucene_world-raw.json')
    convert_to_binary('/Users/daniel/ideaProjects/multirc/baseline-scores/raw/lucene_world-raw.json',
                        '/Users/daniel/ideaProjects/multirc/baseline-scores/lucene_world.json', 0.56)


def convert_to_binary(outFile, exported_file, threshold):
    output = json.load(open(outFile))
    for a in output:
        a["scores"] = binarize(a["scores"], threshold)

    with open(exported_file, 'w') as outfile:
        json.dump(output, outfile)


def binarize(scores, th):
    return [1.0 if s > th else 0.0 for s in scores]

def tune_threshold(outFile):
    input = json.load(open(inputFile))
    output = json.load(open(outFile))

    for th in np.arange(-0.5, 1.0, 0.02):
        input_binarized = dict([[a["pid"] + "==" + a["qid"], binarize(a["scores"], th)] for a in output])
        [P1, R1, F1m] = measures.per_question_metrics(input["data"], input_binarized)
        print("Threshold: " + str(th) + " \tP: " + str(P1) + " - R: " + str(R1) + " - F1m: " + str(F1m))

if __name__ == "__main__":
    main()
