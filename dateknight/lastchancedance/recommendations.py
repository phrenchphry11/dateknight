"""
A class for computing which people's tastes are most similar to one 
another so as to recommend crushes

May 10, 2013
"""

from collections import defaultdict
from operator import itemgetter

class KNN:
    
    def __init__(self, list_of_people):
        self.people = list_of_people
        self.neighbors  = [[] for person in self.people]

    def computeJaccardSim(self, crushlistA, crushlistB):
        """
        Compute the similarity between two people's list of crushes so 
        as to compare tastes
        
        If person A has no crushes currently, instead of being dissimilar 
        from everyone, their similarity is based on how many people person
        B likes
        
        """
        
        if len(crushlistA) == 0:
            return len(crushlistB)
        
        intersection = crushlistA.intersection(crushlistB)
        intersectionSize = len(intersection)
        
        union = crushlistA.union(crushlistB)
        unionSize = len(union)
            
        similarity = float(intersectionSize) / unionSize;
        
        return similarity
        
    def getCrushList(self, person):
        if person == 0:
            return set([1,3, 2])
        elif person == 1:
            return set([])
        elif person == 2:
            return set([1])
        return set([0,1])
    
    def getIndexOfPerson(self, person):
        return person
            
            
    def computeK_NN(self):
        """
        Compute the similarity between each pair of people to determine
        whose tastes are most similar
        
        """
        
        for a in range(len(self.people)):
            for b in range(len(self.people)):
                if a != b:
                    crushlistA = self.getCrushList(a)
                    crushlistB = self.getCrushList(b)
                    similarity = self.computeJaccardSim(crushlistA, crushlistB);
                    
                    if similarity > 0:
                        self.neighbors[a].append((similarity, b));
                    
            self.neighbors[a] = sorted(self.neighbors[a], reverse=True)
                    
    def getK_NN(self, k, person):
        """Return the k (or fewer) nearest neighbors for a given person"""
        
        allNeighbors = self.neighbors[person]
        
        kNeighbors = []
        
        index = 0
        while index < k and index < len(allNeighbors):
            kNeighbors.append(allNeighbors[index][1])
            index += 1
        return kNeighbors
        
    def run(self):
        """(Re)compute the similarities between pairs of people"""
        
        self.neighbors = [[] for person in self.people]
        self.computeK_NN()
        

    
    def getRecommendations(self, k, person):
        """
        Find k people who should be recommended to a specified person
        """
        personIndex = self.getIndexOfPerson(person)
        
        neighbors = self.getK_NN(k, personIndex)
        counts = defaultdict(int)
        for neighbor in neighbors:
            crushes = self.getCrushList(neighbor)
            for crush in crushes:
                if crush != personIndex:
                    counts[crush] += 1
                
        countList = sorted(counts.items(), key=itemgetter(1), reverse=True)
        finalCrushes = [crush[0] for crush in countList][:k]
        return [self.people[index] for index in finalCrushes]

if __name__=="__main__":
    crushlistA = set([0,5,3])
    crushlistB = set([0,5,3])
    
    knn = KNN(["PERSONA", "PERSONB", "PERSONC", "PERSOND"])
    knn.computeK_NN()
    print knn.getRecommendations(3, 0)
