import numpy as np
import matplotlib.pyplot as plt

# evenly sampled time at 200ms intervals
# t = np.arange(0., 5., 0.2)

# red dashes, blue squares and green triangles
# plt.plot(t, t, 'r--', t, t**2, 'bs')
# plt.plot(t, t**3, 'g^', label="asdad")
# plt.legend()
# plt.show()

def myPlot(filename, plotname, options,lw):
    rows = []
    import csv
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(len(row))
            split = row[0].split(",")
            rows.append( [float(i) for i in split] )

    # print(str(rows))
    plt.plot(rows[1], rows[0], options, linewidth=lw, label=plotname)

myPlot('/Users/daniel/ideaProjects/hard-qa/files/everything/pr-human2-small.csv', "Human", 'ro',1.5)
myPlot('/Users/daniel/ideaProjects/hard-qa/files/everything/pr-bidaf-phrasesim.csv', "Bidaf", '-g',1.5)
myPlot('/Users/daniel/ideaProjects/hard-qa/files/everything/pr-SW-normalized.csv', "SW+D", '--b',1.5)
myPlot('/Users/daniel/ideaProjects/hard-qa/files/everything/pr-lucene-world.csv', "IR(web)", '*c',0.8)
myPlot('/Users/daniel/ideaProjects/hard-qa/files/everything/pr-lucene-multirc-sentences.csv', "IR(paragraphs)", ':m',2.5)
myPlot('/Users/daniel/ideaProjects/hard-qa/files/everything/pr-semanticilp.csv', "SemanticILP", '-.k',2.5)
plt.xlabel('Recall', fontsize=11)
plt.ylabel('Precision', fontsize=11)
plt.legend(loc="lower left",fontsize=9)
plt.show()




# import matplotlib.pyplot as plt
# from matplotlib.legend_handler import HandlerLine2D
#
# line1, = plt.plot([3,2,1], marker='o', label='Line 1')
# line2, = plt.plot([1,2,3], marker='o', label='Line 2')
#
# plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
#
#
# import matplotlib.pyplot as plt
# import numpy as np
#
# y = [2,4,6,8,10,12,14,16,18,20]
# y2 = [10,11,12,13,14,15,16,17,18,19]
# x = np.arange(10)
# fig = plt.figure()
# ax = plt.subplot(111)
# ax.plot(x, y, label='$y = numbers')
# ax.plot(x, y2, label='$y2 = other numbers')
# plt.title('Legend inside')
# ax.legend()
# plt.show()
