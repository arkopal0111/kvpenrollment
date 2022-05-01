import pandas as pd 
import plotly.express as px
import streamlit as st 

st.set_page_config(page_title = 'Sales Dashboard',
                    page_icon= ':bar_chart:',
                    layout='wide')

def get_data_from_exel():

    df = pd.read_excel(
            
            'supermarkt_sales.xlsx',
            sheet_name='Sales',
            skiprows=3,
            usecols='B:R',
            nrows = 1000,)

    df['hour'] = pd.to_datetime(df['Time'],format = "%H:%M:%S").dt.hour
    return df
df = get_data_from_exel()

#------------- SIDEBAR -------------------
st.sidebar.header("Please Filter Here")
city = st.sidebar.multiselect('Select the City',
                                options = df['City'].unique(),
                                default = df.City.unique())

customer_type = st.sidebar.multiselect('Select the Customer Type',
                                options = df['Customer_type'].unique(),
                                default = df.Customer_type.unique())

gender = st.sidebar.multiselect('Select the Gender',
                                options = df['Gender'].unique(),
                                default = df.Gender.unique())

df_selection = df.query(
    'City ==@city & Customer_type == @customer_type & Gender == @gender')


# -----------------  MAIN PAGE -----------------------------
st.title(":bar_chart: Sales Document")
st.markdown("##")

#TOP KPI's

total_sales = int(df_selection.Total.sum())
average_rating = round(df_selection.Rating.mean(),1)
star_rating = ":star:" * int(round(average_rating,0))
average_sales_by_transaction = round(df_selection.Total.mean(),2)


left_col, mid_col,right_col = st.columns(3)
with left_col:
    st.subheader("Total Sales: ")
    st.subheader(f"US $ {total_sales:,}")
with mid_col:
    st.subheader("Average Rating")
    st.subheader(f"{average_rating} {star_rating}")
with right_col:
    st.subheader("Average Sales Per Transaction: ")
    st.subheader(f"US ${average_sales_by_transaction}")

st.markdown("---")

#--------- SALES BY PRODUCT LINE [BARCHART]-----

sales_by_product_line = (
df_selection.groupby(by=['Product line']).sum()[['Total']].sort_values(by = 'Total')
    )

fig_product_sales = px.bar(sales_by_product_line,
                        x = 'Total',
                        y = sales_by_product_line.index,
                        orientation = 'h',
                        title = '<b>Sales by Product Line</b>',
                        color_discrete_sequence = ['#0083B8'] * len(sales_by_product_line),
                        template = 'plotly_white',
                        )   
fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = dict(showgrid = False))


#---------------- SALES BY HOUR-------------
sales_by_hour = df_selection.groupby(by=['hour']).sum()[['Total']]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x = sales_by_hour.index,
    y = 'Total',
    title = '<b>Sales By Hour</b>',
    color_discrete_sequence = ['#0083B8'] * len(sales_by_product_line),

    template = 'plotly_white'
    )
fig_hourly_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = dict(tickmode='linear'),
    yaxis = (dict(showgrid = False))
    )

left_col, right_col = st.columns(2)
left_col.plotly_chart(fig_hourly_sales,use_container_width = True)
right_col.plotly_chart(fig_product_sales,use_container_width = True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)