### Evaluation script used for evaluation of baselines for MultiRC dataset
# The evaluation script expects the questions, and predicted answers from separate json files.
# The predicted answers should be 1s and 0s (no real-valued scores)

import json

from multirc_measures import Measures

# this is the location of your data; has to be downloaded from http://cogcomp.org/multirc/
inputFile = '/Users/daniel/ideaProjects/hard-qa/splitv1/dev_83-with-lucene.json'

measures = Measures()

def main():
    eval('baseline-scores/human-01.json')
    # eval('baseline-scores/allOnes.json')
    # eval('baseline-scores/allZeros.json')
    # eval('baseline-scores/simpleLR.json')
    # eval('baseline-scores/lucene_world.json')
    # eval('baseline-scores/lucene_paragraphs.json')

# the input to the `eval` function is the file which contains the binary predictions per question-id
def eval(outFile):
    input = json.load(open(inputFile))
    output = json.load(open(outFile))
    output_map = dict([[a["pid"] + "==" + a["qid"], a["scores"]] for a in output])

    assert len(output_map) == len(output), "You probably have redundancies in your keys"

    [P1, R1, F1m] = measures.per_question_metrics(input["data"], output_map)
    print("Per question measures (i.e. precision-recall per question, then average) ")
    print("\tP: " + str(P1) + " - R: " + str(R1) + " - F1m: " + str(F1m))

    EM0 = measures.exact_match_metrics(input["data"], output_map, 0)
    EM1 = measures.exact_match_metrics(input["data"], output_map, 1)
    print("\tEM0: " + str(EM0))
    print("\tEM1: " + str(EM1))

    [P2, R2, F1a] = measures.per_dataset_metric(input["data"], output_map)

    print("Dataset-wide measures (i.e. precision-recall across all the candidate-answers in the dataset) ")
    print("\tP: " + str(P2) + " - R: " + str(R2) + " - F1a: " + str(F1a))

if __name__ == "__main__":
    main()
