import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Title of the app
st.title("A/B Testing App")

# Upload CSV data
uploaded_file_test = st.file_uploader("Choose a CSV file for test", type="csv")
uploaded_file_control = st.file_uploader("Choose a CSV file for control", type="csv")
if uploaded_file_test is not None:
    testdata = pd.read_csv(uploaded_file_test)
    st.write(testdata.head())

if uploaded_file_control is not None:
    controldata = pd.read_csv(uploaded_file_control)
    st.write(controldata.head())
       

# Calculate metrics
control = controldata
treatment = testdata

# Perform t-test
t_stat, p_value = stats.ttest_ind(control, treatment)

# Display results
st.write(f"T-statistic: {t_stat}")
st.write(f"P-value: {p_value}")

# Conclusion
alpha = 0.05
if p_value < alpha:
    st.write("Reject the null hypothesis: There is a significant difference between the two groups.")
else:
    st.write("Fail to reject the null hypothesis: There is no significant difference between the two groups.")

# Plot confidence intervals
st.header("Confidence Interval Plot")
control_mean = np.mean(control)
treatment_mean = np.mean(treatment)
control_se = stats.sem(control)
treatment_se = stats.sem(treatment)

# Confidence intervals
ci_control = stats.t.interval(0.95, len(control)-1, loc=control_mean, scale=control_se)
ci_treatment = stats.t.interval(0.95, len(treatment)-1, loc=treatment_mean, scale=treatment_se)

fig, ax = plt.subplots()
ax.errorbar(['Control', 'Treatment'], [control_mean, treatment_mean], 
            yerr=[control_se * 1.96, treatment_se * 1.96], fmt='o', capsize=5)
ax.axhline(y=control_mean, color='blue', linestyle='--', label='Control Mean')
ax.axhline(y=treatment_mean, color='orange', linestyle='--', label='Treatment Mean')
ax.fill_between(['Control', 'Treatment'], ci_control[0], ci_control[1], color='blue', alpha=0.1)
ax.fill_between(['Control', 'Treatment'], ci_treatment[0], ci_treatment[1], color='orange', alpha=0.1)
ax.legend()
st.pyplot(fig)

# Sample size calculation
st.header("Sample Size Calculation")
st.write("The sample size required for an A/B test can be calculated using the following formula:")
st.latex(r'''
n = \left( \frac{Z_{\alpha/2} + Z_{\beta}}{\delta} \right)^2 \cdot \left( \sigma_1^2 + \sigma_2^2 \right)
''')
st.write("""
Where:
- \( Z_{\alpha/2} \) is the Z-score for the desired confidence level (e.g., 1.96 for 95% confidence)
- \( Z_{\beta} \) is the Z-score for the desired power (e.g., 0.84 for 80% power)
- \( \delta \) is the minimum detectable effect
- \( \sigma_1 \) and \( \sigma_2 \) are the standard deviations of the control and treatment groups
""")

# Confidence level
st.header("Confidence Level")
st.write("The confidence level represents the probability that the confidence interval contains the true effect size. Common confidence levels are 90%, 95%, and 99%.")
st.latex(r'''
\text{Confidence Interval} = \bar{x} \pm Z_{\alpha/2} \cdot \left( \frac{\sigma}{\sqrt{n}} \right)
''')
st.write("""
Where:
- \( \bar{x} \) is the sample mean
- \( Z_{\alpha/2} \) is the Z-score for the desired confidence level
- \( \sigma \) is the standard deviation
- \( n \) is the sample size
""")

# Duration calculation
st.header("Test Duration Calculation")
st.write("The duration of an A/B test depends on the sample size and the traffic to your site. A simple formula to estimate the duration is:")
st.latex(r'''
\text{Duration (days)} = \frac{n}{\text{Daily Visitors} \times \text{Conversion Rate}}
''')
st.write("""
Where:
- \( n \) is the required sample size
- Daily Visitors is the average number of visitors per day
- Conversion Rate is the baseline conversion rate
""")


