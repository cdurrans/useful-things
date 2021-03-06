import pandas as pd 
from matplotlib import pyplot as plt
base = 'C:/Users/cdurrans/Downloads/'
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np


#####
#Example of quick plot
####
# df = pd.read_csv(base + 'AbandonedCallExplorationCall_Log.csv')
# #check that key is unique
# assert len(df) == len(df['Call Interaction ID'].unique())
# mu = df['Duration'].mean()
# exp_vals = np.random.exponential(mu,10000)
# n_vals = np.random.normal(mu,df['Duration'].std(),10000)
# sns.kdeplot(df['Duration'],shade=False)
# sns.kdeplot(exp_vals, label="Exp samples",shade=False)
# sns.kdeplot(n_vals, label="Normal samples",shade=False)
# plt.legend()
# plt.axvline(0)
# plt.show()





import warnings
import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels as sm
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
matplotlib.style.use('ggplot')

# Create models from data
def best_fit_distribution(data, bins=200, ax=None, label='Label'):
    distributiondf = pd.DataFrame()
    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0
    # Distributions to check
    DISTRIBUTIONS = [        
        st.alpha,
        st.anglit,
        st.arcsine,
        st.beta,
        st.betaprime,
        st.bradford,
        st.burr,
        st.cauchy,
        st.chi,
        st.chi2,
        st.cosine,
        st.dgamma,
        st.dweibull,
        st.erlang,
        st.expon,
        st.exponnorm,
        st.exponweib,
        st.exponpow,
        st.f,
        st.fatiguelife,
        st.fisk,
        st.foldcauchy,
        st.foldnorm,
        st.frechet_r,
        st.frechet_l,
        st.genlogistic,
        st.genpareto,
        st.gennorm,
        st.genexpon,
        st.genextreme,
        st.gausshyper,
        st.gamma,
        st.gengamma,
        st.genhalflogistic,
        st.gilbrat,
        st.gompertz,
        st.gumbel_r,
        st.gumbel_l,
        st.halfcauchy,
        st.halflogistic,
        st.halfnorm,
        st.halfgennorm,
        st.hypsecant,
        st.invgamma,
        st.invgauss,
        st.invweibull,
        st.johnsonsb,
        st.johnsonsu,
        st.ksone,
        st.kstwobign,
        st.laplace,
        st.levy,
        st.levy_l,
        st.levy_stable,
        st.logistic,
        st.loggamma,
        st.loglaplace,
        st.lognorm,
        st.lomax,
        st.maxwell,
        st.mielke,
        st.nakagami,
        st.ncx2,
        st.ncf,
        st.nct,
        st.norm,
        st.pareto,
        st.pearson3,
        st.powerlaw,
        st.powerlognorm,
        st.powernorm,
        st.rdist,
        st.reciprocal,
        st.rayleigh,
        st.rice,
        st.recipinvgauss,
        st.semicircular,
        st.t,
        st.triang,
        st.truncexpon,
        st.truncnorm,
        st.tukeylambda,
        st.uniform,
        st.vonmises,
        st.vonmises_line,
        st.wald,
        st.weibull_min,
        st.weibull_max,
        st.wrapcauchy
    ]
    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf
    # Estimate distribution parameters from data
    count = -1
    for distribution in DISTRIBUTIONS:
        count += 1
        distributiondf.at[count,'dist'] = distribution.name
        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
                # fit dist to data
                params = distribution.fit(data)
                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]
                distributiondf.at[count,'loc'] = loc
                distributiondf.at[count,'scale'] = scale
                distributiondf.at[count,'arg'] = str(arg)
                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))
                distributiondf.at[count,'sse'] = str(sse)
                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                    end
                except Exception:
                    pass
                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse
        except Exception:
            pass
    distributiondf.at[count,'label'] = label
    return (best_distribution.name, best_params, distributiondf)

def make_pdf(dist, params, size=10000):
    """Generate distributions's Probability Distribution Function """
    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]
    # Get sane start and end points of distribution
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)
    # Build PDF and turn into pandas Series
    x = np.linspace(start, end, size)
    y = dist.pdf(x, loc=loc, scale=scale, *arg)
    pdf = pd.Series(y, x)
    return pdf
