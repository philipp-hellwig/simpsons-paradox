import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Simpson's paradox")
st.markdown(f"# Simpson's Paradox\nWe follow the example of Covid19 cases in the UK :uk:.  \n**Exercise:** Try to find a configuration of sample sizes of the contingency table sample sizes to make the Simpson's paradox disappear (You can adjust these in the sidebar).\n",
            unsafe_allow_html=True)

st.markdown(f"### Mortality rates by age")
p_50_uv = 0.0634
p_50_v =0.0171
p_younger_uv = 0.0003
p_younger_v = 0.0002
by_age = pd.DataFrame(data=[[ p_younger_uv, p_younger_v],[p_50_uv, p_50_v]],index=["under 50","50+"], columns=["unvaccinated", "vaccinated"])
st.table(by_age)

df_by_age = pd.DataFrame({
    "mortality rate": [p_younger_uv, p_younger_v, p_50_uv, p_50_v],
    "vaccination status": ["unvaccinated", "vaccinated","unvaccinated", "vaccinated"],
    "age group": ["under 50","under 50","50+","50+"]
    })
ax = sns.barplot(data=df_by_age, x="age group", y="mortality rate", hue="vaccination status")
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.bottom'] = False
for i in ax.containers:
    ax.bar_label(i,)
st.pyplot(plt.gcf())

st.sidebar.header("Set Sample Sizes:")
n_younger_uv = st.sidebar.slider("under 50 and unvaccinated", min_value=10, max_value=150_000, value=147612)
n_younger_v = st.sidebar.slider("under 50 and vaccinated", min_value=10, max_value=150_000, value=89807)
n_50_uv = st.sidebar.slider("50+ and unvaccinated", min_value=10, max_value=150_000, value=3440)
n_50_v = st.sidebar.slider("50+ and vaccinated", min_value=10, max_value=150_000, value=27307)

st.markdown(f"### Mortality rate aggregates")
aggr = pd.DataFrame(data={"vaccination status":["unvaccinated","vaccinated"], "mortality rate":[(p_50_uv *n_50_uv + p_younger_uv * p_younger_uv)/(n_50_uv + n_younger_uv),(p_50_v * n_50_v + p_younger_v * n_younger_v)/(n_50_v + n_younger_v)]})
st.table(aggr)
fig, ax = plt.subplots()
ax = sns.barplot(data=aggr, x="vaccination status", y="mortality rate", hue="vaccination status")
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.bottom'] = False
st.pyplot(fig)

if(aggr.loc[0,"mortality rate"] > aggr.loc[1,"mortality rate"]):
    st.markdown(f"Well done! The aggregate now reflects the dynamic found on the subgroup level!")
    st.balloons()