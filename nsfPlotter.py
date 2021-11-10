import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl
from math import pow as pow
from matplotlib import gridspec

file = open('processed-data-2.dat','rb')
pickleData = pickle.load(file)
file.close()

searchStem = pickleData['searchStem']

abbrToName = {"BIO" : "Biological Sciences",
"CSE" : "Computer & Information Science & Engineering",
"EHR" : "Education & Human Resources",
"ENG" : "Engineering",
"GEO" : "Geosciences",
"MPS" : "Mathematical & Physical Sciences",
"SBE" : "Social, Behavioral & Economic Sciences",
"BFA" : "Budget, Finance, and Award Management"}

cosDistByDivTFIDF = pickleData['cosDistByDivTFIDF']
cosDistByDiv = pickleData['cosDistByDiv']
totalTermsByDiv = pickleData['totalTermsByDiv']
meanTermFreqByDiv = pickleData['meanTermFreqByDiv']
termFreqSTDByDiv = pickleData['termFreqSTDByDiv']
termCountsTYD = pickleData['termCountsTYD']
totalAwardsbyDiv = pickleData['totalAwardsbyDiv']
totalFundingbyDiv = pickleData['totalFundingbyDiv']
totalWordsbyDiv = pickleData['totalWordsbyDiv']
cosDistByDivEm = pickleData['cosDistByDivEm']
cosDistByDivEmTFIDF = pickleData['cosDistByDivEmTFIDF']
deiFundingByDiv = pickleData['deiFundingByDiv']
deiAwardsByDiv = pickleData['deiAwardsByDiv']
cosDistSampledByDiv = pickleData['cosDistSampledByDiv']
cosDistEmSampledByDiv = pickleData['cosDistEmSampledByDiv']

sampledAwardsByDiv = pickleData['sampledAwardsByDiv'] 
looseDEIAwardsByDiv = pickleData['looseDEIAwardsByDiv']
looseDEIFundingByDiv = pickleData['looseDEIFundingByDiv']

with plt.style.context("bmh"):

    fig = plt.figure()
    fig.set_figheight(5)
    fig.set_figwidth(8)
    fig.suptitle("Percentage of NSF Award Abstracts Containing Given Terms by Year")
    spec = gridspec.GridSpec(ncols = 5, nrows = 2, hspace = 0.3, top = 0.85, wspace = 0.4)
    n = 0
    for t in searchStem:
        totals = [0 for _ in range(1990, 2021)]
        for i in range(31):
            totalAwards = 0.0
            totalWords = 0.0
            for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
                totalAwards += totalAwardsbyDiv[d][i]
                totalWords += termCountsTYD[t][(1990 + i)][d] * totalAwardsbyDiv[d][i]
            totals[i] = (totalWords / totalAwards) * 100.0
        xs = range(1990, 2021)
        ys = totals
        ax = fig.add_subplot(spec[n])
        ax.plot(xs,ys)
        ax.set_title(t, fontsize = 8)
        n += 1

    plt.figure(2, figsize = (8,6))
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        xs = range(1990, 2021)
        ys = [((looseDEIAwardsByDiv[d][i] / totalAwardsbyDiv[d][i]) * 100) for i in range(31)]
        plt.plot(xs,ys, label=abbrToName[d])

    plt.suptitle("Percentage of National Science Foundation Awards Containing at Least\n One of Following Terms per Division by Year")
    plt.title("(Equity, Diversity, Inclusion, Gender, Marginalize, Underrepresented, Disparity)", fontsize=10)
    plt.xlabel("Year")
    plt.ylabel("Percentage")
    plt.legend(loc = "upper left", fontsize = 7)
    plt.show()

    totals = [0 for _ in range(1990, 2021)]
    for i in range(31):
        totalAwards = 0.0
        totalDEI = 0.0
        for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
            totalAwards += totalAwardsbyDiv[d][i]
            totalDEI += looseDEIAwardsByDiv[d][i]
        totals[i] = (totalDEI / totalAwards) * 100

    plt.figure(3, figsize = (8,6))
    xs = range(1990, 2021)
    ys = totals
    plt.plot(xs, ys, label="All Directorates")
    plt.suptitle("Percentage of National Science Foundation Awards Containing at Least\n One of Following Terms for all Division by Year")
    plt.title("(Equity, Diversity, Inclusion, Gender, Marginalize, Underrepresented, Disparity)", fontsize=10)
    plt.xlabel("Year")
    plt.ylabel("Percentage")
    plt.legend(loc = "upper left", fontsize = 10)
    plt.show()

    plt.figure(2, figsize = (8,6))
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        xs = range(1990, 2021)
        ys = [(looseDEIFundingByDiv[d][i] / pow(10,6)) for i in range(31)]
        plt.plot(xs,ys, label=abbrToName[d])

    plt.suptitle("Total Funding of National Science Foundation Awards Containing at Least\n One of Following Terms per Division by Year")
    plt.title("(Equity, Diversity, Inclusion, Gender, Marginalize, Underrepresented, Disparity)", fontsize=10)
    plt.xlabel("Year")
    plt.ylabel("Millions of Dollars (USD)")
    plt.legend(loc = "upper left", fontsize = 7)
    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))
    plt.show()

    totals = [0 for _ in range(1990, 2021)]
    for i in range(31):
        totalAwards = 0.0
        totalDEI = 0.0
        totals[i] = 0.0
        for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
            totals[i] += (looseDEIFundingByDiv[d][i] / pow(10,6))

    plt.figure(3, figsize = (8,6))
    xs = range(1990, 2021)
    ys = totals
    plt.plot(xs, ys, label="All Directorates")
    plt.suptitle("Total Funding of National Science Foundation Awards Containing at Least\n One of Following Terms for all Division by Year")
    plt.title("(Equity, Diversity, Inclusion, Gender, Marginalize, Underrepresented, Disparity)", fontsize=10)
    plt.xlabel("Year")
    plt.ylabel("Millions of Dollars (USD)")
    plt.legend(loc = "upper left", fontsize = 10)
    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))
    plt.show()


    plt.figure(10, figsize = (8,6))
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        xs = range(1990, 2021)
        ys = cosDistSampledByDiv[d]
        plt.plot(xs,ys, label=abbrToName[d])

    plt.ylim(0.4,0.8)
    plt.suptitle("Average National Science Foundation Award Abstract Uniqueness Measured by \n Cosine Distance of Word Frequency from Mean Word Frequency.")
    plt.title("For Each Division by Year", fontsize=10)
    plt.xlabel("Year")
    plt.ylabel("Average Cosine Distance")
    plt.legend(loc = "upper right", fontsize = 7)
    plt.show()

    totals = [0 for _ in range(1990, 2021)]
    for i in range(31):
        totalAwards = 0.0
        totalCosDist = 0.0
        for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
            totalAwards += totalAwardsbyDiv[d][i]
            totalCosDist += cosDistSampledByDiv[d][i] * totalAwardsbyDiv[d][i]
            totals[i] = (totalCosDist / totalAwards)

    
    plt.figure(3, figsize = (8,6))
    xs = range(1990, 2021)
    ys = totals
    plt.ylim(0.4,0.8)
    plt.plot(xs, ys, label="All Directorates")
    plt.suptitle("Average National Science Foundation Award Abstract Uniqueness Measured by \n Cosine Distance of Word Frequency from Mean Word Frequency.")
    plt.title("For All Divisions by Year", fontsize=10)
    plt.xlabel("Year")
    plt.ylabel("Average")
    plt.legend(loc = "upper right", fontsize = 10)
    plt.show()

    plt.figure(10, figsize = (8,6))
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        xs = range(1990, 2021)
        ys = cosDistEmSampledByDiv[d]
        plt.plot(xs,ys, label=abbrToName[d])

    plt.ylim(0.0,0.2)
    plt.suptitle("Average National Science Foundation Award Abstract Uniqueness Measured by \n Cosine Distance of Aggregate Word Embedding from Mean.")
    plt.title("For Each Division by Year", fontsize=10)
    plt.xlabel("Year")
    plt.ylabel("Average Cosine Distance")
    plt.legend(loc = "upper right", fontsize = 7)
    plt.show()

    totals = [0 for _ in range(1990, 2021)]
    for i in range(31):
        totalAwards = 0.0
        totalCosDist = 0.0
        for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
            totalAwards += totalAwardsbyDiv[d][i]
            totalCosDist += cosDistEmSampledByDiv[d][i] * totalAwardsbyDiv[d][i]
            totals[i] = (totalCosDist / totalAwards)

    
    plt.figure(3, figsize = (8,6))
    xs = range(1990, 2021)
    ys = totals
    plt.ylim(0.0,0.2)
    plt.plot(xs, ys, label="All Directorates")
    plt.suptitle("Average National Science Foundation Award Abstract Uniqueness Measured by \n Cosine Distance of Aggregate Word Embedding from Mean.")
    plt.title("For All Divisions by Year", fontsize=10)
    plt.xlabel("Year")
    plt.ylabel("Average Cosine Distance")
    plt.legend(loc = "upper right", fontsize = 10)
    plt.show()

    plt.figure(1, figsize = (8,6))
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        xs = range(1990, 2021)
        ys = sampledAwardsByDiv[d]
        plt.plot(xs,ys, label=abbrToName[d])

    plt.title("Awards Abstracts with 100 or More Words per Year by Division")
    plt.xlabel("Year")
    plt.ylabel("Awards")
    plt.legend(loc = "upper left", fontsize = 7)
    plt.show()


    plt.figure(1, figsize = (8,6))
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        xs = range(1990, 2021)
        ys = cosDistByDivTFIDF[d]
        plt.plot(xs,ys, label=abbrToName[d])

    plt.title("Average Cosine Difference per Year by Division (TF-IDF)")
    plt.xlabel("Year")
    plt.ylabel("Average Cosine Distance")
    plt.legend(loc = "upper right", fontsize = 7)
    plt.show()

    plt.figure(2, figsize = (8,6))
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        xs = range(1990, 2021)
        ys = [((deiAwardsByDiv[d][i] / totalAwardsbyDiv[d][i]) * 100) for i in range(31)]
        plt.plot(xs,ys, label=abbrToName[d])

    plt.title("Percentage of 'DEI' Awards per Division by Year")
    plt.xlabel("Year")
    plt.ylabel("Percentage")
    plt.legend(loc = "upper left", fontsize = 7)
    plt.show()

    totals = [0 for _ in range(1990, 2021)]
    for i in range(31):
        totalAwards = 0.0
        totalDEI = 0.0
        for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
            totalAwards += totalAwardsbyDiv[d][i]
            totalDEI += deiAwardsByDiv[d][i]
        totals[i] = (totalDEI / totalAwards) * 100

    plt.figure(3, figsize = (8,6))
    xs = range(1990, 2021)
    ys = totals
    plt.plot(xs, ys, label="All Directorates")
    plt.title("Percentage of 'DEI' Awards for All Division by Year")
    plt.xlabel("Year")
    plt.ylabel("Percentage")
    plt.legend(loc = "upper left", fontsize = 10)
    plt.show()

    plt.figure(2, figsize = (8,6))
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        xs = range(1990, 2021)
        ys = [(deiFundingByDiv[d][i] / pow(10,6)) for i in range(31)]
        plt.plot(xs,ys, label=abbrToName[d])

    plt.title("Total 'DEI' Funding per Division by Year")
    plt.xlabel("Year")
    plt.ylabel("Millions of Dollars (USD)")
    plt.legend(loc = "upper left", fontsize = 7)
    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))
    plt.show()

    totals = [0 for _ in range(1990, 2021)]
    for i in range(31):
        totalAwards = 0.0
        totalDEI = 0.0
        for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
            totalDEI += deiFundingByDiv[d][i] / pow(10,6)
            totals[i] = totalDEI

    plt.figure(3, figsize = (8,6))
    xs = range(1990, 2021)
    ys = totals
    plt.plot(xs, ys, label="All Directorates")
    plt.title("Total 'DEI' Funding for All Division by Year")
    plt.xlabel("Year")
    plt.ylabel("Millions of Dollars (USD)")
    plt.legend(loc = "upper left", fontsize = 10)
    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))
    plt.show()

    plt.figure(2, figsize = (8,6))
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        xs = range(1990, 2021)
        ys = cosDistByDiv[d]
        plt.plot(xs,ys, label=abbrToName[d])

    plt.ylim(0.4,0.8)
    plt.title("Average Cosine Difference per Year by Division")
    plt.xlabel("Year")
    plt.ylabel("Average Cosine Distance")
    plt.legend(loc = "upper right", fontsize = 7)
    plt.show()

    totals = [0 for _ in range(1990, 2021)]
    for i in range(31):
        totalAwards = 0.0
        totalCosDist = 0.0
        for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
            totalAwards += totalAwardsbyDiv[d][i]
            totalCosDist += cosDistByDiv[d][i] * totalAwardsbyDiv[d][i]
            totals[i] = (totalCosDist / totalAwards)

    plt.figure(3, figsize = (8,6))
    xs = range(1990, 2021)
    ys = totals
    plt.ylim(0.4,0.8)
    plt.plot(xs, ys, label="All Directorates")
    plt.title("Average Cosine Difference of all Divisions by Year")
    plt.xlabel("Year")
    plt.ylabel("Average Cosine Distance")
    plt.legend(loc = "upper right", fontsize = 10)
    plt.show()


    plt.figure(3, figsize = (8,6))
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        xs = range(1990, 2021)
        ys = totalTermsByDiv[d]
        plt.plot(xs,ys, label=abbrToName[d])

    plt.title("Total Number of Terms by Division by Year")
    plt.xlabel("Year")
    plt.ylabel("Number of Terms")
    plt.legend(loc = "upper left", fontsize = 7)
    plt.show()

    plt.figure(4, figsize = (8,6))
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        xs = range(1990, 2021)
        ys = meanTermFreqByDiv[d]
        plt.plot(xs,ys, label=abbrToName[d])

    plt.title("Mean Frequency of Terms by Division by Year")
    plt.xlabel("Year")
    plt.ylabel("Mean Term Frequency")
    plt.legend(loc = "upper right", fontsize = 7)
    plt.show()

    plt.figure(5, figsize = (8,6))
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        xs = range(1990, 2021)
        ys = termFreqSTDByDiv[d]
        plt.plot(xs,ys, label=abbrToName[d])

    plt.title("Term Frequency Standard Deviation by Divison by Year")
    plt.xlabel("Year")
    plt.ylabel("Term Frequency STD")
    plt.legend(loc = "upper right", fontsize = 7)
    plt.show()

    plt.figure(6, figsize = (8,6))
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        xs = range(1990, 2021)
        ys = totalAwardsbyDiv[d]
        plt.plot(xs,ys, label=abbrToName[d])

    plt.title("Total Awards by Division by Year")
    plt.xlabel("Year")
    plt.ylabel("Total Awards")
    plt.legend(loc = "upper left", fontsize = 7)
    plt.show()

    plt.figure(7, figsize = (8,6))
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        xs = range(1990, 2021)
        ys = [(i / pow(10,6)) for i in totalFundingbyDiv[d]]
        plt.plot(xs,ys, label=abbrToName[d])

    plt.title("Total Funding by Division by Year")
    plt.xlabel("Year")
    plt.ylabel("Millions of Dollars (USD)")
    plt.legend(loc = "upper left", fontsize = 7)
    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))
    plt.show()

    plt.figure(8, figsize = (8,6))
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        xs = range(1990, 2021)
        ys = totalWordsbyDiv[d]
        plt.plot(xs,ys, label=abbrToName[d])

    plt.title("Total Words by Division by Year")
    plt.xlabel("Year")
    plt.ylabel("Total Words")
    plt.legend(loc = "upper left", fontsize = 7)
    plt.show()

    plt.figure(8, figsize = (8,6))
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        xs = range(1990, 2021)
        ys = [totalWordsbyDiv[d][i] / totalAwardsbyDiv[d][i] for i in range(31)]
        plt.plot(xs,ys, label=abbrToName[d])

    plt.title("Average Words per Award by Division by Year")
    plt.xlabel("Year")
    plt.ylabel("Average Words")
    plt.legend(loc = "upper left", fontsize = 7)
    plt.show()


    plt.figure(9, figsize = (8,6))
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        xs = range(1990, 2021)
        ys = cosDistByDivEmTFIDF[d]
        plt.plot(xs,ys, label=abbrToName[d])

    plt.title("Average Cosine Difference Word Embeddings per Year by Division (TF-IDF)")
    plt.xlabel("Year")
    plt.ylabel("Average Cosine Distance")
    plt.legend(loc = "lower left", fontsize = 7)
    plt.show()

    plt.figure(10, figsize = (8,6))
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        xs = range(1990, 2021)
        ys = cosDistByDivEm[d]
        plt.plot(xs,ys, label=abbrToName[d])

    plt.ylim(0.0,0.2)
    plt.title("Word Embeddings Average Cosine Difference per Year by Division")
    plt.xlabel("Year")
    plt.ylabel("Average Cosine Distance")
    plt.legend(loc = "upper right", fontsize = 7)
    plt.show()

    totals = [0 for _ in range(1990, 2021)]
    for i in range(31):
        totalAwards = 0.0
        totalCosDist = 0.0
        for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
            totalAwards += totalAwardsbyDiv[d][i]
            totalCosDist += cosDistByDivEm[d][i] * totalAwardsbyDiv[d][i]
            totals[i] = (totalCosDist / totalAwards)

    
    plt.figure(3, figsize = (8,6))
    xs = range(1990, 2021)
    ys = totals
    plt.ylim(0.0,0.2)
    plt.plot(xs, ys, label="All Directorates")
    plt.title("Word Embeddings Average Cosine Difference of all Divisions by Year")
    plt.xlabel("Year")
    plt.ylabel("Average Cosine Distance")
    plt.legend(loc = "upper right", fontsize = 10)
    plt.show()


    fig = 11
    for t in searchStem:
        plt.figure(fig, figsize = (8,6))
        for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
            xs = range(1990, 2021)
            ys = [(termCountsTYD[t][y][d] * 100) for y in xs]
            plt.plot(xs,ys, label=abbrToName[d])

        plt.title("Percentage of Documents with '" + t + "' Terms per Year by Division", fontsize = 13)
        plt.xlabel("Year")
        plt.ylabel("Percentage")
        plt.legend(loc = "upper left", fontsize = 7)
        plt.show()

        totals = [0 for _ in range(1990, 2021)]
        for i in range(31):
            totalAwards = 0.0
            totalWords = 0.0
            for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
                totalAwards += totalAwardsbyDiv[d][i]
                totalWords += termCountsTYD[t][(1990 + i)][d] * totalAwardsbyDiv[d][i]
            totals[i] = (totalWords / totalAwards) * 100.0

        plt.figure(fig, figsize = (8,6))
        xs = range(1990, 2021)
        ys = totals
        plt.plot(xs, ys, label="All Directorates")
        plt.title("Percentage of Documents with '" + t + "' Terms in all Divisions by Year", fontsize = 13)
        plt.xlabel("Year")
        plt.ylabel("Percentage")
        plt.legend(loc = "upper left", fontsize = 10)
        plt.show()





