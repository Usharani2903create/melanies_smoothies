# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# Input for name on the smoothie
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Get Snowflake session and fruit options
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

# Multiselect for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# Build ingredients string
if ingredients_list:
    ingredients_string = ' '
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        # Display nutrition info for each selected fruit
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


    # Insert order into Snowflake
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                         VALUES ('{ingredients_string.strip()}', '{name_on_order}')"""
    # You would typically execute this statement using session.sql(my_insert_stmt).collect()
    # Button to submit the order
    time_to_insert = st.button('Submit Order')

# Execute the insert statement when button is clicked
    if time_to_insert:
       session.sql(my_insert_stmt).collect()

# Confirmation message
       st.success('Your Smoothie is ordered!', icon='✅')

       import requests
       
       #st.text(smoothiefroot_response.json())
       
       
        
   
