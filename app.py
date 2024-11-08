import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simpson's paradox")
st.markdown(f"# Simpson's Paradox\nWe follow the example of Covid19 cases in the UK.  \n**Exercise:** Try to find a configuration of sample sizes of the contingency table sample sizes to make the Simpson's paradox disappear (You can adjust these in the sidebar).\n",
            unsafe_allow_html=True)

st.markdown(f"### Death rates by age")
p_50_uv = 0.0634
p_50_v =0.0171
p_younger_uv = 0.0003
p_younger_v = 0.0002
by_age = pd.DataFrame(data=[[p_50_uv, p_50_v], [ p_younger_uv, p_younger_v]],index=["50+", "under 50"], columns=["unvaccinated", "vaccinated"])
st.table(by_age)


st.sidebar.header("Set Sample Sizes:")
n_50_uv = st.sidebar.slider("50+ and unvaccinated", min_value=10, max_value=150_000, value=3440)
n_50_v = st.sidebar.slider("50+ and vaccinated", min_value=10, max_value=150_000, value=27307)
n_younger_uv = st.sidebar.slider("under 50 and unvaccinated", min_value=10, max_value=150_000, value=147612)
n_younger_v = st.sidebar.slider("under 50 and vaccinated", min_value=10, max_value=150_000, value=89807)

st.markdown(f"### Death rate aggregates")
aggr = pd.DataFrame(data={"unvaccinated":[(p_50_uv *n_50_uv + p_younger_uv * p_younger_uv)/(n_50_uv + n_younger_uv)], "vaccinated":[(p_50_v * n_50_v + p_younger_v * n_younger_v)/(n_50_v + n_younger_v)]}, index=["death rate"])
st.table(aggr)
