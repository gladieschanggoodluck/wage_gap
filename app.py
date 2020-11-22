# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 20:01:06 2020

@author: gladis
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')



markdown_text = '''
[Quick Facts About the Gender Wage Gap](https://www.americanprogress.org/issues/women/reports/2020/03/24/482141/quick-facts-gender-wage-gap/)
The article discusses the wage gap between females and males. In addition, the article further states that the wage gap between colored females to males is wider than among males only.
[The Simple Truth About the Gender Pay Gap(https://www.aauw.org/resources/research/simple-truth/)
According to the article, working women are paid 82% of what men are paid. Even women who hold advanced degrees received lower pay than men.
GSS[http://www.gss.norc.org/About-The-GSS]
GSS stands for General Social Survey. The survey offers some insightful questions to study the science of the society  in the USA. 
'''

mycol = ['income', 'job_prestige', 'socioeconomic_index', 'education', 'sex']
gss_clean_p2 = gss_clean[mycol]

gss_p2  = gss_clean_p2.groupby(['sex']).agg({'income' : 'mean', 'job_prestige' : 'mean', 'socioeconomic_index' : 'mean', 'education' : 'mean'})
gss_p2 = round(gss_p2, 2)

table = ff.create_table(gss_p2)

gss_p3_table = gss_clean.male_breadwinner.value_counts().reset_index()
px.bar(gss_p3_table , x='index', y='male_breadwinner', color='index',
       labels={'male_breadwinner':'Number of male_breadwinner', 'index':'male_breadwinner choice'},
       title = 'male_breadwinner')


colpercent = round(100*pd.crosstab(gss_clean.male_breadwinner, gss_clean.sex, normalize='columns'),2).reset_index()
colpercent = pd.melt(colpercent, id_vars = 'male_breadwinner', value_vars = ['male', 'female'])
colpercent = colpercent.rename({'value':'colpercent'}, axis=1)

rowpercent = round(100*pd.crosstab(gss_clean.male_breadwinner,  gss_clean.sex, normalize='index'),2).reset_index()
rowpercent = pd.melt(rowpercent, id_vars = 'male_breadwinner', value_vars = ['male', 'female'])
rowpercent = rowpercent.rename({'value':'rowpercent'}, axis=1)

male_breadwinner = pd.crosstab(gss_clean.male_breadwinner, gss_clean.sex).reset_index()
male_breadwinner = pd.melt(male_breadwinner, id_vars = 'male_breadwinner', value_vars = ['male', 'female'])
male_breadwinner = male_breadwinner.rename({'value':'male_breadwinner'}, axis=1)

anes_groupbar = pd.merge(colpercent, rowpercent, on=['male_breadwinner', 'sex'], validate='one_to_one')
anes_groupbar['coltext'] = anes_groupbar['colpercent'].astype(str) + '%'
anes_groupbar['rowtext'] = anes_groupbar['rowpercent'].astype(str) + '%'


gss_p3 = px.bar(anes_groupbar, x='male_breadwinner', y='colpercent', color='sex',
            labels={'male_breadwinner':'male_breadwinner choice', 'colpercent':'Percent'},
            title = 'male_breadwinner',
            text='coltext',
            barmode = 'group')


gss_p4 = px.scatter(gss_clean, x='job_prestige', y='income', 
                 trendline='ols',
                 color = 'sex', 
                 height= 600, width=800,
                 labels={'job_prestige':'The respondents occupational prestige score', 
                        'income':'The respondents personal annual income'},
                 hover_data=['sex', 'education', 'socioeconomic_index'],
                 title = 'Job prestige vs. income')

gss_p5 = px.box(gss_clean, y='income', x = 'sex', color = 'sex',
                   labels={'income':'The respondents personal annual income', 'sex':''},
                   title = 'income vs. sex')
gss_p5.update(layout=dict(title=dict(x=0.5)))
gss_p5.update_layout(showlegend=False)


gss_p5 = px.box(gss_clean, y='job_prestige', x = 'sex', color = 'sex',
                   labels={'job_prestige':'The respondents occupational prestige score', 'sex':''},
                   title = 'job_prestige vs. sex')
gss_p5.update(layout=dict(title=dict(x=0.5)))
gss_p5.update_layout(showlegend=False)


mycols_p6 = ['income', 'sex', 'job_prestige']
gss_p6 = gss_clean[mycols_p6]

gss_p6['job_prestige_cut'] = pd.cut( x = gss_p6['job_prestige'], bins = [15, 26, 37, 48, 59, 70, 81], labels = ['A', 'B', 'C', 'D', 'E', 'F'])
gss_p6_cat = gss_p6.drop(['job_prestige'], axis = 1)
gss_p6_cat = gss_p6_cat.dropna()

gss_p6 = px.box(gss_p6_cat, y='income', x = 'job_prestige_cut', color = 'sex',
                   facet_col='job_prestige_cut',facet_col_wrap=2, 
                   labels={'job_prestige':'the respondents job prestige', 'income':'income'},
                   title = 'job prestige vs. income by sex', color_discrete_map = {'male':'blue', 'female':'red'})
gss_p6.update(layout=dict(title=dict(x=0.5)))
gss_p6.update_layout(showlegend=False)

mycol_ch2 = ['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork']
cat_columns3 = ['sex', 'region', 'education']
anes_ft2 = gss_clean[mycol_ch2 + cat_columns3].dropna()
anes_ft2['index_col'] = anes_ft2.index 

app = JupyterDash(__name__, external_stylesheets=external_stylesheets)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


table.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

gss_p3.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


app.layout = html.Div(
    [
        html.H1("Wage gap study"), 
        dcc.Markdown(
        style={"background-color": "yellow", "border": "solid 1px black"},
        children = markdown_text), 
        html.H2("Men and Women income study"),
        dcc.Graph(figure=table),
        html.H2("Gender Opionions on Male BreadWinner"),
        dcc.Graph(figure=gss_p3),
        html.H2("Gender Opinions on Relationship Between Job Prestige vs. Income"),
        dcc.Graph(figure=gss_p4),
        html.H2("Job Prestige vs. Sex"),
        dcc.Graph(figure=gss_p5),
        html.H2("Gender Opinions on Relationship Between Job Prestige vs. Income from Six Categories"),
        dcc.Graph(figure=gss_p6),
        
        html.Div([
            html.H3("x-axis feature"),
            dcc.Dropdown(id='x-axis',
                         options=[{'label': i, 'value': i} for i in mycol_ch2],
                     value='relationship'),
            html.H3("y-axis feature"),
            dcc.Dropdown(id='y-axis',
                         value='index_col'),
            html.H3("colors"),
            dcc.Dropdown(id='color',
                         options=[{'label': i, 'value': i} for i in cat_columns3],
                         value=None)], style={"width": "25%", "float": "left"}),
        
        html.Div([dcc.Graph(id="graph", style={"width": "70%", "display": "inline-block"})])
    
    ]
)
@app.callback(Output(component_id="graph",component_property="figure"), 
                  [Input(component_id='x-axis',component_property="value"),
                   Input(component_id='y-axis',component_property="value"),
                   Input(component_id='color',component_property="value")])

def make_figure(x, y, color):
    return px.bar(
        anes_ft2,
        x=x,
        y='index_col',
        color=color,
        height=700,
        opacity = 1
)



if __name__ == '__main__':
    app.run_server(debug = False)