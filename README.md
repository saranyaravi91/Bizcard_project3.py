# [Project 3: Extracting Business Card Data with OCR](https://github.com/saranyaravi91/Bizcard_project3)
## Overview:
   This portfolio project aims to build a Streamlit web application that allows users to upload images of business cards, extract relevant information using OCR (Optical 
   Character Recognition), and store the extracted data in a MySQL database.
## Technologies Used:
   * Streamlit: For building the user interface and web application.
   * EasyOCR: To perform Optical Character Recognition on business card images.
   * MySQL: As the database to store the extracted business card data.
   * Pandas: For data manipulation and handling the extracted data in a DataFrame.
   * Matplotlib: For image processing and displaying the uploaded business card with highlighted text.
   * OpenCV: To process and manipulate images.
## Steps:
## Setting Page Configurations: 
   Configuring Streamlit's page settings, including title, icon, layout, and sidebar options.
## Option Menus:
   * Creating a sidebar with options for the Home, Upload and Extract, and Modify sections.
## Home Section:
   * Displaying an overview of the project, including project title, technologies used, and a brief project description.
## Upload and Extract Section:
   * Allowing users to upload an image of a business card.
   * Using the EasyOCR library to extract text data from the uploaded image.
   * Displaying the uploaded image with highlighted text using OpenCV and Matplotlib.
   * Extracting relevant information from the extracted text, such as company name, card holder name, designation, mobile number, email, website, area, city, state, and 
     pin code.
   * Storing the extracted data in a Pandas DataFrame.
## Store Section:
   * Connecting to a MySQL database using the mysql.connector library.
   * Creating a table named "Business_Cards" if it doesn't exist to store the extracted business card data.
   * Storing the data from the Pandas DataFrame into the MySQL database.
## Modify Section:
   * Providing options to update and delete existing data in the database.
   * Displaying a dropdown to select the card holder name to update.
   * Allowing users to modify the data for the selected business card and committing the changes to the database.
   * Displaying a dropdown to select the card holder name to delete.
   * Confirming the deletion of the selected card and deleting the data from the database.
## Technologies Used:
   * Streamlit: For building the user interface and web application.
   * EasyOCR: To perform Optical Character Recognition on business card images.
   * MySQL: As the database to store the extracted business card data.
   * Pandas: For data manipulation and handling the extracted data in a DataFrame.
   * Matplotlib: For image processing and displaying the uploaded business card with highlighted text.
   * OpenCV: To process and manipulate images.
## Future Enhancement:
   * User Authentication: Implement user authentication and user accounts to allow multiple users to access the application securely. 
   * Improved OCR Accuracy: Explore and experiment with other OCR libraries or models to improve the accuracy of text extraction from business card images.
