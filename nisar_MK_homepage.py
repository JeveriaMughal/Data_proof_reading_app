import streamlit as st
import nisar_MK,revision_phase1

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
def app():
    local_css("style.css")
    file1=open("master_data/MC_ENG_NMK.txt","r")
    corpus=file1.readlines()
    # file2=open("master_data/official-terms.ur","r")
    # glossary=file2.readlines()
    column1,column2,column3=st.columns(3)
    with column1:
        st.metric(label="Programmer, NLPD", value="Nisar Mamakhel", delta="Phase I Reviewer", delta_color="normal", help=None)
    with column2:
        st.metric(label="Assigned Data Sets", value="1", delta="CORPUS", delta_color="normal", help=None)
    with column3:
        st.metric(label="Assigned Lines", value=str(len(corpus)), delta=None, delta_color="normal", help=None)
    

    col1,col2,col3=st.columns([2,2,1])
    with col3:
        # selection=st.radio("DATA SET",["GLOSSARY","CORPUS"])
        revise=st.checkbox("revise your work")
    
    # if selection == "CORPUS":
    #     rauf_parekh.app()
    # if selection == "GLOSSARY":
    #     rauf_parekh_glossary.app()

    if revise:
        revision_phase1.app_nisar()
    else:
        nisar_MK.app()
