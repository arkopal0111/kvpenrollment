import pandas as pd 
import plotly.express as px
import streamlit as st 

st.set_page_config(page_title = 'Student Enrollment Dashboard',
                    page_icon= ':bar_chart:',
                    layout='wide')

def get_data_from_exel():

    df = pd.read_excel(
            
            'AllStudentDetails.xls',
            sheet_name='AllStudentDetails',
            usecols='A:AY',
            nrows = 495,)
    return df

df = get_data_from_exel()

# -----------------  MAIN PAGE -----------------------------
st.title('Kendriya Vidyalaya No 1 Kanchrapara')
st.header(":bar_chart: Student Enrollment Dashboard")
st.markdown("##")



# ---------------------- SIDE BAR -------------------------

st.sidebar.header("Please Filter Here")

Class = st.sidebar.multiselect('Select the Class',
                                options = df.Class.unique(),
                                default = None)
gender = st.sidebar.multiselect('Select the Gender',
                                options = df.Gender.unique(),
                                default = df.Gender.unique())
adm_cat = st.sidebar.multiselect('Select the Admission Category',
                                options = df['AdmnCategory'].unique(),
                                default = df['AdmnCategory'].unique())
category = st.sidebar.multiselect('Select the Social Category',
                                options = df.Category.unique(),
                                default = df.Category.unique())
minority = st.sidebar.multiselect('Select the Minority',
                                options = df.Minority.unique(),
                                default = df.Minority.unique())

df_selection = df.query(
    'Class == @Class & Gender == @gender & AdmnCategory == @adm_cat & Category == @category & Minority == @minority')

total_boys = df_selection.loc[df_selection.Gender == 'Boy'].StudentCode.count()
total_girls = df_selection.loc[df_selection.Gender =='Girl'].StudentCode.count()
total_strength = df_selection.StudentCode.count()

left_col, mid_col,right_col = st.columns(3)
with left_col:
    st.subheader(":boy: Total Boys")
    st.subheader(total_boys)
with mid_col:
    st.subheader(":girl: Total Girls")
    st.subheader(total_girls) 
with right_col:
    st.subheader(":busts_in_silhouette: Total Strength")
    st.subheader(total_strength)

st.markdown('---')
#------------- BARCHART CATEGORY WISE --------------------


left_col, right_col = st.columns(2)

categorywise = df_selection.groupby(by= ['Category']).count()[['StudentCode']]

fig_category = px.bar(
    categorywise,
    x = categorywise.index,
    y = 'StudentCode',
    title = 'Category Wise Data',
    color_discrete_sequence = ['#0083B8'] * len(categorywise),
    template = 'plotly_white')

fig_category.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = dict(tickmode='linear'),
    yaxis = (dict(showgrid = False)))



adm_catwise = df_selection.groupby(by= ['AdmnCategory']).count()[['StudentCode']] 
fig_adm_category = px.bar(
    adm_catwise,
    x = adm_catwise.index,
    y = 'StudentCode',
    title = 'Admission Category Wise Data',
    color_discrete_sequence = ['#0083B8'] * len(adm_catwise),
    template = 'plotly_white')

fig_adm_category.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = dict(tickmode='linear'),
    yaxis = (dict(showgrid = False)))


with left_col:
    st.dataframe(categorywise)
    st.plotly_chart(fig_category,use_container_width = True)
with right_col:
    st.dataframe(adm_catwise) 
    st.plotly_chart(fig_adm_category,use_container_width = True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
