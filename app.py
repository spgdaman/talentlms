import talentlms
import streamlit as st
import pandas as pd
import numpy as np
from download import download_button
import datetime

x = datetime.datetime.now()

st.set_page_config(layout='wide')
 
# function to get unique values
def unique(list1):
    x = np.array(list1)
    return(np.unique(x))

@st.cache(suppress_st_warning=True)
def talent():
    API_KEY = 'TC7azJYg1UAcBMSvSiN4eEuldImd29'

    lms = talentlms.api('pendahealth.talentlms.com', API_KEY)
    courses = lms.courses(course_id=None)
    users = lms.users(search_term=None)
    users = pd.DataFrame(users)
    # st.write(users)
    users = users['custom_field_4'].unique()
    users = users.tolist()
    users.remove(None)
    # users = users[:20]
    # print(users)

    course_certification = []
    for user in users:
        custom_field = lms.get_users_by_custom_field(f"{user}")

        keys = []
        for value in custom_field:
            keys.append(value)

        for i in keys:
            id = custom_field[f"{i}"]['id']
            first_name = custom_field[f"{i}"]['first_name']
            last_name = custom_field[f"{i}"]['last_name']
            email = custom_field[f"{i}"]['email']
            certifications = custom_field[f"{i}"]['certifications']
            if len(certifications) >= 1:
                for value in certifications:
                    value.update({'user_id':id})
                    value.update({'first_name':first_name})
                    value.update({'last_name':last_name})
                    value.update({'email':email})
                    course_certification.append(value)

    # Courses taken by staff
    course_details = pd.DataFrame(course_certification)
    course_details['full_name'] = course_details['first_name'] + " " + course_details['last_name']

    return course_details

    # if type(user) and type(course) == 'str':
    #     user_course_status = lms.get_user_status_in_course(int(user),int(course))
    #     st.write(user_course_status)
    # user_course_status = lms.get_user_status_in_course(int(user),int(course))

    # users = course_details['tl_id'].tolist()
    # users = unique(users)
    # course_ids = course_details['course_id'].tolist()
    # course_ids = unique(course_ids)

    # units = []
    # for user in users:
    #     for course in course_ids:
    #         # Get user status in course and unit
    #         try:
    #             user_course_status = lms.get_user_status_in_course(int(user),int(course))
    #             # st.write(user_course_status)
    #             role = user_course_status.get('role')
    #             enrolled_on = user_course_status.get('enrolled_on')
    #             enrolled_on_timestamp = user_course_status.get('enrolled_on_timestamp')
    #             completion_status = user_course_status.get('completion_status')
    #             completion_percentage = user_course_status.get('completion_percentage')
    #             completed_on = user_course_status.get('completed_on')
    #             completed_on_timestamp = user_course_status.get('completed_on_timestamp')
    #             expired_on = user_course_status.get('expired_on')
    #             expired_on_timestamp = user_course_status.get('expired_on_timestamp')
    #             total_time = user_course_status.get('total_time')
    #             total_time_seconds = user_course_status.get('total_time_seconds')
    #             course_id = course

    #             progress = {}

    #             # progress.update({'user_id': user})
    #             progress.update({'course_id': course_id})
    #             progress.update({'role': role})
    #             progress.update({'enrolled_on': enrolled_on})
    #             # progress.update({'enrolled_on_timestamp': enrolled_on_timestamp})
    #             progress.update({'course_completion_status': completion_status})
    #             progress.update({'course_completion_percentage': completion_percentage})
    #             progress.update({'course_completed_on': completed_on})
    #             # progress.update({'course_completed_on_timestamp': completed_on_timestamp})
    #             progress.update({'course_expired_on': expired_on})
    #             # progress.update({'course_expired_on_timestamp': expired_on_timestamp})
    #             progress.update({'course_total_time': total_time})
    #             # progress.update({'course_total_time_seconds': total_time_seconds})

    #             units.append(progress)

    #             # units = user_course_status.get('units')
    #             # for i in units:
    #             #     i.update({'user_id': user})
    #             #     i.update({'role': role})
    #             #     i.update({'enrolled_on': enrolled_on})
    #             #     i.update({'enrolled_on_timestamp': enrolled_on_timestamp})
    #             #     i.update({'course_completion_status': completion_status})
    #             #     i.update({'course_completion_percentage': completion_percentage})
    #             #     i.update({'course_completed_on': completed_on})
    #             #     i.update({'course_completed_on_timestamp': completed_on_timestamp})
    #             #     i.update({'course_expired_on': expired_on})
    #             #     i.update({'course_expired_on_timestamp': expired_on_timestamp})
    #             #     i.update({'course_total_time': total_time})
    #             #     i.update({'course_total_time_seconds': total_time_seconds})
    #             #     units.append(i)

    #         except:
    #             pass
    
    # # Course completion status
    # units = pd.DataFrame(units)
    # units = pd.merge(
    #     units,
    #     course_details,
    #     left_on = 'course_id',
    #     right_on = 'course_id',
    #     how = 'left'
    # )
    # del units['email']
    # del units['public_url']
    # del units['download_url']
    # del units['unique_id']
    # column_names = [
    #     "tl_id",
    #     "course_id",
    #     "course_name",
    #     "first_name",
    #     "last_name",
    #     "enrolled_on",
    #     "course_completion_status",
    #     "course_completion_percentage",
    #     "course_completed_on",
    #     "course_total_time"
    # ]
    # units = units[column_names]

    # return course_details, units

talent()

data = talent()

# Filter by user
columns = ["course_name","full_name"]

for column in data.columns:
    if column in columns:
        options = pd.Series(["All"]).append(data[column], ignore_index=True).unique()
        choice = st.sidebar.selectbox("Select {}.".format(column), options)
        
        if choice != "All":
            data = data[data[column] == choice]
st.header("Courses enrolled by Staff")
st.dataframe(data)

download_button_str = download_button(data, f"Courses Enrolled {x}.csv", 'Download CSV', pickle_it=False)
st.markdown(download_button_str, unsafe_allow_html=True)

# filter course completion details
API_KEY = 'TC7azJYg1UAcBMSvSiN4eEuldImd29'
lms = talentlms.api('pendahealth.talentlms.com', API_KEY)

user = st.text_input("Enter user_id")
course = st.text_input("Enter course_id")

st.header("Course Units Completion Status")
if user or course != "":
    user_course_status = lms.get_user_status_in_course(int(user),int(course))
    units = user_course_status.get('units')
    units = pd.DataFrame(units)
    st.write(units)
    download_button_str = download_button(units, f"Course Units Completed {x}.csv", 'Download CSV', pickle_it=False)
    st.markdown(download_button_str, unsafe_allow_html=True)
else:
    st.warning("Please enter the user and course id of the staff")

# course_details, units = talent()

# course_name = pd.Series(["All"]).append(course_details["course_name"], ignore_index=True).unique()
# course_name_choice = st.selectbox('Select course:', course_name, key=1)
# if course_name_choice == "All":
#     st.title("Courses done by Staff")
#     st.write(course_details)
#     download_button_str = download_button(course_details, f"Courses done by Staff.csv", 'Download CSV', pickle_it=False)
#     st.markdown(download_button_str, unsafe_allow_html=True)
# elif course_name_choice != "All":
#     course_name_filter = course_details.loc[course_details['course_name'] == course_name_choice]
#     st.title("Courses done by Staff")
#     st.write(course_name_filter)
#     download_button_str = download_button(course_name_filter, f"Courses done by Staff.csv", 'Download CSV', pickle_it=False)
#     st.markdown(download_button_str, unsafe_allow_html=True)

# unit_name = pd.Series(["All"]).append(units["course_name"], ignore_index=True).unique()
# unit_name_choice = st.selectbox('Select course:', course_name, key=2)
# if unit_name_choice == "All":
#     st.title("Units Completion Status")
#     st.write(units)
#     download_button_str = download_button(units, f"Course Completion Status.csv", 'Download CSV', pickle_it=False)
#     st.markdown(download_button_str, unsafe_allow_html=True)
# elif unit_name_choice != "All":
#     unit_name_filter = units.loc[units['course_name'] == unit_name_choice]
#     st.title("Units Completion Status")
#     st.write(unit_name_filter)
#     download_button_str = download_button(unit_name_filter, f"Course Completion Status.csv", 'Download CSV', pickle_it=False)
#     st.markdown(download_button_str, unsafe_allow_html=True)