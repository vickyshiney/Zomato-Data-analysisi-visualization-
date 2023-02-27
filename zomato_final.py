


!pip install pandas

import pandas as pd
df=pd.read_csv("https://raw.githubusercontent.com/nethajinirmal13/Training-datasets/main/zomato/zomato.csv")
df.head()

from IPython.lib.display import Code
import pandas as pd
df1=pd.read_csv("/content/Country-Code (1).csv")
df1

"""Checking if dataset contains any null"""

nan_values = df.isna()
nan_columns = nan_values.any()

columns_with_nan = df.columns[nan_columns].tolist()
print(columns_with_nan)

"""Let us merge both datasets. This will help us to understand the dataset country-wise"""

df2 = pd.merge(df,df1,on='Country Code',how='left')
df2.head(2)

"""Exploratory Analysis and Visualization,
List of counteries the survey is spread accross
"""

print('List of counteris the survey is spread accross - ')
for x in pd.unique(df2.Country): print(x)
print()
print('Total number to country', len(pd.unique(df2.Country)))

"""
TASK 1: DATA ENGINEERING
"""

!pip install easy-exchange-rates
!pip install geopandas
!pip install dash_bootstrap_components

#Generating the INR exchange rate for other Currencies
from easy_exchange_rates import API
from datetime import date
Curr_code = list(df1['Currency_code'])
Exchange_Rate = []

api = API()
for i in range (0, len(Curr_code)):
  time_series = api.get_exchange_rates(
  base_currency=Curr_code[i], 
  start_date=str(date.today()), 
  end_date=str(date.today()), 
  targets=['INR']
  )
  Exchange_Rate.append((time_series[str(date.today())])['INR'])

df1['Exchange_rate'] = Exchange_Rate

#updating the Exchange rates to Zomato Data Set

Zomato = pd.merge(df2,df1)
Zomato.head(2)

"""Adding a column with rupees as the currency """

#Currency Converstion to INR using exchange rate

ex_rate = list(Zomato['Exchange_rate'])
rate_conversion = list(Zomato ['Average Cost for two'])

Price_in_INR = []

for i in range (0,len(rate_conversion)):
  Price_in_INR.append(ex_rate[i]*rate_conversion[i])

Zomato['Indian_Rupee']=Price_in_INR
Zomato

""" Plot that compares indian currency with other country’s currency """

import matplotlib.pyplot as plt



Zomato.plot(kind='hist', x='Country', y='Exchange_rate',label='Exchange Rate')
plt.xlabel('Country')
plt.ylabel('Exchange Rate (INR/Country Currency)')
plt.title('Exchange Rate Comparison')
plt.legend()
plt.show()

Zomato.to_csv("/content/new_zomato (1).csv", index=False)

"""TASK 2 : DASHBOARD DEVELOPMENT """

!pip install jupyter_dash

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import seaborn as sns

Zomato_data = pd.read_csv("/content/new_zomato (1).csv")
Zomato_data.head()

Zomato_data.info()

Zomato_data.describe()

country_code = pd.read_csv("/content/Country-Code (1).csv")
country_code.head()

Zomato_data.shape

sns.heatmap(Zomato_data.corr(),annot=True)

"""Handling Missing Values

# Let us try to find out wether there are any missing values in the dataset or not, and if there are, we will try to handle them correctly.

"""

import missingno as msn
msn.bar(Zomato_data)

Zomato_data.isnull().sum()

"""As we can see that the Cuisines column has 9 missing values. Let us see how we can handle these NULL values.

"""

Zomato_data['Cuisines'].value_counts()

Zomato_data['Cuisines'].value_counts().count()

"""there are 1825 distinct values in the Cuisines column. So, in order to handle the missing values in the column, we'll replace the NULL values with "Other" to depict that these retaurants serve a different type of cuisine than these 1825 values.

"""

Zomato_data['Cuisines'].fillna("Other", inplace=True)

msn.bar(Zomato_data)

"""By the above plot no missing values found"""

Zomato_data['Cuisines'].isnull().sum()

"""As we can see, there are no more NULL values in the Cuisines column of the dataset.

# Now, let us see what restaurants have "Other" as the cuisine that is served there:
"""

Zomato_data[Zomato_data['Cuisines']=="Other"]

"""Analysing and Visualizing the dataset

"""

#Let's see the different countries from which restaurants are listed on Zomato
country_wise_data = (Zomato_data['Country'].value_counts())
country_wise_data

"""From above details we come to know that the majority of restaurants listed on Zomato are from India, which makes sense as Zomato is a company that has its home-base in India itself. It has only recently started expanding to other countries.

# Let's visulaize this data clearly using a pie-chart
"""

pie_country_wise = px.pie(country_wise_data, values=country_wise_data.values, names=country_wise_data.index, color_discrete_sequence=px.colors.sequential.Inferno)
pie_country_wise.update_traces(textposition='inside')
pie_country_wise.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
pie_country_wise.update_layout(title_text="Zomato's Presence around the World", title_x=0.5)

Zomato_data['Rating color'].value_counts()

country_df = Zomato_data[Zomato_data['Country']=='India']
rating_df = country_df[country_df['Rating color']=='Dark Green']
rating_wise_city_df = rating_df['City'].value_counts()
pie_rating_wise = px.pie(rating_wise_city_df, values=rating_wise_city_df.values, names=rating_wise_city_df.index, color_discrete_sequence=px.colors.sequential.Viridis, hole=0.6)
pie_rating_wise.update_traces(textposition='inside')
pie_rating_wise.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
pie_rating_wise.update_layout(title_text="Country wise % of restaurants having selected number of stars", title_x=0.5)
pie_rating_wise

"""
# Now lets take a look at the cities in India from where maximum number of restaurants are listed on Zomato"""

country_wise_df = Zomato_data[Zomato_data['Country']=='India']
city_count = (country_wise_df['City'].value_counts())
city_count

country_wise_df = Zomato_data[Zomato_data['Country']=='India']
city_count = (country_wise_df['City'].value_counts())
fig = px.bar(city_count, x=city_count.index, y=city_count.values,labels={'x': "Cities","y": "Number of Restaurants"},color_discrete_sequence=px.colors.qualitative.Antique)
fig.update_layout(plot_bgcolor="powderblue")
#fig.update_yaxes(range=[10,20])
fig.update_layout(title_text='Cities in India listed on Zomato', title_x=0.5)

"""# Clearly, most of the restaurants listed on Zomato are located in New Delhi and least are in Mohali and Panchkula

# Lets take a look at how many of these restaurants in each city of India have online delivery services
"""

fig2=px.histogram(country_wise_df, x=country_wise_df['City'], color="Has Online delivery",barmode='group',
                      color_discrete_sequence=px.colors.sequential.Reds_r)
fig2.update_layout(plot_bgcolor="#f4f4f2")
fig2.update_layout(title_text='Restraunts having online delivery service', title_x=0.5)

"""# As expected, New Delhi has the maximum number of restaurants offering online delivery service via Zomato

# Now let's take a look at how does the rating of a restaurant vary with it's average cost for two and wether a higher cost affects rating or not
"""

city_wise_df = Zomato_data[Zomato_data['City']=='New Delhi']
fig = px.scatter(city_wise_df, x="Average Cost for two", y="Aggregate rating",color="Average Cost for two",
                 color_continuous_scale=px.colors.sequential.Reds_r,hover_data=["Restaurant Name"])
fig.update_layout(plot_bgcolor="#f4f4f2")
fig.update_layout(title_text='Cost for Two vs. Rating', title_x=0.5)
fig.show()

"""Now, lets take a look at the rating of the restaurants in India. Let's see in which city are majority of the 5 star rating restaurants located using a donut graph.

"""

# The Rating color column in the dataset represents the stars of the restaurant. The order is as follows:
# - Dark Green: 5 stars
# - Green: 4 stars
# - Yellow: 3 stars
# - Orange: 2 stars
# - Red: 1 star
# - White: No Rating

country_df['Rating color'].value_counts()

rating_df = country_wise_df[country_wise_df['Rating color']=='Dark Green']
rating_wise_city_df = rating_df['City'].value_counts()
pie_rating_wise = px.pie(rating_wise_city_df, values=rating_wise_city_df.values, names=rating_wise_city_df.index, 
                             color_discrete_sequence=px.colors.sequential.Plasma_r, hole=0.6)
pie_rating_wise.update_traces(textposition='inside')
pie_rating_wise.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
pie_rating_wise.update_layout(title_text="% of restaurants having selected number of ★", title_x=0.5)

"""Naturally, most of them are in New Delhi.

# Now, lets see in which country are the majority of restaurants having 5 star rating located on the world map.
"""

rating_df_cmap = Zomato_data[Zomato_data['Rating color']=='Dark Green']
cmap_df = (rating_df_cmap['Country'].value_counts())
cmap_df

fig = px.choropleth(cmap_df, locations=cmap_df.index, locationmode='country names',color=cmap_df.values ,color_continuous_scale=px.colors.sequential.Plasma_r)
fig.update_layout(geo=dict(bgcolor= '#ed7953'), title_text = 'Restaurants having selected number of ★ by Country',title_x=0.5)

import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

train_desc = pd.Series(Zomato_data['Restaurant Name'].tolist()).astype(str)
cloud = WordCloud(width=1440, height=1080,stopwords=STOPWORDS).generate(" ".join(train_desc.astype(str)))
plt.figure(figsize=(20, 15))
plt.imshow(cloud)
plt.title("Most frequent words in the Restaurant column")
plt.axis('off')

"""Clearly a vast majority of them are in India itself."""

!pip install dash_bootstrap_components

# ### Creating the Dashboard using Dash and Plotly
# The first thing that we have to do is initialize the Dash app as follows:

from jupyter_dash import JupyterDash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from plotly import graph_objs as go
from plotly.subplots import make_subplots
import dash_table as dt
app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

# Next, we specify the layout of the app, which describes what the application is supposed to look like. We have used the components such as html.Div, html.H1, html.P, dcc.Dropdown, dcc.Slider and dcc.Graph.
# 
# - The dash_core_components are higher-level components that are interactive and are generated with JavaScript, HTML, and CSS through the React.js library
# - The html_components are normal components which are used in HTML

app.layout = html.Div(children=[
    
    #This is the main header of the dashboard displaying the name - ZOMATO DASHBOARD
    html.Div(children=[
        
            html.H1(children='ZOMATO DASHBOARD'), 
            html.Div(children='A one-stop dashboard to get all your information about Zomato')],
            style={'textAlign': 'center','backgroundColor':'#E23744','color': 'white','font-family':['Open Sans','sans-serif'], 
                   'font-style': ['italic'],'padding-top':'20px','padding-bottom':'40px','fontSize':17}
            ),
#This is the first row of the dashboard displaying three cards
    html.Div(children=[
            
            #The first one is for the number of restaurants on Zomato app from across the world
            html.Div([
                html.H3(children="NUMBER OF RESTAURANTS WORLDWIDE", style={'fontSize':25}),
                html.P(Zomato_data.shape[0], style={'fontSize':30})],
                style={'display':'inline-block','width': '30%','textAlign': 'center','backgroundColor': '#2D2D2D',
                       'color': 'white','margin':'25px','border-radius':'5px','box-shadow':'2px 2px 2px #1f2c56'}
                     ),

  #The second one displays the number of restaurants on Zomato app which are located in the country that has been
            #selected from the first dropdown
            html.Div([
                html.H3(children="NUMBER OF RESTAURANTS IN SELECTED COUNTRY", style={'fontSize':25}),
                html.P(id="numOfRestCountry", children=8652, style={'fontSize':30})],
                style={'display':'inline-block','width': '30%','textAlign': 'center','backgroundColor': '#2D2D2D',
                       'color': 'white','margin':'25px','border-radius':'5px','box-shadow':'2px 2px 2px #1f2c56'}),

   #The third card displays the number of restaurants on Zomato app which are located in the city that has been
            #selected from the second dropdown
            html.Div([
                html.H3(children="NUMBER OF RESTAURANTS IN SELECTED CITY", style={'fontSize':25}),
                html.P(id="numOfRestCity",children=20, style={'fontSize':30})],
                style={'display':'inline-block','width': '30%','textAlign': 'center','backgroundColor': '#2D2D2D',
                       'color': 'white','margin':'25px','border-radius':'5px','box-shadow':'2px 2px 2px #1f2c56'}),
                     ]),

#This is the second row of the dashboard
    html.Div(children=[
            
            #This first div in the second row contains three different Dash core components 
            #Two dropdown lists and a slider
            html.Div(children=[
                    
                #The first component in this Div is a dropdown menu which displays the different countries from which
                #different restaurants are displayed on the Zomato App
                html.P('SELECT COUNTRY: ', style={'color':'white'}),
                dcc.Dropdown(
                        id="countries_dropdown",
                        multi=False,
                        clearable=True,
                        value='India',
                        placeholder="Select Countries:",
                        options=[{'label':c, 'value':c} for c in (country_code['Country'])]),
                html.Br(),
                html.Br(),
 #The second component in this Div is another dropdown menu which displays the different cities from the
                #selected country in earlier dropdown list, from which different restaurants are displayed on Zomato App
                html.P('SELECT CITY: ', style={'color':'white'}),
                dcc.Dropdown(
                        id="cities_dropdown",
                        multi=False,
                        clearable=True,
                        value='New Delhi',
                        placeholder="Select Cities:",
                        options=[]),
                html.Br(),
                html.Br(), 

 #The final component in this Div is a slider which allows us to select ratings from 0 to 5.  
                #These ratings are based on the Rating colors specified for each restaurant. 
                #0 means No Rating and 5 means Highest Rating 
                html.P('SELECT RATING: ', style={'color':'white'}),
                html.Br(),
                dcc.Slider(
                        id='slider',
                        min=0,
                        max=5,
                        step=None,
                        marks=
                        {
                            0: '0★',
                            1: '1★',
                            2: '2★',
                            3: '3★',
                            4: '4★',
                            5: '5★'
                        },
                        value=5)
                ],
                style={'display':'inline-block','textAlign': 'left','backgroundColor': '#2D2D2D','color': 'black',
                        'margin-left':'25px','margin-right':'25px','width':'30%','border-radius':'5px',
                        'box-shadow':'2px 2px 2px #1f2c56','padding':'25px'}
            ),

      #The second div in the second row displays a static pie chart showcasing the presence of Zomato across the globe
            html.Div([
                    dcc.Graph(
                            id="pie-chart1", figure=pie_country_wise, 
                            style={'display':'inline-block','width':'57vh',
                                    'margin-left':'25px','margin-right':'25px','align':'center'})
                    ]),
        
            #This third div in the second row displays a bar chart 
            #This bar chart represents the Top 10 cities(from selected country) having the maximum number of restaurants listed
            #on Zomato
             html.Div([
                    dcc.Graph(
                            id="bar-chart", 
                            style={'display':'inline-block','width':'57vh','margin-left':'25px','margin-right':'25px',
                                   'align':'center'})]
                    )], 

            style={'display':'flex'}
        ),

#This is the third row of the dashboard
    html.Div([
            
            #The first div in this row displays a grouped bar chart
            #This grouped bar chart depicts the number of restaurants having and not having online delivery service, from the 
            # Top 10 cities having maximum number of listings from selected country
            html.Div([
                    dcc.Graph(
                            id="grouped-bar-chart", 
                            style={'display':'inline-block','width':'57vh','margin-left':'25px','margin-right':'25px'})
                    ]),
            
        
            #The second div in this row displays a scatter plot
            #It shows how the rating of restaurant varies with the average price for two people for all restaurants in 
            #the selected city
            html.Div([
                    dcc.Graph(
                            id="scatter_plot", 
                            style={'display':'inline-block','width':'62vh','margin-left':'25px','margin-right':'1px'})
                    ]),
     #The third div in this row displays a donut chart
            #This chart shows the percentage of restaurants having selected number of stars(from slider) from different cities
            #of the selected city
            html.Div([
                    dcc.Graph(
                            id="donut_graph", 
                            style={'display':'inline-block','width':'57vh','margin-left':'25px','margin-right':'25px'})]
                    )], 

            style={'display':'flex','margin-top':'25px'}
        ),
   #This is the fourth row of the dashboard
    html.Div([
        
        #This is the a graph which depicts the denisty of restaurants in a country having selected number of stars
        html.Div([dcc.Graph(id="world_map")],style={'width':'90%','align':'center','margin-left':'25px','margin-right':'25px'})
            
            
        ]),
    
    #This is the footer of the dashboard
    html.Div(children=[
         
            html.Div(children='Created by: vignesh')],
            style={'textAlign': 'center','backgroundColor':'#E23744','color': 'white','font-family':['Open Sans','sans-serif'], 
                   'font-style': ['italic'],'padding-top':'20px','padding-bottom':'20px','fontSize':17}
            )
    
])

""" Next, we specify the callback section of our Dash app. The callbacks are used to establish interactivity and communication between the different components of our Dashboard.
These are the functions that are automatically called by Dash whenever an input component's property changes, in order to update some property in another component (the output).

"""

#This callback function is used to set the values in the City Dropdown menu from Selected Country in Country Dropdown menu
@app.callback(
    Output("cities_dropdown", "options"),
    [Input("countries_dropdown", "value")],suppress_callback_exceptions=True
)
def get_city_options(countries_dropdown):
    df_result = Zomato_data[Zomato_data['Country']==countries_dropdown]
    return [{'label':i , 'value': i} for i in df_result['City'].unique()]

#This callback function is used to set the selected value in the City Dropdown menu as first city listed in the entire city list
@app.callback(
    Output("cities_dropdown", "value"),
   [ Input("cities_dropdown", "options")],suppress_callback_exceptions=True)
def count_city_options(cities_dropdown):
    return [k['value'] for k in cities_dropdown][0]

#This callback function is used to set the value displayed in the SECOND card
#The total number of restaurants listed on Zomato from country selected in dropdown menu 
@app.callback(
    Output("numOfRestCountry", "children"),
    [Input("countries_dropdown", "value")],suppress_callback_exceptions=True)
def well_city_options(countries_dropdown):
    df_result = Zomato_data[Zomato_data['Country']==countries_dropdown]
    return df_result.shape[0]

#This callback function is used to set the value displayed in the THIRD card
#The total number of restaurants listed on Zomato from city selected in dropdown menu 
@app.callback(
    Output("numOfRestCity", "children"),
   [ Input("cities_dropdown", "value")],suppress_callback_exceptions=True)
def great_city_options(cities_dropdown):
    df_result = Zomato_data[Zomato_data['City']==cities_dropdown]
    return df_result.shape[0]

#This callback function is used to update the bar chart displayed in the second row depending upon the country that has been
#selected
@app.callback(
    Output("bar-chart", "figure"),
    [Input("countries_dropdown", "value")],suppress_callback_exceptions=True)
def update_bar_chart(countri):
    country_wise_df = Zomato_data[Zomato_data['Country']==countri]
    city_count = (country_wise_df['City'].value_counts())
    fig = px.bar(city_count, x=city_count.index[:10], y=city_count.values[:10],
                 labels={"x": "Cities","y": "Number of Restaurants"},color_discrete_sequence=px.colors.qualitative.Set1)
    fig.update_layout(plot_bgcolor="#f4f4f2")
    fig.update_layout(title_text='Top 10 cities in Selected Country', title_x=0.5)
    return fig

#This callback function is used to update the grouped bar chart displayed in the third row 
#It takes the country selected in the dropdown as input and accordingly displays the Top 10 cities in that country having or not
#having online delivery service
@app.callback(
    Output("grouped-bar-chart", "figure"),
    [Input("countries_dropdown", "value")],suppress_callback_exceptions=True)
def update_grouped_bar_chart(countri):
    country_wise_df = Zomato_data[Zomato_data['Country']==countri]
    city_count = (country_wise_df['City'].value_counts())
    top_10_cities = list(city_count.index[:10])
    
    top_10_cities_df = country_wise_df[country_wise_df["City"].isin(top_10_cities)]
    
    fig2=px.histogram(top_10_cities_df, y=top_10_cities_df['City'], color="Has Online delivery",barmode='group',
                      color_discrete_sequence=px.colors.sequential.Reds_r)
    fig2.update_layout(plot_bgcolor="#f4f4f2")
    fig2.update_layout(title_text='Restraunts having online delivery service', title_x=0.5)
    
    return fig2

#This callback function is used to update the scatter displayed in the third row 
#It takes the city selected in the dropdown as input and accordingly displays how the rating of restaurants in that city varies
#with their average prices
@app.callback(
    Output("scatter_plot", "figure"),
    [Input("cities_dropdown", "value")],suppress_callback_exceptions=True)
def update_scatter_plot(city):
    city_wise_df = Zomato_data[Zomato_data['City']==city]
    fig = px.scatter(city_wise_df, x="Average Cost for two", y="Aggregate rating",color="Average Cost for two",
                     color_continuous_scale=px.colors.sequential.Reds_r,hover_data=["Restaurant Name"])
    fig.update_layout(plot_bgcolor="#f4f4f2")
    fig.update_layout(title_text='Cost for Two vs. Rating per City', title_x=0.2)
    return fig

#This callback function is used to update the donut graph displayed in the third row 
#It takes the country selected in the dropdown as well as the rating selected in the slider as input 
#It accordingly displays a graph depecting the % of restaurants in each city of that country having those many stars
@app.callback(
    Output("donut_graph", "figure"),
    [Input("countries_dropdown", "value"),Input("slider", "value")],suppress_callback_exceptions=True)
def update_scatter_plot(countri,val):
    country_wise_data = Zomato_data[Zomato_data['Country']==countri]
    
    op='Dark Green'
    if(val == 0):
        op = 'White'
    elif(val==1):
        op = 'Red'
    elif(val==2):
        op = 'Orange'
    elif(val==3):
        op = 'Yellow'
    elif(val==4):
        op = 'Green'
    elif(val==5):
        op = 'Dark Green'
    rating_df = country_wise_data[country_wise_data['Rating color']==op]
    rating_wise_city_df = rating_df['City'].value_counts()
    pie_rating_wise = px.pie(rating_wise_city_df, values=rating_wise_city_df.values, names=rating_wise_city_df.index, 
                             color_discrete_sequence=px.colors.sequential.Reds_r, hole=0.6)
    pie_rating_wise.update_traces(textposition='inside')
    pie_rating_wise.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    pie_rating_wise.update_layout(title_text="% of restaurants having selected number of ★")
    return pie_rating_wise

#This callback function is used to update the world map choropleth displayed in the fourth row 
#It takes the country selected in the dropdown as input 
#This map depicts the denisty of restaurants having selected number of stars, from across the world
@app.callback(
    Output("world_map", "figure"),
    [Input("slider", "value")],suppress_callback_exceptions=True)
def update_world_map(val):
    
    op='Dark Green'
    if(val == 0):
        op = 'White'
    elif(val==1):
        op = 'Red'
    elif(val==2):
        op = 'Orange'
    elif(val==3):
        op = 'Yellow'
    elif(val==4):
        op = 'Green'
    elif(val==5):
        op = 'Dark Green'
        
    rating_df_cmap = Zomato_data[Zomato_data['Rating color']==op]
    cmap_df = (rating_df_cmap['Country'].value_counts())
    
    fig_world = px.choropleth(cmap_df, locations=cmap_df.index, locationmode='country names',color=cmap_df.values ,
                              color_continuous_scale=px.colors.sequential.Reds)
    fig_world.update_layout(geo=dict(bgcolor= '#f4f4f2'), title_text = 'Restaurants having selected number of ★ by Country',
                            title_x=0.5)
    return fig_world
    
if __name__ == '__main__':
    app.run_server(debug=True)

!lsof -i:8050

!kill PID *552*
