import numpy as np


class GMM:

    def __init__(self, k=3, epsil=0.0001):
        self.k = k
        self.epsil = epsil

        from collections import namedtuple

    def EMfit(self, X, iterMax= 1000):
        n,d = X.shape;



        log_likelihoods = []

        mu = X[np.random.choice(n, self.k, False), :]


        Sigma = [np.eye(d)] * self.k



        w = [1. / self.k] * self.k

        R = np.zeros((n, self.k))


        P = lambda mu, s: np.linalg.det(s) ** -.5 ** (2 * np.pi) ** (-X.shape[1] / 2.)* np.exp(-.5 * np.einsum('ij, ij -> i', \
                                                   X - mu, np.dot(np.linalg.inv(s), (X - mu).T).T))

        while len(log_likelihoods) < iterMax:

            for k in range(self.k):
                R[:, k] = w[k] * P(mu[k], Sigma[k])

            log_likelihood = np.sum(np.log(np.sum(R, axis=1)))

            log_likelihoods.append(log_likelihood)

            R = (R.T / np.sum(R, axis=1)).T

            N_ks = np.sum(R, axis=0)

            for k in range(self.k):


                mu[k] = 1. / N_ks[k] * np.sum(R[:, k] * X.T, axis=1).T
                x_mu = np.matrix(X - mu[k])

                Sigma[k] = np.array(1 / N_ks[k] * np.dot(np.multiply(x_mu.T, R[:, k]), x_mu))

                w[k] = 1. / n * N_ks[k]

            if len(log_likelihoods) < 2: continue
            if np.abs(log_likelihood - log_likelihoods[-2]) < self.epsil: break
        from collections import namedtuple
        self.params = namedtuple('params', ['mu', 'Sigma', 'w', 'log_likelihoods', 'num_iters'])
        print 'mu', mu
        print 'Sigma', Sigma
        self.params.mu = mu
        self.params.Sigma = Sigma
        self.params.w = w
        self.params.log_likelihoods = log_likelihoods
        self.params.num_iters = len(log_likelihoods)

        return self.params

    def plot_log_likelihood(self):
        import pylab as plt
        plt.plot(self.params.log_likelihoods)
        plt.title('Log Likelihood vs iteration plot')
        plt.xlabel('Iterations')
        plt.ylabel('log likelihood')
        plt.show()
'''
    def predict(self, x):
        p=lambda mu, s: np.linalg.det(s) ** - 0.5 * (2 * np.pi) ** \
                        
                        
                          (-len(x) / 2) * np.exp(-0.5 * np.dot(x - mu, \
                                                               np.dot(np.linalg.inv(s), x - mu)))
        probs=np.array([w * p(mu, s) for mu, s, w in \
                        
                        
                          zip(self.params.mu, self.params.Sigma, self.params.w)])

        return probs/np.sum(probs)


'''
def demo_2d():
    np.random.seed(3)
    m1, cov1 = [9, 8], [[.5, 1], [.25, 1]]
    data1 = np.random.multivariate_normal(m1, cov1, 90)

    m2, cov2 = [6, 13], [[.5, -.5], [-.5, .1]]
    data2 = np.random.multivariate_normal(m2, cov2, 45)

    m3, cov3 = [4, 7], [[0.25, 0.5], [-0.1, 0.5]]
    data3 = np.random.multivariate_normal(m3, cov3, 65)
    X = np.vstack((data1, np.vstack((data2, data3))))
    np.random.shuffle(X)

    gmm = GMM(3, 0.000001)
    params = gmm.EMfit(X, iterMax=100)
    print 'log likelihoods', params.log_likelihoods
    import pylab as plt
    from matplotlib.patches import Ellipse

    def plot_ellipse(pos, cov, nstd=2, ax=None, **kwargs):
        def eigsorted(cov):
            values, vects = np.linalg.eigh(cov)
            ord = values.argsort()[::-1]
            return values[ord], vects[:, ord]

        if ax is None:
            ax = plt.gca()

        values, vects = eigsorted(cov)
        theta = np.degrees(np.arctan2(*vects[:, 0][::-1]))

        width, height = 2 * nstd * np.sqrt(abs(values))
        ellip = Ellipse(xy=pos, width=width, height=height, angle=theta, **kwargs)

        ax.add_artist(ellip)
        return ellip

    def disp(X, mu, cov):

        plt.cla()
        clust = len(mu)  # number of clusters
        colors = ['b', 'k', 'g', 'c', 'm', 'y', 'r']
        plt.plot(X.T[0], X.T[1], 'm*')
        for k in range(clust):
            plot_ellipse(mu[k], cov[k], alpha=0.6, color=colors[k % len(colors)])

    fig = plt.figure(figsize=(13, 6))
    fig.add_subplot(121)


    disp(X, params.mu, params.Sigma)
    fig.add_subplot(122)


    plt.plot(np.array(params.log_likelihoods))

    plt.title('Log Likelihood vs iteration plot')

    plt.xlabel('Iterations')
    plt.ylabel('log likelihood')
    plt.show()
#    print gmm.predict(np.array([1, 2]))


if __name__ == "__main__":

    demo_2d()

    k=3
    epsil=0.0001
    iterMax=1000
'''''
    X = np.genfromtxt("", delimiter=',')
    gmm = GMM(k, epsil)
    params = gmm.EMfit(X, iterMax)
    print params.log_likelihoods
    gmm.plot_log_likelihood()
    print gmm.predict(np.array([1, 2]))
'''
