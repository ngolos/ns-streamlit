import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

url_csv = "https://raw.githubusercontent.com/ngolos/ns-streamlit/main/june_upd_.csv"

@st.cache
def get_data():
    df = pd.read_csv(url_csv, keep_default_na=False)
    #df['Mo. Revenue'] = df['Mo. Revenue'].astype(str).astype(float, errors='ignore')
    #df['Sales_Mln'] = (df['Sales_Mln']).round(2)
    return df


st.title('Nutrastar Dashboard')
"""
This is supposed to be a multipage framework. 
- Page 1: Product form - Ingredient based view. 
- Page 2: function based view. 
- Page 3: could be google trends, etc. All the data is based on June'2020 Amazon BSL in Dietaty Supplements Category.
- Currently I use a singe page mode. 
"""
df = get_data()


# Filters
#st.sidebar.header('User Input Features')
#product_choice = []

#product_type = df['Sup_Type'].drop_duplicates()
#product_choice = st.sidebar.multiselect('Select product form:', options=sorted(product_type), default='Capsules')

#category list
#function_type=['Beauty', 'Body', 'Brain', 'Digest', 'Energy', 'Fitness', 'Immune', 'Joints', 'Multi', 'Stress_Sleep','Weight_Mngm' ]
#function_choice = st.sidebar.selectbox('Select functionality:', function_type)

st.header('Page 1 - Explore the Largest Ingredient Groups for each Product Form')
product_choice = []

st.markdown(f"Sales Split by Product Form & Ingredient:")
product_type = df['Sup_Type'].drop_duplicates()
product_choice = st.multiselect('Select product form:', options=sorted(product_type), default='Capsules')



#Filter df based on selection
filterd_type_df = df[df['Sup_Type'].isin(product_choice)]
#filterd_type_df


fig2 = px.treemap(filterd_type_df, path=['Category', 'Group'],
                 values='Sales_Mln')

st.plotly_chart(fig2, use_container_width=True)


st.header('Page 2 - Explore Function Claims')

#category list
function_type=['Beauty', 'Body', 'Brain', 'Digest', 'Energy', 'Fitness', 'Immune', 'Joints', 'Multi', 'Stress_Sleep','Weight_Mngm' ]
function_choice = st.selectbox('Select functionality:', function_type)
#Filtered Dataframe based on Functionality

cols_list = ["Sup_Type","Type", 'Active Ingredient', "Group", "Category", "Product Name", "Sales_Mln"]
# Add 'functionality' to the list
cols_list.append(function_choice)
filtered_df = df[cols_list]
dff=filtered_df[filtered_df.iloc[:,-1]!=""]
cat=dff.groupby('Sup_Type').agg(Sales_Mln=('Sales_Mln', 'sum')).sort_values(by="Sales_Mln", ascending=False).reset_index()
cat2=dff.groupby(['Sup_Type','Type', "Active Ingredient",'Category']).agg(Sales_Mln=('Sales_Mln', 'sum')).sort_values(by="Sales_Mln", ascending=False).head(20).reset_index()


st.markdown(f"Total Sales of products with {function_choice} - related claims in Mln $$: **{(cat.Sales_Mln.sum()).round(1)}**")

#st.text('Overall Category pie-chart diagram:')
st.markdown(f"Overall {function_choice} - related claims category structure:")

fig = px.pie(cat, values='Sales_Mln', names='Sup_Type', color='Sup_Type', color_discrete_map={'Capsules':'393B79',
                                 'Chewable':'FF7F0E',
                                 'Powder':'9467BD',
                                 'Tablets':'2CA02C',
                                 'Other':'silver'})
st.plotly_chart(fig, use_container_width=True)


#Filter df based on selection
#filterd_type_df = df[df['Sup_Type'].isin(product_choice)]
#filterd_type_df

#dff1=filterd_type_df.groupby(['Active Ingredient','Category']).agg(Sales_Mln=('Sales_Mln', 'sum')).sort_values(by="Sales_Mln", ascending=False).head(10).reset_index()

"""
Top 20 Ingredients grouped by product form :
"""
#set colors
domain = [
    "Capsules",
    "Tablets",
    "Powder",
    "Other",
    "Gummy",
    "Softgels",
    "Chewable Tablets",
    'Lozenges',
    'Pieces',
    'Caplets',
    '0',
    'CapsulesPowder',
    'CapsulesSoftgels',
    'CapsulesTablets',
    'CapsulesTabletsPowder',
    'TabletsPowder',

]
range = [
    "393B79",
    "2CA02C",
    "9467BD",
    "silver",
    "FFF7F0",
    "FFB79",
    "FDD0A2",
    'silver',
    'silver',
    'silver',
    'silver',
    'silver',
    'silver',
    'silver',
    'silver',
    'silver'
]
chart=alt.Chart(cat2).mark_bar().encode(
    y=alt.Y('Active Ingredient:N', sort='-x'),
    x='Sales_Mln:Q',
    #color=alt.Color('Type:N',scale=alt.Scale(domain=domain, range=range)),
    color='Type:N',
    tooltip=['Sales_Mln', 'Sup_Type', 'Active Ingredient']
)
st.altair_chart(chart, use_container_width=True)

#cat
#cat=cat.reset_index()

#Chart for Top N products
#select nlargerst and show
#top=df.nlargest(5,'Mo. Revenue')[['Active Ingredient', 'Sup_Type', 'Sales_Mln', "Sex"]]

#top['Name']=top['Active Ingredient'] +"-" + top ['Sex']

#top


#"""
#Top 5 Selling Products:
#"""



#c=alt.Chart(top).mark_bar().encode(
#    y=alt.Y('Name:N', sort='-x'),
#    x='Sales_Mln:Q',
#    color=alt.Color('Sup_Type:N', scale=alt.Scale(domain=domain, range=range)),
#    tooltip=['Sup_Type', 'Sales_Mln']
#)


#st.altair_chart(c, use_container_width=True)

#c = alt.Chart(df).mark_circle().encode(
#    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
st.set_option('deprecation.showPyplotGlobalUse', False)
ingredient=dff['Product Name']
text = " ".join(description for description in ingredient)

unwanted = "gummy gummies women one support bottle supplements softgel softgels gel gels health healthy tablets powder natural advanced shelf increase stable help capsules capsule pill pills packaging supports made day may vary non-gmo non gmo veg veggie formula promote promotes dietary absorption nature premium powder powerful wellness 1200mg daily whole food standardized helps nutrition nature best better months free pure ultra pack maximum per serving servings 500mg 1000mg month supply organic supplement mg usa count extract gluten vegan vegetarian caps"
list_unwanted = unwanted.split()

STOPWORDS.update(list_unwanted)
wc = WordCloud(max_font_size=100,min_font_size=6, min_word_length =3, max_words=400, stopwords=STOPWORDS, random_state=4, relative_scaling=0.8, background_color="white", colormap="inferno").generate(text)

plt.figure(figsize=(15,15))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
"""
Word Cloud for the Category :
"""
st.pyplot(use_container_width=True)
