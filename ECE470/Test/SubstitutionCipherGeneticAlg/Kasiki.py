import time
import random
import re
cipherText = "DGTKEDTNAXFNSCOIZKPLTWPAMQUYICPSIZFNEJJENXFKWRZAHPEZKFATBQDFVADEUZECSZVTBMUKSZVTBQNYSZCASFIVCLWLMTPLXPOAHPXRWDEALFJEKCTGBFPWJMFTNTFCEHJELMOUXSPDIOUFVDFNAAVKLZWDIZIFPOZNWAMCECLLFFIVWPQOODNVRLYDNTFSSJLNXRFKGSEHYYBCSYRTIAXVPWOOCFUYIJLLFEIFYEPDUZEZJHPDIZUWMYOTBQNDECVSQQMCPJYCBFIVASZLYSBEKTHAMEDRVPONIIJKIWWYIGCLXESELQXRVYENISFKXTYGUIBPCZFKHAXKLPJGLUQGIOFSUXMRROXALOIVHFDRCSIKEWZNAEUIETRHNRPIXSPGLMWVCLCDQTJTLHLSUYJCILYDUTBCJOZWHFIVVTGELMOUXSPWBAMVXZHNUFPLVSPEFEGFVHPMUPFESTDEYZPLKSLNXUUNEDZNFKOZRPTNNTFVZPYIHSBJAPHEHFCPSFCHIGTVMHTSBQEZLLONNEFEXXLRSVBEIZFTIRUFAYMEWMVJIYZWCRJTSFWDNUQYICEHYIJEODSEXXJXLEZUNMOUWLGEGQBEHMWOQAOFYCOEUPCVEEDWYXMNIDHALYFUEWZNAPPNRESELUWVVCZAXVVJXNLRLKJEKZYLCWFNMWOCUFTRROEOGMLVMEXOLQTTECJTBQTBCHLSXMSBMYRUJMOUXSPLCSIKRTYGVQHZRYTNAFPNMYVAHPGCMEEELMOUXSPWCZEKSDSIPQSRQZYGMFUYIWPAPQTKLTDWUEUYIXZSNMXWYWERIGCCILYDGATKHLYGYDTFQPTEPQSNEDTNUZEZALDKCZEVVDEUHZFUIGPRSFIZRRHAMSPZRRDOXUGWICPNNRSFQHSANUIRHLWLIIFUJZCSNQBUSQMECZHWMIPDMAJTSFWDNMLVQJZWHFJDITQIQMOKIOEOUZEJIPLLFFIVJFYAHPIRZPXALKKRRPLTGKCRGVEOMMWVQPLNXEFKQPQRYQXYIYEHYOMFWPQINOPDISPRYIBJRZEHCZHZRESEQASCHMPTQUYKQPLNXEVUHPYDYMUYFFEJOEUKLPXTUFUFSXLREEJWXSPYXUEEXQTNXFIVQTNOOXEEXMPALFPKLTYKUNPLXTEAHPZVXDZMYTPNMNZUFPOKXSTNEMCFYEYONTJEKPWSYUUXSEOALWFIEYODUDLVVLYDCFXRWLMEUGUZJFWTCYFKSRTVYFIVGCZWXFIVWWTPVGUKLLEBCSILWVJHUPNVFJEHYISZWESIHQTRROLBIPZDMRSTUEXVPWERSFPXMGPGIXJRVESEMXJGLPORUSHVHXPRCSIKEWZNATFNEDDOYJDZXPOAHPJYEOEOLGOKSVPEJGQNLPYTBQZXSEEHYDFKLPJSQMSDIOTNNAUYIRCAPQZRVOLNXIBJLPOOPQSZXWTKYMOFZPCFFAXRROHHYZUYIJRONFPXVLGENTFP"

def sortValues(frequencies, letters):
    i=(len(frequencies)-1)
    while i>0:
        t=i
        while t>0:
            if frequencies[i]<frequencies[t-1]:
                temp = frequencies[t-1]
                tempLet = letters[t-1]
                frequencies[t-1]=frequencies[i]
                frequencies[i]=temp
                letters[t-1]=letters[i]
                letters[i]=tempLet
            t-=1
        i-=1
    return frequencies, letters
def findLetterA(letterE):
    alphabet="abcdefghijklmnopqrstuvwxyz"
    before, after = alphabet.split(letterE)
    newAlphabet = after+before+letterE
    return newAlphabet[len(newAlphabet)-5]
def getDigraphs(i):
	text = file("words.txt").read()
	text = text.split("\n")
	alphabet="abcdefghijklmnopqrstuvwxyz"
	counts=[]
	matches=[]
	for word in text:
	    t=0
	    for letter in word:
	        if letter.lower()==alphabet[i]:
	            if(t!=(len(word)-1)):
	                matches.append(word[t+1])
	        t+=1
	counts=[]
	for letter in alphabet:
		count = 0
		for x in matches:
			if letter==x:
				count+=1
		counts.append(count)
	return counts

def constructPossibleWord(startingLetter, possibleLetters):
    tempLetter=startingLetter
    alphabet="abcdefghijklmnopqrstuvwxyz"
    i=alphabet.find(startingLetter)
    newString = ""
    possibles=[]
    t=0
    newString = ""
    newString+=startingLetter
    while t<len(possibleLetters):
        #print newString
        startingLetter=getNextLetter(getNextLikelyLetter(newString),possibleLetters[t])
        newString+=startingLetter
        t+=1
    return newString
def getNextLetter(digraphs,letters):
##    print letters
##    print digraphs
    alphabet="abcdefghijklmnopqrstuvwxyz"
    biggestLetter=""
    biggestValue=0
    for letter in letters:
        i=alphabet.find(letter)
        if digraphs[i]>=biggestValue:
            biggestValue=digraphs[i]
            biggestLetter=letter
    return biggestLetter
def getNextLikelyLetter(previous):
    text = file("words.txt").read()
    re1="\s("+previous+")(\w)"
    rg = re.compile(re1,re.IGNORECASE|re.DOTALL)
    m = re.findall(re1,text)
    matches=[]
    if m:
        for match in m:
            matches.append(match[1])
    alphabet="abcdefghijklmnopqrstuvwxyz"
    counts=[]
    for letter in alphabet:
            count = 0
            for x in matches:
                    if letter==x:
                            count+=1
            counts.append(count)
    return counts
def solveMonoalphabetic(cipherText):
    alphabet="abcdefghijklmnopqrstuvwxyz"
    frequencies=[]
    letters=[]
    for letter in alphabet:
        count=0
        for compareLetter in cipherText:
            if letter==compareLetter.lower():
                count+=1
        letters.append(letter)
        frequencies.append(count)
    sfrequencies, sletters = sortValues(frequencies, letters)
    topFiveLetters = sletters[len(letters)-5:]
    topFiveFrequencies = sfrequencies[len(frequencies)-5:]
    #print topFiveLetters
    i=0
    possibleAnswers=[]
    while i<5:
        possibleAnswers.append(findLetterA(topFiveLetters[i]))
        i+=1
    return possibleAnswers
def getLikelyKeyLength(spacing):
    i=2
    mostFactors=0
    mostLikely=0
    factors=[]
    likely=[]
    while i<50:
        count=0;
        for num in spacing:
            if(num%i==0):
                count+=1
            if(count>mostFactors):
                mostFactors=count
                mostLikely=i
        likely.append(i)
        factors.append(count)
        i+=1
    trashValues, mostLikely = sortValues(factors, likely)
    return mostLikely[len(mostLikely)-5:]

i=0
repeatedWords=[]
spacing = []
while i+2<len(cipherText):
    compareString = cipherText[i] + cipherText[i+1]+cipherText[i+2]
    t=i+2
    while t+2<len(cipherText):
        compareStringTwo = cipherText[t] + cipherText[t+1]+cipherText[t+2]
        if(compareString==compareStringTwo):
            spacing.append(t-i)
            repeatedWords.append(compareString)
        t+=1
    i+=1;
mostLikelyNums=getLikelyKeyLength(spacing)
for mostLikely in mostLikelyNums:
    alphabets=[]
    i=0
    while(i<mostLikely):
        monoAlphabetic=[]
        t=i
        while(t+mostLikely<len(cipherText)):
            #print cipherText[t]
            monoAlphabetic.append(cipherText[t])
            t+=mostLikely
        #print monoAlphabetic
        alphabets.append(monoAlphabetic)
        i+=1
    possibleKeyArrays = []
    for alphabet in alphabets:
        possibleKeyArrays.append(solveMonoalphabetic(alphabet))
    i=0
    print possibleKeyArrays[0]
    while i<5:
        startingLetter=possibleKeyArrays[0][i]
        #print startingLetter
        print constructPossibleWord(startingLetter, possibleKeyArrays[1:])
        i+=1


        
