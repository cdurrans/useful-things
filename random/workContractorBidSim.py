

bidPrep = 5000
Materials = 60000
laborWks = 9
employeeCost = 2800
laborCost = employeeCost * laborWks
weeksDelay = 2
jobTimeToComplete = laborWks + weeksDelay
deadlineToComplete = 12
penaltyCostPerWeek = 12000

if jobTimeToComplete <= deadlineToComplete:
    penalty = 0
else:
    penalty = penaltyCostPerWeek * (jobTimeToComplete-deadlineToComplete)

cost = bidPrep + Materials + laborCost + penalty
print('Cost of Business: ',cost)



#May need to use another distribution to sample from but basic truncated norm is below
# import scipy.stats as stats

# a, b = 500, 600
# mu, sigma = 550, 30
# dist = stats.truncnorm((a - mu) / sigma, (b - mu) / sigma, loc=mu, scale=sigma)

# values = dist.rvs(1000)


meanOfMaterials = 60000
stdOfMaterials = 4000
import numpy as np 
sampledPriceMaterials = np.random.normal(loc=meanOfMaterials,scale=stdOfMaterials)

#I believe numpy arrays can be sampled according to a dist

wksToCompleteList = [7,8,9,10,11,12,13]
wksToCompleteProbs = [0.1,0.3,0.3,0.1,0.05,0.07,0.08]
assert len(wksToCompleteList) == len(wksToCompleteProbs)

np.random.choice(wksToCompleteList, 5, p=wksToCompleteProbs)

