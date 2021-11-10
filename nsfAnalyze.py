import pickle
import random
from math import log as log
from math import sqrt as sqrt
from math import pow as pow
import matplotlib.pyplot as plt
from nltk.stem import PorterStemmer

wordEmbeddingVectors = dict()
emFile = open('embeddings/crawl-300d-2M.vec', 'r', encoding="utf8")
print(emFile.readline())
for i in range(1999995):
    line = emFile.readline().split()
    word = line[0]
    vec = [float(line[i]) for i in range(1,301)]
    wordEmbeddingVectors[word] = vec

print("Done Loading Embeddings!")

f = open("stop_words_english.txt","r", encoding="utf8")
stopWords = [line.strip() for line in f]

ps = PorterStemmer()

cosDistByDivTFIDF = dict()
cosDistByDiv = dict()
totalTermsByDiv = dict()
meanTermFreqByDiv = dict()
termFreqSTDByDiv = dict()
termCountsTYD = dict()
totalAwardsbyDiv = dict()
totalFundingbyDiv = dict()
totalWordsbyDiv = dict()
cosDistByDivEm = dict()
cosDistByDivEmTFIDF = dict()
deiAwardsByDiv = dict()
deiFundingByDiv = dict()
cosDistSampledByDiv = dict()
cosDistEmSampledByDiv = dict()
sampledAwardsByDiv = dict()
looseDEIAwardsByDiv = dict()
looseDEIFundingByDiv = dict()

def processWord(w):
    w = w.lower()
    w.replace('-','')
    w.replace('/','')
    if not w.isalpha():
        return None
    return w

searchStem = {
    "Equity" : ["equity","equitable"],
    "Diversity" : ["diversity", "diversify", "diversification"],
    "Inclusion" : ["inclusion","inclusive","inclusivity"],
    "Gender" : ["gender","genders","gendered"],
    "Intersectional" : ["intersectional", "intersectionality"],
    "Women" : ["women", "woman"],
    "Disparity" : ["disparities", "disparity"],
    "Marginalize" : ["marginalize", "marginalization", "marginalized"],
    "Underrepresented" : ["underrepresented", "underrepresentation"],
    "Latinx" : ["latinx"]
}    

abbrToName = {"BIO" : "Biological Sciences",
"CSE" : "Computer & Information Science & Engineering",
"EHR" : "Education & Human Resources",
"ENG" : "Engineering",
"GEO" : "Geosciences",
"MPS" : "Mathematical & Physical Sciences",
"SBE" : "Social, Behavioral & Economic Sciences",
"BFA" : "Budget, Finance, and Award Management"}

for y in range(1990,2021):
    for d in ["BIO","CSE","ENG","GEO","MPS","SBE","EHR"]:
        file = open("pickled-data/" + str(d) + "-" + str(y) + ".dat", "rb")
        thedata = pickle.load(file)
        newdata = dict()
        for i in thedata:
            if len(thedata[i]['words']) > 0:
                newdata[i] = thedata[i]
        thedata = newdata
        totalWordCount = dict()
        awardsPerWord = dict()
        wordsByAward = dict()
        rawWordsByAward = dict()
        totalWordCountEM = dict()
        awardsPerWordEM = dict()
        wordsByAwardEM = dict()
        sampledWordsByAward = dict()
        sampledWordsEmByAward = dict()
        totalWordCountSampled = dict()
        totalWordCountSampledEM = dict()
        totalAwards = len(thedata)
        if d not in totalAwardsbyDiv:
            totalAwardsbyDiv[d] = [totalAwards]
        else:
            totalAwardsbyDiv[d] += [totalAwards]
        totalFunding = 0.0
        deiFunding = 0.0
        deiCount = 0
        sampledAwards = 0
        looseDEICount = 0
        looseDEIFunding = 0.0
        for i in thedata:
            totalFunding += thedata[i]['amount']
            sampledWordCount = dict()
            sampledWordCountEM = dict()
            rawWordCount = dict()
            wordCount = dict()
            wordCountEM = dict()
            theWords = []
            theWordsEM = []
            for w in thedata[i]['words']:
                if w not in stopWords:
                    if w in wordEmbeddingVectors:
                        theWordsEM += [w]
                        if w not in wordCountEM:
                            wordCountEM[w] = 1
                        else:
                            wordCountEM[w] += 1
                    w = processWord(w)
                    if w != None:
                        if w not in rawWordCount:
                            rawWordCount[w] = 1
                        else:
                            rawWordCount[w] += 1
                        w = ps.stem(w)
                        theWords += [w]
                        if w not in wordCount:
                            wordCount[w] = 1
                        else:
                            wordCount[w] += 1
            for w in thedata[i]['titlewords']:
                if w not in stopWords:
                    if w in wordEmbeddingVectors:
                        theWordsEM += [w]
                        if w not in wordCountEM:
                            wordCountEM[w] = 1
                        else:
                            wordCountEM[w] += 1
                    w = processWord(w)
                    if w != None:
                        if w not in rawWordCount:
                            rawWordCount[w] = 1
                        else:
                            rawWordCount[w] += 1
                        w = ps.stem(w)
                        theWords += [w]
                        if w not in wordCount:
                            wordCount[w] = 1
                        else:
                            wordCount[w] += 1
            for w in wordCount:
                if w not in totalWordCount:
                    totalWordCount[w] = wordCount[w]
                else:
                    totalWordCount[w] += wordCount[w]
                if w not in awardsPerWord:
                    awardsPerWord[w] = 1
                else:
                    awardsPerWord[w] += 1
            for w in wordCountEM:
                if w not in totalWordCountEM:
                    totalWordCountEM[w] = wordCountEM[w]
                else:
                    totalWordCountEM[w] += wordCountEM[w]
                if w not in awardsPerWordEM:
                    awardsPerWordEM[w] = 1
                else:
                    awardsPerWordEM[w] += 1
            wordsByAwardEM[i] = wordCountEM
            wordsByAward[i] = wordCount
            rawWordsByAward[i] = rawWordCount
            if len(theWords) > 100:
                sampledAwards += 1
                theWords = random.sample(theWords,100)
                for w in theWords:
                    if w not in sampledWordCount:
                        sampledWordCount[w] = 1
                    else:
                        sampledWordCount[w] += 1
                    if w not in totalWordCountSampled:
                        totalWordCountSampled[w] = 1
                    else:
                        totalWordCountSampled[w] += 1
                sampledWordsByAward[i] = sampledWordCount
            if len(theWordsEM) > 100:
                theWordsEM = random.sample(theWordsEM,100)
                for w in theWordsEM:
                    if w not in sampledWordCountEM:
                        sampledWordCountEM[w] = 1
                    else:
                        sampledWordCountEM[w] += 1
                    if w not in totalWordCountSampledEM:
                        totalWordCountSampledEM[w] = 1
                    else:
                        totalWordCountSampledEM[w] += 1
                sampledWordsEmByAward[i] = sampledWordCountEM






        wordWeights = dict()
        wordWeightsEM = dict()
        for w in awardsPerWord:
            wordWeights[w] = log(float(totalAwards/awardsPerWord[w]),10)
        for w in awardsPerWordEM:
            wordWeightsEM[w] = log(float(totalAwards/awardsPerWordEM[w]),10)
        totalSemanticVec = [0.0 for _ in range(300)]
        totalSemanticVecTDIDF = [0.0 for _ in range(300)]
        for w in totalWordCountEM:
            v = wordEmbeddingVectors[w]
            m = totalWordCountEM[w]
            f = wordWeightsEM[w]
            for i in range(300):
                totalSemanticVec[i] += v[i] * m
                totalSemanticVecTDIDF[i] += v[i] * m * f
        sumTF = 0.0
        sum = 0.0
        for i in range(300):
            sum += pow(totalSemanticVec[i],2)
            sumTF += pow(totalSemanticVecTDIDF[i],2)
        sum = sqrt(sum)
        sumTF = sqrt(sumTF)
        for i in range(300):
            totalSemanticVec[i] = totalSemanticVec[i] / sum
            totalSemanticVecTDIDF[i] = totalSemanticVecTDIDF[i] / sumTF

        normedWordCountTFIDF = dict()
        normedWordCount = dict()
        sumTF = 0.0
        sum = 0.0
        for w in totalWordCount:
            adjusted = totalWordCount[w] * wordWeights[w]
            normedWordCountTFIDF[w] = adjusted
            sumTF += adjusted * adjusted
            sum += pow(totalWordCount[w], 2)
        sum = sqrt(sum)
        sumTF = sqrt(sumTF)
        for w in totalWordCount:
            normedWordCount[w] = totalWordCount[w] / sum
        for w in normedWordCountTFIDF:
            normedWordCountTFIDF[w] = normedWordCountTFIDF[w] / sumTF
        totalCosDistTFIDF = 0.0
        totalCosDist = 0.0
        totalCosDistEm = 0.0
        totalCosDistEmTFIDF = 0.0
        for t in searchStem:
            if t not in termCountsTYD:
                termCountsTYD[t] = dict()
            if y not in termCountsTYD[t]:
                termCountsTYD[t][y] = dict()
            termCountsTYD[t][y][d] = 0
        for i in thedata:
            deiScore = 0.0
            looseDEIscore = 0
            wordCount = wordsByAward[i]
            wordCountEM = wordsByAwardEM[i]
            rawWordCount = rawWordsByAward[i]
            awardSumTF = 0.0
            awardSum = 0.0
            wordCountTF = dict()
            for w in wordCount:
                adjusted = wordCount[w] * wordWeights[w]
                wordCountTF[w] = adjusted
                awardSumTF += adjusted * adjusted
                awardSum += pow(wordCount[w],2)
            awardSumTF = sqrt(awardSumTF)
            awardSum = sqrt(awardSum)
            dotProd = 0.0
            for w in wordCountTF:
                dotProd += (wordCountTF[w] * normedWordCountTFIDF[w]) / awardSumTF
            totalCosDistTFIDF += 1 - dotProd
            dotProd = 0.0
            for w in wordCount:
                dotProd += (wordCount[w] * normedWordCount[w]) / awardSum
            totalCosDist += 1 - dotProd
            embeddingVec = [0.0 for _ in range(300)]
            embeddingVecTF = [0.0 for _ in range(300)]
            for w in wordCountEM:
                v = wordEmbeddingVectors[w]
                m = wordCountEM[w]
                f = wordWeightsEM[w]
                for j in range(300):
                    embeddingVec[j] += v[j] * m
                    embeddingVecTF[j] += v[j] * m * f
            sumEM = 0.0
            sumEMTF = 0.0
            for j in range(300):
                sumEM += pow(embeddingVec[j],2)
                sumEMTF += pow(embeddingVecTF[j],2)
            sumEM = sqrt(sumEM)
            sumEMTF = sqrt(sumEMTF)
            for j in range(300):
                embeddingVec[j] = (embeddingVec[j] / sumEM) if sumEM != 0.0 else 0.0
                embeddingVecTF[j] = (embeddingVecTF[j] / sumEMTF) if sumEMTF != 0.0 else 0.0
            dotEM = 0.0
            dotEMTF = 0.0
            for j in range(300):
                dotEM += embeddingVec[j] * totalSemanticVec[j]
                dotEMTF += embeddingVecTF[j] * totalSemanticVecTDIDF[j]
            totalCosDistEm += 1 - dotEM                
            totalCosDistEmTFIDF += 1 - dotEMTF

            for t in searchStem:
                for w in searchStem[t]:
                    if w in rawWordCount:
                        termCountsTYD[t][y][d] += 1
                        if t == "Diversity" or t == "Equity" or t == "Inclusion":
                            deiScore += 1
                            if deiScore == 2:
                                deiCount += 1
                                deiFunding += thedata[i]['amount']
                        if t == "Diversity" or t == "Equity" or t == "Inclusion" or t == "Gender" or t == "Underrepresented" or t == "Disparity" or t == "Marginalize":
                            looseDEIscore += 1
                            if looseDEIscore == 1:
                                looseDEICount += 1
                                looseDEIFunding += thedata[i]['amount']
                        break
        freqSum = 0.0
        totalWords = 0.0
        for w in totalWordCount:
            totalWords += totalWordCount[w]
        for w in totalWordCount:
            freqSum += totalWordCount[w] / totalWords
        meanFreq = freqSum / len(totalWordCount)
        if d not in meanTermFreqByDiv:    
            meanTermFreqByDiv[d] = [meanFreq]
        else:
            meanTermFreqByDiv[d] += [meanFreq]
        varianceSum = 0.0
        for w in totalWordCount:
            varianceSum += pow((totalWordCount[w] / totalWords) - meanFreq, 2)
        stdFreq = sqrt(varianceSum / len(totalWordCount))

        #Sampled Words
        # Normalize totalWordCountsSampled and build and normalize totalSemanticVecSampled
        tot = 0.0
        for w in totalWordCountSampled:
            tot += pow(totalWordCountSampled[w], 2)
        tot = sqrt(tot)
        for w in totalWordCountSampled:
            totalWordCountSampled[w] = totalWordCountSampled[w] / tot

        totalSemanticVecSampled = [0.0 for _ in range(300)]
        for w in totalWordCountSampledEM:
            res = wordEmbeddingVectors[w]
            n = totalWordCountSampledEM[w]
            for i in range(300):
                totalSemanticVecSampled[i] += n * res[i]
        sum = 0.0
        for i in range(300):
            sum += pow(totalSemanticVecSampled[i],2)
        sum = sqrt(sum)
        for i in range(300):
            totalSemanticVecSampled[i] = totalSemanticVecSampled[i] / sum

        totalCosDistSampled = 0.0
        totalCosDistEmSample = 0.0

        for i in sampledWordsByAward:
            sum = 0.0
            for w in sampledWordsByAward[i]:
                sum += pow(sampledWordsByAward[i][w],2)
            sum = sqrt(sum)
            dotProd = 0.0
            for w in sampledWordsByAward[i]:
                dotProd += sampledWordsByAward[i][w] * totalWordCountSampled[w]
            dotProd = dotProd / sum
            totalCosDistSampled += 1 - dotProd

        for i in sampledWordsEmByAward:
            awardSemanticVec = [0.0 for _ in range (300)]
            for w in sampledWordsEmByAward[i]:
                res = wordEmbeddingVectors[w]
                n = sampledWordsEmByAward[i][w]
                for j in range(300):
                    awardSemanticVec[j] += res[j] * n
            
            sum = 0.0
            for j in range(300):
                sum += pow(awardSemanticVec[j], 2)
            sum = sqrt(sum)

            dotProd = 0.0
            for j in range(300):
                dotProd += awardSemanticVec[j] * totalSemanticVecSampled[j]
            dotProd = dotProd / sum
            totalCosDistEmSample += 1 - dotProd

        totalCosDistEmSample = totalCosDistEmSample / len(sampledWordsEmByAward)
        totalCosDistSampled = totalCosDistSampled / len(sampledWordsByAward)


        if d not in cosDistSampledByDiv:
            cosDistSampledByDiv[d] = [totalCosDistSampled]
        else:
            cosDistSampledByDiv[d] += [totalCosDistSampled]

        if d not in cosDistEmSampledByDiv:
            cosDistEmSampledByDiv[d] = [totalCosDistEmSample]
        else:
            cosDistEmSampledByDiv[d] += [totalCosDistEmSample]


        if d not in termFreqSTDByDiv:
            termFreqSTDByDiv[d] = [stdFreq]
        else:
            termFreqSTDByDiv[d] += [stdFreq]
        if d not in totalFundingbyDiv:
            totalFundingbyDiv[d] = [totalFunding]
        else:
            totalFundingbyDiv[d] += [totalFunding]
        if d not in totalWordsbyDiv:
            totalWordsbyDiv[d] = [totalWords]
        else:
            totalWordsbyDiv[d] += [totalWords]

        print(str(d) + " : " + str(y) + ", ACD (TF-IDF): " 
        + str(totalCosDistTFIDF / totalAwards) + ", ACD: " + str(totalCosDist / totalAwards))
        if d not in cosDistByDivTFIDF:
            cosDistByDivTFIDF[d] = [totalCosDistTFIDF / totalAwards]
        else:
            cosDistByDivTFIDF[d] += [totalCosDistTFIDF / totalAwards]
        if d not in cosDistByDiv:
            cosDistByDiv[d] = [totalCosDist / totalAwards]
        else:
            cosDistByDiv[d] += [totalCosDist / totalAwards]
        for t in searchStem:
            termCountsTYD[t][y][d] = termCountsTYD[t][y][d] / len(thedata)
        if d not in totalTermsByDiv:
            totalTermsByDiv[d] = [len(totalWordCount)]
        else:
            totalTermsByDiv[d] += [len(totalWordCount)]
        if d not in cosDistByDivEm:
            cosDistByDivEm[d] = [totalCosDistEm / totalAwards]
        else:
            cosDistByDivEm[d] += [totalCosDistEm / totalAwards]
        if d not in cosDistByDivEmTFIDF:
            cosDistByDivEmTFIDF[d] = [totalCosDistEmTFIDF / totalAwards]
        else:
            cosDistByDivEmTFIDF[d] += [totalCosDistEmTFIDF / totalAwards]
        if d not in deiAwardsByDiv:
            deiAwardsByDiv[d] = [deiCount]
        else:
            deiAwardsByDiv[d] += [deiCount]
        if d not in deiFundingByDiv:
            deiFundingByDiv[d] = [deiFunding]
        else:
            deiFundingByDiv[d] += [deiFunding]

        if d not in looseDEIAwardsByDiv:
            looseDEIAwardsByDiv[d] = [looseDEICount]
        else:
            looseDEIAwardsByDiv[d] += [looseDEICount]

        if d not in looseDEIFundingByDiv:
            looseDEIFundingByDiv[d] = [looseDEIFunding]
        else:
            looseDEIFundingByDiv[d] += [looseDEIFunding]

        if d not in sampledAwardsByDiv:
            sampledAwardsByDiv[d] = [sampledAwards]
        else:
            sampledAwardsByDiv[d] += [sampledAwards]

        file.close()

pickleData = dict()

pickleData['cosDistByDivTFIDF'] = cosDistByDivTFIDF
pickleData['cosDistByDiv'] = cosDistByDiv
pickleData['totalTermsByDiv'] = totalTermsByDiv
pickleData['meanTermFreqByDiv'] = meanTermFreqByDiv
pickleData['termFreqSTDByDiv'] = termFreqSTDByDiv
pickleData['termCountsTYD'] = termCountsTYD
pickleData['totalAwardsbyDiv'] = totalAwardsbyDiv
pickleData['totalFundingbyDiv'] = totalFundingbyDiv
pickleData['totalWordsbyDiv'] = totalWordsbyDiv
pickleData['cosDistByDivEm'] = cosDistByDivEm
pickleData['cosDistByDivEmTFIDF'] = cosDistByDivEmTFIDF
pickleData['searchStem'] = searchStem
pickleData['deiFundingByDiv'] = deiFundingByDiv
pickleData['deiAwardsByDiv'] = deiAwardsByDiv
pickleData['cosDistSampledByDiv'] = cosDistSampledByDiv
pickleData['cosDistEmSampledByDiv'] = cosDistEmSampledByDiv
pickleData['sampledAwardsByDiv'] = sampledAwardsByDiv
pickleData['looseDEIAwardsByDiv'] = looseDEIAwardsByDiv
pickleData['looseDEIFundingByDiv'] = looseDEIFundingByDiv

file = open('processed-data-2.dat','wb')
pickle.dump(pickleData, file)
file.close()
