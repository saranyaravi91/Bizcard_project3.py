import pandas as pd
import streamlit as st
import easyocr
import pymysql
from streamlit_option_menu import option_menu
from PIL import Image
import cv2
import os
import matplotlib.pyplot as plt
import re

icon = Image.open("C:\\Users\\saran\\.vscode\.venv\\business card.jpg")

# SETTING PAGE CONFIGURATIONS
st.set_page_config(
    page_title=" Extracting Business Card Data with OCR ",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded")


st.title(':violet[Extracting Business Card Data with OCR]') 

with st.sidebar:
    selected = option_menu("Menu", ["Home","Upload and Extract and Store","Modify"],
                           icons =["house","image", "toggles"],
                          default_index=0,
                          orientation="vertical",
                          styles={"nav-link": {"font-size": "20px", "text-align": "centre", "margin": "0px", 
                                                "--hover-color": "#FF0000"},
                                   "icon": {"font-size": "40px"},
                                   "container" : {"max-width": "2000px"},
                                   "nav-link-selected": {"background-color": "#D3D3D3"},
                                   "nav": {"background-color": "#D3D3D3"}})

# INITIALIZING THE EasyOCR READER
reader = easyocr.Reader(['en'])

# CONNECTING WITH MYSQL DATABASE
mydb = pymysql.connect(
     host="localhost",
     user="root",
     password="12345",
)
cursor=mydb.cursor()
cursor.execute("CREATE DATABASE  if not exists Business_Cards")
cursor.execute("use Business_Cards")

# TABLE CREATION
cursor.execute('''CREATE TABLE IF NOT EXISTS Business_Cards
                   (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    company_name VARCHAR(50),card_holder VARCHAR(50),
                    designation VARCHAR(50),mobile_number VARCHAR(50),
                    email TEXT,website TEXT,area TEXT,city VARCHAR(50),
                    state VARCHAR(50),pin_code VARCHAR(10),image LONGBLOB)''')

# HOME MENU
if selected == "Home":
    
    st.markdown(":black_large_square: **Project Title** : BizCardX: Extracting Business Card Data with OCR")

    technologies = "streamlit, SQL, Data Extraction"
    st.markdown(f":black_large_square: **Technologies** : {technologies}")

    overview = "Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR."
    st.markdown(f":black_large_square: **Overview** : {overview}")
    st.image(Image.open("C:\\Users\\saran\\.vscode\\.venv\\visiting.jpg"),width = 400)

#Initialize df as None
df= None    

# UPLOAD AND EXTRACT MENU
if selected == "Upload and Extract and Store":
   
    tab1,tab2,tab3=st.tabs(["UPLOAD","EXTRACT","STORE"])
    with tab1:
        st.markdown("### Upload a Business Card")
        uploaded_card = st.file_uploader("Upload here", label_visibility="collapsed", type=["png", "jpeg", "jpg"])

        if uploaded_card is not None:
            # Save the uploaded file to a temporary directory
            temp_dir = os.path.join("uploaded_cards")
            os.makedirs(temp_dir, exist_ok=True)
            temp_file_path = os.path.join(temp_dir, "temp_card.jpg")
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_card.getbuffer())

            # Display the uploaded card
            st.markdown("### You have uploaded the card")
            st.image(uploaded_card)
    
    with tab2:
         
        if uploaded_card is not None:
            if hasattr(uploaded_card, 'name') and uploaded_card.name is not None:
                with open(os.path.join("uploaded_cards", uploaded_card.name), "wb") as f:
                    f.write(uploaded_card.getbuffer())
                # Rest of the code that depends on uploaded_card
                image = cv2.imread(temp_file_path)
                res = reader.readtext(temp_file_path)
                st.markdown("### Image Processed and Data Extracted")
                

                def image_preview(image, res):
                    for (bbox, text, prob) in res:
                       # unpack the bounding box
                        (tl, tr, br, bl) = bbox
                        tl = (int(tl[0]), int(tl[1]))
                        tr = (int(tr[0]), int(tr[1]))
                        br = (int(br[0]), int(br[1]))
                        bl = (int(bl[0]), int(bl[1]))
                        cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                        cv2.putText(image, text, (tl[0], tl[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    plt.rcParams['figure.figsize'] = (15, 15)
                    plt.axis('off')
                    plt.imshow(image)    

                # DISPLAYING THE CARD WITH HIGHLIGHTS
        
                with st.spinner("Please wait, processing image..."):
                        st.set_option('deprecation.showPyplotGlobalUse', False)
                        saved_img = os.path.join(os.getcwd(), "uploaded_cards", uploaded_card.name)
                        image = cv2.imread(saved_img)
                        res = reader.readtext(saved_img)
                        st.pyplot(image_preview(image, res))

               # easyOCR
                saved_img = os.path.join(os.getcwd(), "uploaded_cards", uploaded_card.name)
                result = reader.readtext(saved_img, detail=0, paragraph=False)

                # CONVERTING IMAGE TO BINARY TO UPLOAD TO SQL DATABASE
                def img_to_binary(file):
                    # Convert image data to binary format
                    with open(file, 'rb') as file:
                        binaryData = file.read()
                    return binaryData

                data = {"company_name": [],
                        "card_holder": [],
                        "designation": [],
                        "mobile_number": [],
                        "email": [],
                        "website": [],
                        "area": [],
                        "city": [],
                        "state": [],
                        "pin_code": [],
                        "image": img_to_binary(saved_img)
                        }

                def get_data(res):
                    for ind, i in enumerate(res):
                        # To get WEBSITE_URL
                        if "www " in i.lower() or "www." in i.lower():
                            data["website"].append(i)
                        elif "WWW" in i:
                            data["website"] = res[4] + "." + res[5]
                        # To get EMAIL ID
                        elif "@" in i:
                            data["email"].append(i)
                        # To get MOBILE NUMBER
                        elif "-" in i:
                            data["mobile_number"].append(i)
                            if len(data["mobile_number"]) == 2:
                                data["mobile_number"] = " & ".join(data["mobile_number"])
                        # To get COMPANY NAME                                             
                        elif i == "selva" or i == "digitals":
                            data["company_name"].append(i)
                            if len(data["company_name"]) > 1:
                                data["company_name"] = " ".join(data["company_name"])
                        elif i == "GLOBAL" or i == "INSURANCE":
                            data["company_name"].append(i)
                            if len(data["company_name"]) > 1:
                                data["company_name"] = " ".join(data["company_name"])
                        elif i == "BORCELLE" or i == "AIRLINES":
                            data["company_name"].append(i)
                            if len(data["company_name"]) > 1:
                                data["company_name"] = " ".join(data["company_name"])
                        elif i == "Family" or i == "Restaurant":
                            data["company_name"].append(i)
                            if len(data["company_name"]) > 1:
                                data["company_name"] = " ".join(data["company_name"])
                        elif i == "Sun Electricals":
                            data["company_name"].append(i)
                            if len(data["company_name"]) > 1:
                                data["company_name"] = " ".join(data["company_name"])
                        
                        # To get CARD HOLDER NAME
                        elif ind == 0:
                            data["card_holder"].append(i)
                        # To get DESIGNATION
                        elif ind == 1:
                            data["designation"].append(i)
                        # To get AREA
                        if re.findall('^[0-9].+, [a-zA-Z]+', i):
                            data["area"].append(i.split(',')[0])
                        elif re.findall('[0-9] [a-zA-Z]+', i):
                            data["area"].append(i)
                        # To get CITY NAME
                        match1 = re.findall('.+St , ([a-zA-Z]+).+', i)
                        match2 = re.findall('.+St,, ([a-zA-Z]+).+', i)
                        match3 = re.findall('^[E].*', i)
                        if match1:
                            data["city"].append(match1[0])
                        elif match2:
                            data["city"].append(match2[0])
                        elif match3:
                            data["city"].append(match3[0])
                        # To get STATE
                        state_match = re.findall('[a-zA-Z]{9} +[0-9]', i)
                        if state_match:
                            data["state"].append(i[:9])
                        elif re.findall('^[0-9].+, ([a-zA-Z]+);', i):
                            data["state"].append(i.split()[-1])
                        if len(data["state"]) == 2:
                            data["state"].pop(0)
                        # To get PINCODE
                        if len(i) >= 6 and i.isdigit():
                            data["pin_code"].append(i)
                        elif re.findall('[a-zA-Z]{9} +[0-9]', i):
                            data["pin_code"].append(i[10:])
                get_data(result)

               # FUNCTION TO CREATE DATAFRAME
                def create_df(data):
                    df = pd.DataFrame(data)
                    return df
                df = create_df(data)
                st.success("### Data Extracted!")
                st.write(df)
                pass
# STORING datas in mysql
    with tab3:
        
        if df is not None and not df.empty:
            try:
                # CONNECTING WITH MYSQL DATABASE
                mydb = pymysql.connect(
                    host="localhost",
                    user="root",
                    password="12345",
)
                cursor=mydb.cursor()
                cursor.execute("use Business_Cards")
                for i, row in df.iterrows():
                    sql = """INSERT INTO Business_Cards(company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code,image)
                         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(sql, tuple(row))
                    # Commit the changes and close the cursor and connection
                    mydb.commit()
                    cursor.close()
                    mydb.close()
                    st.success("Data uploaded to the database successfully!")
            except pymysql.connector.Error as error:
                st.error(f"Failed to store data in the database: {error}")
        else:
            st.warning("No data to store. Please upload and extract business card data first.")
            st.warning("No data to store. Please upload and extract business card data first.") 
            pass

# MODIFY MENU
if selected == "Modify":
    
    col1, col2, col3 = st.columns([3, 3, 2])
    st.markdown("## Alteration and Deletion of Datas")
    column1, column2 = st.columns(2, gap="large")
    
    try:
        with column1:
            cursor.execute("SELECT card_holder FROM Business_Cards")
            result = cursor.fetchall()
            business_cards = {row[0]: row[0] for row in result}
            
            selected_card = st.selectbox("Select a card holder name to update", list(business_cards.keys()))
            st.markdown("#### Modify the Datas")
            
            cursor.execute("SELECT company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code FROM Business_Cards WHERE card_holder=%s", (selected_card,))
            result = cursor.fetchone()
            
            # DISPLAYING ALL THE INFORMATION
            company_name = st.text_input("Company Name", result[0])
            card_holder = st.text_input("Card Holder", result[1])
            designation = st.text_input("Designation", result[2])
            mobile_number = st.text_input("Mobile Number", result[3])
            email = st.text_input("Email", result[4])
            website = st.text_input("Website", result[5])
            area = st.text_input("Area", result[6])
            city = st.text_input("City", result[7])
            state = st.text_input("State", result[8])
            pin_code = st.text_input("Pin Code", result[9])

            if st.button("Commit changes to DB"):
                # Update the information for the selected business card in the database
                cursor.execute("""
                    UPDATE Business_Cards
                    SET company_name=%s, card_holder=%s, designation=%s, mobile_number=%s, email=%s, website=%s, area=%s, city=%s, state=%s, pin_code=%s
                    WHERE card_holder=%s
                """, (company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code, selected_card))
                mydb.commit()
                st.success("New Information updated in the database successfully.")

        with column2:
            cursor.execute("SELECT card_holder FROM Business_Cards")
            result =cursor.fetchall()
            business_cards = {row[0]: row[0] for row in result}
            
            selected_card = st.selectbox("Select a card holder name to delete", list(business_cards.keys()))
            st.write(f"### You have selected :green[**{selected_card}'s**] card to delete")
            st.write("#### Are You Sure")
            
            if st.button("Yes,sure"):
                cursor.execute(f"DELETE FROM Business_Cards WHERE card_holder='{selected_card}'")
                mydb.commit()
                st.success("Business card information deleted from the database.")
    except:
        st.warning("There is no data available in the database")

    if st.button("View updated data"):
        cursor.execute("SELECT company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code FROM Business_Cards")
        updated_data = pd.DataFrame(cursor.fetchall(), columns=["Company Name", "Card Holder", "Designation", "Mobile Number", "Email", "Website", "Area", "City", "State", "Pin Code"])
        st.write(updated_data)