import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def compute_infected(x, p0, r0):
    """
    Computes y-values for an exponential function
    :param x: values to compute y for
    :param p0: multiplicative start value
    :param r0: base for the exponential function
    :return: y
    """
    return p0 * r0 ** x


def estimate_growth_factors(confirmed_cases):
    """
    Estimates the growth factor for an array between the consecutive observations.
    :param confirmed_cases: confirmed cases over time. The observations have to have equidistant time steps
    :return: list of growth factors
    """
    confirmed_cases = confirmed_cases[confirmed_cases > 0]
    growth_factor = np.array(
        [confirmed_cases[i + 1] / confirmed_cases[i] for i in range(len(confirmed_cases) - 1)])
    return growth_factor


def estimate_r0(confirmed_cases):
    """
    Estimates the base of an exponential function.

    :param confirmed_cases: confirmed cases over time. The observations have to have equidistant time steps
    :return: base for the exponential function
    """
    growth_factor = estimate_growth_factors(confirmed_cases)
    return growth_factor[len(growth_factor) // 2:].mean()


def estimate_p0(confirmed_cases, r0):
    """
    Estimates the multiplicative p of an exponential function, p*r0^x.
    :param confirmed_cases: confirmed cases over time. The observations have to have equidistant time steps
    :param r0: exponential base
    :return:
    """
    baseline_patients = compute_infected(np.arange(len(confirmed_cases)), 1., r0)
    baseline_patients = confirmed_cases / baseline_patients
    return baseline_patients[len(baseline_patients) // 2:].mean()


def estimate_exponential_function(confirmed_cases):
    """
    Estimate parameters for an exponential function best fitting the confirmed cases provided.
    :param confirmed_cases: confirmed cases over time. The observations have to have equidistant time steps
    :return: p0, r0 of the exponential function
    """
    if (confirmed_cases > 0).sum() <= 5:
        return -1
    r0 = estimate_r0(confirmed_cases)
    p0 = estimate_p0(confirmed_cases, r0)
    return p0, r0


def create_country_exp_parameter(data_frame):
    countries = np.unique(data_frame['Country/Region'].values)
    exp_country_dict = {}
    for country in countries:
        data_frame_country = data_frame[data_frame['Country/Region'] == country]
        confirmed_cases = data_frame_country['ConfirmedCases'].values
        params = estimate_exponential_function(confirmed_cases)
        if not params == -1:
            exp_country_dict[country] = params
    return exp_country_dict


def transform_country_names_for_exp(exp_country_dict):
    """
    Cleaning names for countries to match.

    :param exp_country_dict: dictionary with exp params
    :return: transformed exp_country_dict
    """
    transform_countries = {'Czechia': 'Czech Republic',
                           'Korea, South': 'South Korea',
                           'Taiwan*': 'Taiwan',
                           'US': 'United States'}
    for country in transform_countries:
        exp_country_dict[transform_countries[country]] = exp_country_dict[country]
        del exp_country_dict[country]
    del exp_country_dict['Cruise Ship']
    return exp_country_dict


data_frame = pd.read_csv('./data/preprocessed_data/covid19_global_forecast/country_train.csv')
exp_country_dict = create_country_exp_parameter(data_frame)
exp_country_dict = transform_country_names_for_exp(exp_country_dict)

# plot all curves
for key in exp_country_dict.keys():
    p0, r0 = exp_country_dict[key]
    plt.plot(compute_infected(np.arange(50), p0, r0))
plt.show()

# plot some countries
countries = ['Germany', 'Italy', 'US']
color = {'Germany': 'blue', 'Italy': 'orange', 'US': 'green'}
for country in countries:
    p0, r0 = exp_country_dict[country]
    confirmed_cases = data_frame[data_frame['Country/Region'] == country]['ConfirmedCases'].values
    plt.plot(compute_infected(np.arange(len(confirmed_cases)), p0, r0), label=country)
    plt.plot(confirmed_cases)
    plt.ylim((0, 100000))
    plt.title(country)
    plt.show()

###################
country_df = pd.read_csv('./data/preprocessed_data/merged_ourworldindata.csv')
country_df['r0'] = 0.
for country in exp_country_dict:
    country_df.loc[country_df['country'] == country, ['r0']] = exp_country_dict[country][1]

country_df.to_csv('./data/preprocessed_data/full_country_data.csv')
country_df = pd.read_csv('./data/preprocessed_data/full_country_data.csv')

country_df = country_df.fillna(country_df.mean())
country_df['Two centuries of granted patents in the United States']

corr = country_df.corr()
corr = corr.fillna(0)
corr_val = corr['r0'].values[:-1]
most_related = np.argmax(np.abs(corr['r0'].values[:-1]))

print('most relevant feature: {}, correlation: {}'.format(corr.columns[most_related], corr_val[most_related]))

data = country_df[country_df.r0 > 0][['Expected years of living with disability or disease burden', 'r0']].values
plt.scatter(data[:, 0], data[:, 1])
plt.show()

ax = sns.heatmap(
    corr,
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
)
plt.show()