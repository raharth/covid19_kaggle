import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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
    return baseline_patients[len(baseline_patients)//2:].mean()


def estimate_exponential_function(confirmed_cases):
    """
    Estimate parameters for an exponential function best fitting the confirmed cases provided.
    :param confirmed_cases: confirmed cases over time. The observations have to have equidistant time steps
    :return: p0, r0 of the exponential function
    """
    if (confirmed_cases > 0).sum() <= 5 or np.max(confirmed_cases) < 50:
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


data_frame = pd.read_csv('./data/raw_data/kaggle_covid19_global_forecasting_week_1/train.csv')
exp_country_dict = create_country_exp_parameter(data_frame)

# plot all curves
for key in exp_country_dict.keys():
    p0, r0 = exp_country_dict[key]
    plt.plot(compute_infected(np.arange(50), p0, r0))
plt.show()

# plot some countries
countries = ['Germany', 'Italy', 'US']
for key in countries:
    p0, r0 = exp_country_dict[key]
    plt.plot(compute_infected(np.arange(60), p0, r0))
    plt.plot(data_frame[data_frame['Country/Region'] == key]['ConfirmedCases'].values)
    plt.title(key)
    plt.show()


# r0 = estimate_r0(confirmed_cases)
# p0 = estimate_p0(confirmed_cases, r0)
#
# plt.plot(confirmed_cases)
# plt.plot(compute_growth(np.arange(51), p0_ger, r0_ger))
# for key in exp_country_dict.keys():
#     p0, r0 = exp_country_dict[key]
#     if p0 == 4969489243995030:
#         print(key)
#
#
# exp_country_dict['Montenegro']
#
# data_frame_country = data_frame[data_frame['Country/Region'] == 'Montenegro']
#
# exp_country_dict['China']