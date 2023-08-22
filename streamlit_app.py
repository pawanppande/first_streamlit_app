import streamlit
import pandas as pd 
import requests
import json
import snowflake.connector
from urllib.error import URLError
streamlit.title('My Parents New Healthy Dinner')

streamlit.subheader('Breakfast menu')

streamlit.text('🥣 omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, spinach & Rocket smoothie')
streamlit.text('🐔 Hard boiled free-range egg')
streamlit.text('🥑🍞Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
#import pandas as pd
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show  = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#New section to display fruitvice api response

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
  else:
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice) 
      fruityvice_normalized = pd.json_normalize(fruityvice_response.json()) 
      streamlit.dataframe(fruityvice_normalized)
    #streamlit.write('The user entered ', fruit_choice)
except URLError as e:
    streamlit.error()

#import request 
#Import json
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
# streamlit.text(fruityvice_response.json())

# test = fruityvice_response
# # write your own comment
# fruityvice_normalized = pd.json_normalize(test.json())
# # write your own comment 
# streamlit.dataframe(fruityvice_normalized)

#The below is working

# Don'r run anything here while we troubleshoot
streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit list contains:")
streamlit.dataframe(my_data_rows)

# Allow end user to add fruit into the list 
add_my_fruit = streamlit.text_input('What fruit would you like information about?','jackfruit')
added_fruit =  streamlit.write('Thanks for adding the',add_my_fruit)
my_cur.execute("insert into fruit_load_list values('from streamlit')")
