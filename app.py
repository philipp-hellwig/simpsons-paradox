import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="Simpson's paradox")
tab1, tab2 = st.tabs(["Covid :uk:", "Tennis :tennis:"])

with tab1:
    st.markdown(f"We follow the example of Covid19 cases in the UK. You can find the data set and more information [here](https://www.openintro.org/data/index.php?data=simpsons_paradox_covid).",
                unsafe_allow_html=True)

    st.markdown(f"### Mortality rates by age")
    # these probabilities were calculated using the original data set
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
    
    fig1, ax1 = plt.subplots()
    ax1 = sns.barplot(data=df_by_age, x="age group", y="mortality rate", hue="vaccination status")
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.bottom'] = False
    for i in ax1.containers:
        ax1.bar_label(i,)
    st.pyplot(fig1)

    
    st.markdown(f"**Exercise:** If we assume that the death rates split by age and vaccination status are true, we can see what happens when we vary the sample size for each condition.  \nExplore how the sample sizes for each condition affect the aggregated death rates.  \nWhen does the death rate become larger for the unvaccinated people than for vaccinated people when the data is aggregated?")
    st.header("Set Sample Sizes:")

    n_younger_uv = st.slider("under 50 and unvaccinated", min_value=10, max_value=150_000, value=147612)
    n_younger_v = st.slider("under 50 and vaccinated", min_value=10, max_value=150_000, value=89807)
    n_50_uv = st.slider("50+ and unvaccinated", min_value=10, max_value=150_000, value=3440)
    n_50_v = st.slider("50+ and vaccinated", min_value=10, max_value=150_000, value=27307)

    st.markdown(f"### Mortality rate aggregates")
    aggr = pd.DataFrame(data={"vaccination status":["unvaccinated","vaccinated"], "mortality rate":[(p_50_uv *n_50_uv + p_younger_uv * p_younger_uv)/(n_50_uv + n_younger_uv),(p_50_v * n_50_v + p_younger_v * n_younger_v)/(n_50_v + n_younger_v)]})

    fig, ax = plt.subplots()
    ax = sns.barplot(data=aggr, x="vaccination status", y="mortality rate", hue="vaccination status")
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.bottom'] = False
    for i in ax.containers:
        ax.bar_label(i,)
    st.pyplot(fig)

    if(aggr.loc[0,"mortality rate"] > aggr.loc[1,"mortality rate"]):
        st.markdown(f"Well done! The aggregate now reflects the dynamic found on the subgroup level!")
        st.balloons()

with tab2:
    st.markdown(f"This is a reproduction of Figure 3 in Kievit et al. [(2013)](https://doi.org/10.3389/fpsyg.2013.00513). The data simulates the relationship between performance and arousal.",
                unsafe_allow_html=True)
    np.random.seed(2)

    # simulate aggressive players
    arousal_aggr = np.random.normal(loc=100, scale=10, size=100)
    performance_aggr = arousal_aggr * -1.7 + np.random.normal(loc=300, scale=20, size=100)

    # simulate defensive players
    arousal_def = np.random.normal(loc=100, scale=10, size=100)
    performance_def = arousal_def * 1.3 + np.random.normal(loc=0, scale=20, size=100)

    arousal = np.concatenate((arousal_aggr, arousal_def))
    performance = np.concatenate((performance_aggr, performance_def))

    tennis = pd.DataFrame({
        "arousal":arousal,
        "performance":performance,
        "playstyle":["aggressive" for _ in range(100)] + ["defensive" for _ in range(100)]})
    split = st.selectbox(label="Split by:", options=["nothing","playstyle"])
    split = None if split=="nothing" else split
    fig = sns.lmplot(data=tennis, x="arousal", y="performance", hue=split, ci=None)
    st.pyplot(fig)