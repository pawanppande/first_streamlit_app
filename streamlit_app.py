import streamlit

streamlit.title('My Parents New Healthy Dinner')

streamlit.subheader('Breakfast menu')

streamlit.text('🥣 omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, spinach & Rocket smoothie')
streamlit.text('🐔 Hard boiled free-range egg')
streamlit.text('🥑🍞Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
import pandas as pd 
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show  = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#New section to display fruitvice api response
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

import requests
import json
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
# streamlit.text(fruityvice_response.json())

# test = fruityvice_response
# # write your own comment
# fruityvice_normalized = pd.json_normalize(test.json())
# # write your own comment 
# streamlit.dataframe(fruityvice_normalized)

#The below is working 
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice) 
fruityvice_normalized = pd.json_normalize(fruityvice_response.json()) 
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_row)
