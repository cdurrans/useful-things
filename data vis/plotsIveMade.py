###############
#Plots
###############
import pandas as pd 


def pltRidgePlot(df,category_col, num_column):
    import seaborn as sns
    from matplotlib import pyplot as plt
    sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
    # Initialize the FacetGrid object
    gr = df.groupby(category_col)[num_column].sum()
    pal = sns.cubehelix_palette(len(gr), rot=-.25, light=.7)
    g = sns.FacetGrid(df, row=category_col, hue=category_col, aspect=15, height=.5, palette=pal)
    #
    # Draw the densities in a few steps
    g.map(sns.kdeplot, num_column, clip_on=False, shade=True, alpha=1, lw=1.5, bw=.2)
    g.map(sns.kdeplot, num_column, clip_on=False, color="w", lw=2, bw=.2)
    g.map(plt.axhline, y=0, lw=2, clip_on=False)
    #
    # Define and use a simple function to label the plot in axes coordinates
    def label(x, color, label):
        ax = plt.gca()
        ax.text(0, .2, label, fontweight="bold", color=color,
                ha="left", va="center", transform=ax.transAxes)
    #
    g.map(label, num_column)
    # Set the subplots to overlap
    g.fig.subplots_adjust(hspace=-.25)
    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(yticks=[])
    g.despine(bottom=True, left=True)
    plt.show()



def snscatPlot(df,catVar,numVar,chartKind='bar'):
    sns.set(style="whitegrid")
    # Draw a nested barplot to show survival for class and sex
    g = sns.catplot(x=catVar, y=numVar, data=df,
                    height=6, kind=chartKind, palette="muted")
    g.despine(left=True)
    g.set_ylabels(numVar)
    plt.show()





#bar chart with negative and positive values
import altair as alt
tMinusBBarChart = alt.Chart(both).mark_bar(opacity= 0.5).encode(
        x=alt.X('TopMinusBot'),
        y= alt.Y('HashTags', sort=alt.EncodingSortField(
            field='TopMinusBot',
            op='sum',
            order = 'descending')),
        tooltip=['HashTags','TopMinusBot','Tcount','Bcount'] 
        ).properties(title='Top Minus HashTags '+y_var)

tMinusBBarChartSort = alt.Chart(both).mark_bar(opacity= 0.5).encode(
        x=alt.X('TopMinusBot'),
        y= alt.Y('HashTags', sort=alt.EncodingSortField(
            field='Total Times Used',
            op='sum',
            order = 'descending')),
        tooltip=['HashTags','TopMinusBot','Tcount','Bcount','Total Times Used'] 
        ).properties(title='Top Minus HashTags '+y_var)


tMinusBBarChart = alt.concat(tMinusBBarChart, tMinusBBarChartSort,  spacing=3)
tMinusBBarChart.save(base+y_var+'_tminusB.html')

tMinusBBarChartSort.save(base+y_var+'_Top Minus Bottom Only.html')

















#3d plot plotly
import plotly.express as px
fig = px.scatter_3d(data, x='Beds', y='acres', z=y_var,
              color='outlierPrediction',
               size_max=18,
               opacity=0.7)
fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
fig.show()



def plotOverTime(dfOT,dateCol):
    import plotly.express as px
    dfOT[dateCol] = pd.to_datetime(dfOT[dateCol])
    dfOT['year'] = dfOT[dateCol].dt.year 
    dfOT['month'] = dfOT[dateCol].dt.month
    dfOT['count'] = 1
    gr = dfOT.groupby(['year','month'])['count'].sum()
    gr = gr.reset_index()
    gr['yearMonth'] = gr['year'].astype('str') +'_'+ gr['month'].astype('str')
    fig = px.line(gr, x = 'yearMonth',y='count')
    fig.show()


# Violin Plot
import seaborn as sns
import matplotlib.pyplot as plt
ax = sns.violinplot(x="outlierPrediction", y="outlierPredictionScore", data=df)
plt.show()




def predVsActualPlot(y_test,y_pred,title="Measure Vs Predicted"):
    import matplotlib.pyplot as plt
    # Visualising the Training set results
    fig, ax = plt.subplots()
    ax.scatter(y_test, y_pred, alpha=0.1)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
    ax.set_xlabel('Measured')
    ax.set_ylabel('Predicted')
    plt.title(title)
    plt.show()






#Need to improve this one
def correlationHeatMap(df,columns):
    correlations = df[columns].corr()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(correlations, vmin=-1, vmax=1)
    fig.colorbar(cax)
    ticks = np.arange(0,len(columns),1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(columns)
    ax.set_yticklabels(columns)
    plt.show()



import seaborn as sns; sns.set(style="ticks", color_codes=True)
xvars = populationColumns + ['TotalPopulation']
g = sns.pairplot(df[xvars])
plt.show()












#Outlier detection
#modified from sklearn
from sklearn.neighbors import LocalOutlierFactor
clf = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
outlierColumns = ['acres', 'Beds','SqFt',y_var]
y_pred = clf.fit_predict(df[outlierColumns])
X_scores = clf.negative_outlier_factor_

plt.title("Local Outlier Factor (LOF)")
plt.scatter(df['Beds'], df[y_var], color='k', s=3., label='Data points')
# plot circles with radius proportional to the outlier scores
radius = (X_scores.max() - X_scores) / (X_scores.max() - X_scores.min())
plt.scatter(df['Beds'], df[y_var], s=1000 * radius, edgecolors='r',
            facecolors='none', label='Outlier scores')
plt.axis('tight')
plt.xlim((-5, 5))
plt.ylim((-5, 5))
plt.xlabel("prediction errors: %d" % (n_errors))
legend = plt.legend(loc='upper left')
legend.legendHandles[0]._sizes = [10]
legend.legendHandles[1]._sizes = [20]
plt.show()



#confusion Matrix
#borrowed, extreme outlier detection with keras
#untested
def confusion_matrix_plot(true,predicted,labels):
    from matplotlib import pyplot as plt
    from sklearn.metrics import confusion_matrix
    import seaborn as sns
    conf_matrix = confusion_matrix(true, predicted)
    plt.figure(figsize=(8, 8))
    sns.heatmap(conf_matrix, xticklabels=labels, yticklabels=labels, annot=True, fmt="d");
    plt.title("Confusion matrix")
    plt.ylabel('True class')
    plt.xlabel('Predicted class')
    plt.show()


#untested
#borrowed extreme outlier detection with keras
def precision_recall_plot(trueClasses,predictionScore):
    #Precision Recall Plot
    from sklearn.metrics import precision_recall_curve
    precision_rt, recall_rt, threshold_rt = precision_recall_curve(trueClasses, predictionScore)
    plt.plot(threshold_rt, precision_rt[1:], label="Precision",linewidth=5)
    plt.plot(threshold_rt, recall_rt[1:], label="Recall",linewidth=5)
    plt.title('Precision and recall for different threshold values')
    plt.xlabel('Threshold')
    plt.ylabel('Precision/Recall')
    plt.legend()
    plt.show()
















import statsmodels.api as sm
from scipy import stats
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
from statsmodels.graphics.gofplots import ProbPlot

def residualsVsFitted(model,y_true):
    model_fitted_y = model.fittedvalues
    # model residuals
    model_residuals = model.resid
    # normalized residuals
    model_norm_residuals = model.get_influence().resid_studentized_internal
    # absolute squared normalized residuals
    model_norm_residuals_abs_sqrt = np.sqrt(np.abs(model_norm_residuals))
    # absolute residuals
    model_abs_resid = np.abs(model_residuals)
    # leverage, from statsmodels internals
    model_leverage = model.get_influence().hat_matrix_diag
    # cook's distance, from statsmodels internals
    model_cooks = model.get_influence().cooks_distance[0]
    plot_lm_1 = plt.figure()
    plot_lm_1.axes[0] = sns.residplot(model_fitted_y, y_true, lowess=True, scatter_kws={'alpha': 0.5}, line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})
    plot_lm_1.axes[0].set_title('Residuals vs Fitted')
    plot_lm_1.axes[0].set_xlabel('Fitted values')
    plot_lm_1.axes[0].set_ylabel('Residuals');
    plt.show()

def qqNormPlot(model):
    # model values
    model_fitted_y = model.fittedvalues
    # model residuals
    model_residuals = model.resid
    # normalized residuals
    model_norm_residuals = model.get_influence().resid_studentized_internal
    # absolute squared normalized residuals
    model_norm_residuals_abs_sqrt = np.sqrt(np.abs(model_norm_residuals))
    # absolute residuals
    model_abs_resid = np.abs(model_residuals)
    # leverage, from statsmodels internals
    model_leverage = model.get_influence().hat_matrix_diag
    # cook's distance, from statsmodels internals
    model_cooks = model.get_influence().cooks_distance[0]
    QQ = ProbPlot(model_norm_residuals)
    plot_lm_2 = QQ.qqplot(line='45', alpha=0.5, color='#4C72B0', lw=1)
    plot_lm_2.axes[0].set_title('Normal Q-Q')
    plot_lm_2.axes[0].set_xlabel('Theoretical Quantiles')
    plot_lm_2.axes[0].set_ylabel('Standardized Residuals');
    # annotations
    abs_norm_resid = np.flip(np.argsort(np.abs(model_norm_residuals)), 0)
    abs_norm_resid_top_3 = abs_norm_resid[:3]
    for r, i in enumerate(abs_norm_resid_top_3):
        plot_lm_2.axes[0].annotate(i,
                                xy=(np.flip(QQ.theoretical_quantiles, 0)[r],
                                    model_norm_residuals[i]));
    plt.show()


def ResidualsVsLeverage(model):
    # model values
    model_fitted_y = model.fittedvalues
    # model residuals
    model_residuals = model.resid
    # normalized residuals
    model_norm_residuals = model.get_influence().resid_studentized_internal
    # absolute squared normalized residuals
    model_norm_residuals_abs_sqrt = np.sqrt(np.abs(model_norm_residuals))
    # absolute residuals
    model_abs_resid = np.abs(model_residuals)
    # leverage, from statsmodels internals
    model_leverage = model.get_influence().hat_matrix_diag
    # cook's distance, from statsmodels internals
    model_cooks = model.get_influence().cooks_distance[0]
    plot_lm_4 = plt.figure();
    plt.scatter(model_leverage, model_norm_residuals, alpha=0.5);
    sns.regplot(model_leverage, model_norm_residuals,
                scatter=False,
                ci=False,
                lowess=True,
                line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8});
    plot_lm_4.axes[0].set_xlim(0, max(model_leverage)+0.01)
    plot_lm_4.axes[0].set_ylim(-3, 5)
    plot_lm_4.axes[0].set_title('Residuals vs Leverage')
    plot_lm_4.axes[0].set_xlabel('Leverage')
    plot_lm_4.axes[0].set_ylabel('Standardized Residuals');
    # annotations
    leverage_top_3 = np.flip(np.argsort(model_cooks), 0)[:3]
    for i in leverage_top_3:
        plot_lm_4.axes[0].annotate(i,
                                    xy=(model_leverage[i],
                                        model_norm_residuals[i]));
    plt.show()


def StandardizedResiduals(model):
    # model values
    model_fitted_y = model.fittedvalues
    # model residuals
    model_residuals = model.resid
    # normalized residuals
    model_norm_residuals = model.get_influence().resid_studentized_internal
    # absolute squared normalized residuals
    model_norm_residuals_abs_sqrt = np.sqrt(np.abs(model_norm_residuals))
    # absolute residuals
    model_abs_resid = np.abs(model_residuals)
    # leverage, from statsmodels internals
    model_leverage = model.get_influence().hat_matrix_diag
    # cook's distance, from statsmodels internals
    model_cooks = model.get_influence().cooks_distance[0]
    #
    plot_lm_3 = plt.figure()
    plt.scatter(model_fitted_y, model_norm_residuals_abs_sqrt, alpha=0.5);
    sns.regplot(model_fitted_y, model_norm_residuals_abs_sqrt,
                scatter=False,
                ci=False,
                lowess=True,
                line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8});
    plot_lm_3.axes[0].set_title('Scale-Location')
    plot_lm_3.axes[0].set_xlabel('Fitted values')
    plot_lm_3.axes[0].set_ylabel('$\sqrt{|Standardized Residuals|}$')
    # annotations
    abs_sq_norm_resid = np.flip(np.argsort(model_norm_residuals_abs_sqrt), 0)
    abs_sq_norm_resid_top_3 = abs_sq_norm_resid[:3]
    for i in abs_sq_norm_resid_top_3:
        plot_lm_3.axes[0].annotate(i,
                                    xy=(model_fitted_y[i],
                                        model_norm_residuals_abs_sqrt[i]));
    plt.show()














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
def best_fit_distribution(data, bins=200, ax=None):
    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0
    # Distributions to check
    DISTRIBUTIONS = [        
        # st.alpha,
        # st.anglit,
        # st.arcsine,
        # st.beta,
        # st.betaprime,
        # st.bradford,
        # st.burr,
        # st.cauchy,
        # st.chi,
        # st.chi2,
        # st.cosine,
        # st.dgamma,
        # st.dweibull,
        # st.erlang,
        st.expon,
        st.exponnorm,
        st.exponweib,
        st.exponpow,
        # st.f,
        # st.fatiguelife,
        # st.fisk,
        # st.foldcauchy,
        # st.foldnorm,
        # st.frechet_r,
        # st.frechet_l,
        # st.genlogistic,
        # st.genpareto,
        # st.gennorm,
        st.genexpon,
        # st.genextreme,
        # st.gausshyper,
        # st.gamma,
        # st.gengamma,
        # st.genhalflogistic,
        # st.gilbrat,
        # st.gompertz,
        # st.gumbel_r,
        # st.gumbel_l,
        # st.halfcauchy,
        # st.halflogistic,
        st.halfnorm,
        # st.halfgennorm,
        # st.hypsecant,
        # st.invgamma,
        # st.invgauss,
        # st.invweibull,
        # st.johnsonsb,
        # st.johnsonsu,
        # st.ksone,
        # st.kstwobign,
        # st.laplace,
        # st.levy,
        # st.levy_l,
        # st.levy_stable,
        # st.logistic,
        # st.loggamma,
        # st.loglaplace,
        # st.lognorm,
        # st.lomax,
        # st.maxwell,
        # st.mielke,
        # st.nakagami,
        # st.ncx2,
        # st.ncf,
        # st.nct,
        st.norm,
        # st.pareto,
        # st.pearson3,
        # st.powerlaw,
        # st.powerlognorm,
        # st.powernorm,
        # st.rdist,
        # st.reciprocal,
        # st.rayleigh,
        # st.rice,
        # st.recipinvgauss,
        # st.semicircular,
        # st.t,
        # st.triang,
        st.truncexpon,
        st.truncnorm,
        # st.tukeylambda,
        # st.uniform,
        # st.vonmises,
        # st.vonmises_line,
        # st.wald,
        # st.weibull_min,
        # st.weibull_max,
        st.wrapcauchy
    ]
    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf
    # Estimate distribution parameters from data
    for distribution in DISTRIBUTIONS:
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
                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))
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
    return (best_distribution.name, best_params)

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

# Load data from statsmodels datasets
data = dataSample[yvar].copy()
# Plot for comparison
plt.figure(figsize=(12,8))
ax = data.plot(kind='density',   alpha=0.5)
# Save plot limits
dataYLim = ax.get_ylim()

# Find best fit distribution
best_fit_name, best_fit_params = best_fit_distribution(data, 200, ax)
best_dist = getattr(st, best_fit_name)

# Update plots
ax.set_ylim(dataYLim)
ax.set_title(u'All Fitted Distributions')
ax.set_xlabel(u'Wait time')
ax.set_ylabel('Frequency')

# Make PDF with best params 
pdf = make_pdf(best_dist, best_fit_params)

# Display
plt.figure(figsize=(12,8))
ax = pdf.plot(lw=2, label='PDF', legend=True)
data.plot(kind='density', alpha=0.5, label='Data', legend=True, ax=ax)

param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
param_str = ', '.join(['{}={:0.2f}'.format(k,v) for k,v in zip(param_names, best_fit_params)])
dist_str = '{}({})'.format(best_fit_name, param_str)

ax.set_title(u'Wait times. with best fit distribution \n' + dist_str)
ax.set_xlabel(u'Wait time')
ax.set_ylabel('Frequency')

plt.show()

