import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def compute_growth(x, p0, r0):
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
    baseline_patients = compute_growth(np.arange(len(confirmed_cases)), 1., r0)
    baseline_patients = confirmed_cases / baseline_patients
    return baseline_patients[len(baseline_patients)//2:].mean()


def estimate_exponential_function(confirmed_cases):
    """
    Estimate parameters for an exponential function best fitting the confirmed cases provided.
    :param confirmed_cases: confirmed cases over time. The observations have to have equidistant time steps
    :return: p0, r0 of the exponential function
    """
    r0 = estimate_r0(confirmed_cases)
    p0 = estimate_p0(confirmed_cases, r0)
    return p0, r0


data_frame = pd.read_csv('./data/raw_data/kaggle_covid19_global_forecasting_week_1/train.csv')

data_frame_ger = data_frame[data_frame['Country/Region'] == 'Germany']
confirmed_cases_ger = data_frame_ger['ConfirmedCases'].values
r0_ger = estimate_r0(confirmed_cases_ger)
p0_ger = estimate_p0(confirmed_cases_ger, r0_ger)

plt.plot(confirmed_cases_ger)
plt.plot(compute_growth(np.arange(51), p0_ger, r0_ger))

# plt.plot(growth_factor)