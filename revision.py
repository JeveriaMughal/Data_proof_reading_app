import streamlit as st
import pandas as pd
import datetime
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
def sentence_form(lines_done,df):
    local_css("style.css")
    # file1=open("master_data/MC_ENG.txt","r")
    english=df["ENG"].values.tolist()
    # file2=open("master_data/MC_URDU.txt","r")
    urdu=df["URDU"].values.tolist()
    status_all=df["status"].values.tolist()
    st.write("lines number = ",lines_done)
    if lines_done < 0 :
        st.success("you have revised all the existing data allocated to you")
        data =pd.DataFrame()
    else:
        default=""
        col1,col2=st.columns(2)
        with col1:
            st.write("English")
            st.title(english[lines_done])
            correction_eng=st.text_input("Change sentence",value=default)
        with col2:
            st.write("اردو")
            # st.title(urdu[lines_done])
            st.markdown('<h1 class="urdu-font-big">'+urdu[lines_done]+'</h1>', unsafe_allow_html=True)
            correction_urdu=st.text_input("جملہ تبدیل کریں",value=default)
        comment=st.text_input("comment",value=default)
        date = datetime.date.today()
        if correction_eng != "" or correction_urdu != "":
            status="REVISED"
        else:
            status=status_all[lines_done]
        if correction_urdu=="":
            translation=urdu[lines_done]
        else:
            translation=correction_urdu
        if correction_eng == "":
            english_line = english[lines_done]
        else:
            english_line = correction_eng
        data=pd.DataFrame({'index':[lines_done],'ENG':[english_line],'URDU': [translation],'status':[status],'comment':[comment],'date':[date]})
    return data
    
def app():
    if 'num' not in st.session_state:
        st.session_state.num = 1
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
		"https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    # Assign credentials ann path of style sheet
    creds = ServiceAccountCredentials.from_json_keyfile_name("blank-test-363706-5265bab97753.json", scope)
    client = gspread.authorize(creds)
    file1=open("master_data/MC_ENG.txt","r")
    english=file1.readlines()
    if 'num' not in st.session_state:
        st.session_state.num = 1
    local_css("style.css")
    column1,column2,column3=st.columns(3)
    with column1:
        st.metric(label="Principle Investigator (NLP-LAB)", value="Mehboob Bugti", delta=None, delta_color="normal", help=None)
    with column2:
        st.metric(label="Assigned Data Sets", value="1", delta="CORPUS", delta_color="normal", help=None)
    with column3:
        st.metric(label="Assigned Lines", value=len(english), delta=None, delta_color="normal", help=None)
    st.write("CORPUS REVIEW")
    sheet = client.open("modified_data").get_worksheet(5)
    df = pd.DataFrame(sheet.get_all_records(),index=None)
    lines_done=(len(df.index))
    line_number=st.selectbox("choose index",df["index"].values.tolist())
    placeholder = st.empty()
    placeholder2 = st.empty()
    while True:    
        num = st.session_state.num

        if placeholder2.button('end', key=num):
            placeholder2.empty()
            break
        else:        
            with placeholder.form(key=str(num)):
                # df=pd.DataFrame(columns=['index','ENG', 'URDU','status','comment','date'])
                # data=pd.read_csv("modified_data/dania.csv")
                # df=pd.concat([df,data],ignore_index = True, axis = 0)
                st.write(df)
                data=sentence_form(line_number,df)
                

                if st.form_submit_button('OK'):  
                    df.at[line_number,'index']=data.at[0,'index']
                    df.at[line_number,'ENG']=data.at[0,'ENG']
                    df.at[line_number,'URDU']=data.at[0,'URDU']
                    df.at[line_number,'status']= data.at[0,'status']
                    df.at[line_number,'comment']=data.at[0,'comment']
                    df.at[line_number,'date']=data.at[0,'date']

                  
                    
                    sheet.clear()
                    set_with_dataframe(worksheet=sheet, dataframe=df, include_index=False,include_column_header=True, resize=True)
                    st.session_state.num += 1
                    placeholder.empty()
                    placeholder2.empty()

                
                else:
                    st.stop()
