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

# Create a repeatable code
def get_fruitvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ this_fruit_choice) 
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json()) 
    return fruityvice_normalized

#New section to display fruitvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
          streamlit.error("Please select a fruit to get information.")
    else:
        back_from_function = get_fruitvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
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
streamlit.header("The fruit load list contains:")

# snowflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall()

# Add button to load the fruit
if streamlit.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

    


# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list")
# my_data_rows = my_cur.fetchall()
# streamlit.header("The fruit list contains:")
# streamlit.dataframe(my_data_rows)

# Allow end user to add fruit into the list 
def inser_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('" +"jackfruit"+"papaya"+"guava"+"kiwi"+"')")
        return "Thanks for adding "+ new_fruit
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)
added_fruit =  streamlit.write('Thanks for adding the',add_my_fruit)
#my_cur.execute("insert into fruit_load_list values('from streamlit')")

