import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import openai
import time
# from openai import OpenAI
from datetime import datetime, timedelta

# Page title
st.set_page_config(page_title='Easy Refactor Code', page_icon='🎫')
st.title('Easy Refactor Code')
st.info('To refactor traditional html/css/js login page code, fill out the form below.')


# Generate data
## Set seed for reproducibility
np.random.seed(42)

## Function to generate a random issue description
def generate_issue():
    issues = [
        "Network connectivity issues in the office",
        "Software application crashing on startup",
        "Printer not responding to print commands",
        "Email server downtime",
        "Data backup failure",
        "Login authentication problems",
        "Website performance degradation",
        "Security vulnerability identified",
        "Hardware malfunction in the server room",
        "Employee unable to access shared files",
        "Database connection failure",
        "Mobile application not syncing data",
        "VoIP phone system issues",
        "VPN connection problems for remote employees",
        "System updates causing compatibility issues",
        "File server running out of storage space",
        "Intrusion detection system alerts",
        "Inventory management system errors",
        "Customer data not loading in CRM",
        "Collaboration tool not sending notifications"
    ]
    return np.random.choice(issues)

## Function to generate random dates
start_date = datetime(2023, 6, 1)
end_date = datetime(2023, 12, 20)
id_values = ['TICKET-{}'.format(i) for i in range(1000, 1100)]
issue_list = [generate_issue() for _ in range(100)]


def generate_random_dates(start_date, end_date, id_values):
    date_range = pd.date_range(start_date, end_date).strftime('%m-%d-%Y')
    return np.random.choice(date_range, size=len(id_values), replace=False)

## Generate 100 rows of data
data = {'Issue': issue_list,
        'Status': np.random.choice(['Open', 'In Progress', 'Closed'], size=100),
        'Priority': np.random.choice(['High', 'Medium', 'Low'], size=100),
        'Date Submitted': generate_random_dates(start_date, end_date, id_values)
    }
df = pd.DataFrame(data)
df.insert(0, 'ID', id_values)
df = df.sort_values(by=['Status', 'ID'], ascending=[False, False])

## Create DataFrame
if 'df' not in st.session_state:
    st.session_state.df = df

def refactorCode(input_html, input_css, input_js):
    # output_html = "testhtml"
    # output_css = "testcss"
    # output_js = "testjs"
    output_html = open("new-static/login-page.html").read()
    output_css = open("new-static/login-page.css").read()
    output_js = open("new-static/slogin-page.js").read()
    
    return output_html, output_css, output_js
    
    
    




# Tabs for app layout
tabs = st.tabs(['Submit Code', 'Submit DB'])

recent_ticket_number = int(max(st.session_state.df.ID).split('-')[1])

with tabs[0]:
  with st.form('Code'):
    html = st.text_area('HTML Code')
    css = st.text_area('CSS Code')
    js = st.text_area('JS Code')
    # priority = st.selectbox('Priority', ['High', 'Medium', 'Low'])
    submit = st.form_submit_button('Submit')

  if submit:
      today_date = datetime.now().strftime('%m-%d-%Y')
      outputs = refactorCode(html, css, js)
      df2 = pd.DataFrame([{'ID': f'TICKET-{recent_ticket_number+1}',
                           'HTML': outputs[0],
                           'CSS': outputs[1],
                            'JS': outputs[2],
                           'Date Submitted': today_date
                          }])
      st.write('Request submitted!')
      time.sleep(5)
      st.dataframe(df2, use_container_width=True, hide_index=True)
      st.session_state.df = pd.concat([st.session_state.df, df2], axis=0).sort_values(by=['Status', 'ID'], ascending=[False, False])

with tabs[1]:
  with st.form('DB'):
    originalDB = st.text_area('DB')
    # priority = st.selectbox('Priority', ['High', 'Medium', 'Low'])
    submit = st.form_submit_button('Submit')

  if submit:
      today_date = datetime.now().strftime('%m-%d-%Y')
      df2 = pd.DataFrame([{'ID': f'TICKET-{recent_ticket_number+1}',
                           'Original DB': originalDB,
                           'Date Submitted': today_date
                          }])
      st.write('Request submitted!')
      st.dataframe(df2, use_container_width=True, hide_index=True)
      st.session_state.df = pd.concat([st.session_state.df, df2], axis=0).sort_values(by=['Status', 'ID'], ascending=[False, False])
      
      
