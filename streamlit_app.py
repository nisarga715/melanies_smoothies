import streamlit as st
from snowflake.snowpark.functions import col


# --- Page setup ---
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# --- Get the active Snowpark session (works when run inside Streamlit in Snowflake) ---
cnx = st.connection("snowflake")
session = cnx.session()

# --- Name on the order ---
name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be:', name_on_order)

# --- Pull available fruit options from a table (adjust table/column names to your schema) ---
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# --- Ingredient picker, capped at 5 like the screenshot ---
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    # Build a single string of ingredients, e.g. "Elderberries Ximenia Ziziphus Jujube Tangerine "
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        # This matches the INSERT shown in the worksheet in your screenshot
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

# New section
import requests

smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)

st.json(smoothiefroot_response.json())



























