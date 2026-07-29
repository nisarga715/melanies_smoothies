import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# --- Page setup ---
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# --- Get the active Snowpark session ---
cnx = st.connection("snowflake")
session = cnx.session()

# --- Name on the order ---
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)

# --- Pull available fruit options ---
my_dataframe = session.table(
    "smoothies.public.fruit_options"
).select(col("FRUIT_NAME"))

# --- Ingredient picker ---
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list:

    # Build ingredient string
    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

    # Display nutrition information (Watermelon example)
    smoothiefroot_response = requests.get(
        "https://my.smoothiefroot.com/api/fruit/watermelon"
    )

    st.dataframe(
        data=pd.json_normalize(smoothiefroot_response.json()),
        use_container_width=True
    )

    # Submit Order button
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """

        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")
