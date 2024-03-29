import streamlit as st
import SM_page1,revision_SM

def app():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
    "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    file2=open("master_data/MC_URDU_SM.txt","r")
    glossary=file2.readlines()
    column1,column2,column3=st.columns(3)
    with column1:
        st.metric(label="Director General NLPD / Project Director NLP-Lab", value="Prof. Dr. Mohd Saleem Mazhar", delta="Language Expert", delta_color="normal", help=None)
    with column2:
        st.metric(label="Assigned Data Sets", value="1", delta="Glossary", delta_color="normal", help=None)
    with column3:
        st.metric(label="Assigned Lines", value="Glossary:"+ str(len(glossary)), delta=None, delta_color="normal", help=None)
    
    
    col1,col2,col3=st.columns([2,2,1])
    with col3:
        revise=st.checkbox("Revise your work")
    if revise:
        revision_SM.app_glossary()  
    else:
        SM_page1.app()

        