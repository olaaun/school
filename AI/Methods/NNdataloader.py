__author__ = 'kaiolae'
__author__ = 'kaiolae'
import Backprop_skeleton as Bp
import matplotlib.pyplot as plt
import time
import sys

#Class for holding your data - one object for each line in the dataset
class dataInstance:

    def __init__(self,qid,rating,features):
        self.qid = qid #ID of the query
        self.rating = rating #Rating of this site for this query
        self.features = features #The features of this query-site pair.

    def __str__(self):
        return "Datainstance - qid: "+ str(self.qid)+ ". rating: "+ str(self.rating)+ ". features: "+ str(self.features)

    def __lt__(self, other):
        return self.rating<other.rating

    def __gt__(self, other):
        return self.rating>other.rating

    def __eq__(self, other):
        return self.qid == other.qid


#A class that holds all the data in one of our sets (the training set or the testset)
class dataHolder:

    def __init__(self, dataset):
        self.dataset = self.loadData(dataset)

    def loadData(self,file):
        #Input: A file with the data.
        #Output: A dict mapping each query ID to the relevant documents, like this: dataset[queryID] = [dataInstance1, dataInstance2, ...]
        data = open(file)
        dataset = {}
        for line in data:
            #Extracting all the useful info from the line of data
            lineData = line.split()
            rating = int(lineData[0])
            qid = int(lineData[1].split(':')[1])
            features = []
            for elem in lineData[2:]:
                if '#docid' in elem: #We reached a comment. Line done.
                    break
                features.append(float(elem.split(':')[1]))
            #Creating a new data instance, inserting in the dict.
            di = dataInstance(qid,rating,features)
            if qid in dataset.keys():
                dataset[qid].append(di)
            else:
                dataset[qid]=[di]
        return dataset


def runRanker(trainingset, testset):
    #Insert the code for training and testing your ranker here.
    #Dataholders for training and testset
    dhTraining = dataHolder(trainingset)
    dhTesting = dataHolder(testset)

    #The lists below should hold training patterns in this format: [(data1Features,data2Features), (data1Features,data3Features), ... , (dataNFeatures,dataMFeatures)]
    #The training set needs to have pairs ordered so the first item of the pair has a higher rating.
    trainingPatterns = [] #For holding all the training patterns we will feed the network
    testPatterns = [] #For holding all the test patterns we will feed the network
    for qid in dhTraining.dataset.keys():
        #This iterates through every query ID in our training set
        dataInstance=dhTraining.dataset[qid] #All data instances (query, features, rating) for query qid
        #Store the training instances into the trainingPatterns array. Remember to store them as pairs, where the first item is rated higher than the second.
        #Hint: A good first step to get the pair ordering right, is to sort the instances based on their rating for this query. (sort by x.rating for each x in dataInstance)
        dataInstance.sort(reverse=True)
        for i in range(len(dataInstance)-1):
            for j in range(i+1,len(dataInstance)):
                if dataInstance[i].rating != dataInstance[j].rating:
                    trainingPatterns.append((dataInstance[i], dataInstance[j]))

    for qid in dhTesting.dataset.keys():
        #This iterates through every query ID in our test set
        dataInstance=dhTesting.dataset[qid]
        #Store the test instances into the testPatterns array, once again as pairs.
        dataInstance.sort(reverse=True)
        for i in range(len(dataInstance)-1):
            for j in range(i+1,len(dataInstance)):
                if dataInstance[i].rating != dataInstance[j].rating:
                    testPatterns.append((dataInstance[i], dataInstance[j]))

    print("Done adding training and test patterns")

    all_test_error_rates = []
    all_training_error_rates = []
    for run in range(7):
        #New network with random initial weights
        nn = Bp.NN(46,10,0.001)
        print("\nBeginning run number " + str(run+1))
        test_error_rates = []
        training_error_rates = []
        for epoch in range(25):
            print("Iteration "+ str(epoch+1) + ", time passed: " + "{0:.2f}".format(time.time()-start_time) + " seconds")
            #Running 25 iterations, measuring testing performance after each round of training.
            #Training
            nn.train(trainingPatterns,iterations=1)
            #Check ANN performance after training.
            test_error_rates.append(nn.countMisorderedPairs(testPatterns))
            training_error_rates.append(nn.countMisorderedPairs(trainingPatterns))
        all_test_error_rates.append(test_error_rates)
        all_training_error_rates.append(training_error_rates)

    average_test_error_rates = []
    average_training_error_rates = []
    for i in range(len(all_test_error_rates[0])):
        sum_test = 0
        sum_training = 0
        for j in range(len(all_test_error_rates)):
            sum_test += all_test_error_rates[j][i]
            sum_training += all_training_error_rates[j][i]
        average_test_error_rates.append(sum_test/len(all_test_error_rates))
        average_training_error_rates.append(sum_training/len(all_test_error_rates))

    #Store the data returned by countMisorderedPairs and plot it, showing how training and testing errors develop.
    epoch_list = list(range(1, len(average_test_error_rates)+1))
    plt.plot(epoch_list, average_test_error_rates, label='Test error rate')
    plt.plot(epoch_list, average_training_error_rates, label='Training error rate')
    plt.ylabel("Error rates")
    plt.xlabel("Epochs")
    plt.legend()
    plt.savefig("plot.png")
    plt.show()


start_time = time.time()
runRanker("ranknetData\\train.txt","ranknetData\\test.txt")
