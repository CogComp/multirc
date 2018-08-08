import json
import numpy
import matplotlib.pyplot as plt

# this is the location of your data; has to be downloaded from http://cogcomp.org/multirc/
inputFile = '/Users/daniel/ideaProjects/hard-qa/split/dev_83.json'


def main():
    myPlot("Human", '-r', 1.5, 'baseline-scores/human.json')
    myPlot("IR(Paragraphs)", '-.g', 1.5, 'baseline-scores/lucene_paragraphs.json')
    myPlot("IR(World)", '*-b', 1.5, 'baseline-scores/lucene_world.json')
    myPlot("SimpleLR", '^--c', 1.5, 'baseline-scores/simpleLR.json')
    plt.xlabel('Recall', fontsize=11)
    plt.ylabel('Precision', fontsize=11)
    plt.legend(loc="lower left", fontsize=9)
    plt.ylim((0.0, 1.0))
    plt.xlim((0.0, 1.0))
    plt.show()


def avg(l):
    return reduce(lambda x, y: x + y, l) / len(l)


def myPlot(plotname, options, lw, outFile):
    print("PlotName: " + plotname)
    input = json.load(open(inputFile))
    output = json.load(open(outFile))
    outputMap = dict([[a["pid"] + "==" + a["qid"], a["scores"]] for a in output])

    minVal = min([min(a["scores"]) for a in output])
    maxVal = max([max(a["scores"]) for a in output])
    num = 10.0  # number of points to measure

    P1 = []
    R1 = []
    for thr in numpy.arange(minVal - 0.1, maxVal + 0.1, (maxVal - minVal) / num):
        R1Tmp = []
        P1Tmp = []
        for p in input["data"]:
            for qIdx, q in enumerate(p["paragraph"]["questions"]):
                id = p["id"] + "==" + str(qIdx)
                if (id in outputMap):
                    predictedAns = [a > thr for a in outputMap.get(id)]
                    correctAns = [int(a["isAnswer"]) for a in q["answers"]]
                    predictCount = sum(predictedAns)
                    correctCount = sum(correctAns)
                    agreementCount = sum([a * b for (a, b) in zip(correctAns, predictedAns)])
                    p1 = (1.0 * agreementCount / correctCount) if correctCount > 0.0 else 1.0
                    r1 = (1.0 * agreementCount / predictCount) if predictCount > 0.0 else 1.0
                    P1Tmp.append(p1)
                    R1Tmp.append(r1)
                else:
                    print("The id " + id + " not found . . . ")
        P1.append(avg(P1Tmp))
        R1.append(avg(R1Tmp))
    plt.plot(P1, R1, options, linewidth=lw, label=plotname)


if __name__ == "__main__":
    main()
