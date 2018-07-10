import json

# this is the location of your data; has to be downloaded from http://cogcomp.org/multirc/
inputFile = '/Users/daniel/ideaProjects/hard-qa/split/dev_83.json'


def main():
    eval('baseline-scores/human-01.json')


def avg(l):
    return reduce(lambda x, y: x + y, l) / len(l)


def eval(outFile):
    input = json.load(open(inputFile))
    output = json.load(open(outFile))
    outputMap = dict([[a["pid"] + "==" + a["qid"], a["scores"]] for a in output])

    assert len(outputMap) == len(output), "You probably have redundancies in your keys"

    P1 = []
    R1 = []

    for p in input["data"]:
        for qIdx, q in enumerate(p["paragraph"]["questions"]):
            id = p["id"] + "==" + str(qIdx)
            if (id in outputMap):
                predictedAns = outputMap.get(id)
                correctAns = [int(a["isAnswer"]) for a in q["answers"]]
                predictCount = sum(predictedAns)
                correctCount = sum(correctAns)
                agreementCount = sum([a * b for (a, b) in zip(correctAns, predictedAns)])
                p1 = (1.0 * agreementCount / predictCount) if predictCount > 0.0 else 1.0
                r1 = (1.0 * agreementCount / correctCount) if correctCount > 0.0 else 1.0
                P1.append(p1)
                R1.append(r1)
            else:
                print("The id " + id + " not found . . . ")

    print("Per question measures (i.e. precision-recall per question, then average) ")
    print("\tP: " + str(avg(P1)) + " - R: " + str(avg(R1)) + " - F1m: " + str(2 * avg(R1) * avg(P1) / (avg(P1) + avg(R1))))

    agreementCount = 0
    correctCount = 0
    predictCount = 0
    for p in input["data"]:
        for qIdx, q in enumerate(p["paragraph"]["questions"]):
            id = p["id"] + "==" + str(qIdx)
            if (id in outputMap):
                predictedAns = outputMap.get(id)
                correctAns = [int(a["isAnswer"]) for a in q["answers"]]
                predictCount += sum(predictedAns)
                correctCount += sum(correctAns)
                agreementCount += sum([a * b for (a, b) in zip(correctAns, predictedAns)])
            else:
                print("The id " + id + " not found . . . ")

    p1 = (1.0 * agreementCount / predictCount) if predictCount > 0.0 else 1.0
    r1 = (1.0 * agreementCount / correctCount) if correctCount > 0.0 else 1.0

    print("Dataset-wide measures (i.e. precision-recall across all the candidate-answers in the dataset) ")
    print("\tP: " + p1) + " - R: " + str(r1) + " - F1a: " + str(2 * r1 * p1 / (p1 + r1))


if __name__ == "__main__":
    main()
