# compute the mean of a sample x
def mean(x):
    N = len(x)
    return 1/N*sum(x)

# compute the variance of a sample x 
def variance(x):
    return mean(x**2) - mean(x)**2




