import streamlit as st
from datetime import datetime, timedelta
import calendar
import pandas as pd

def recurring_task():
    genre = st.radio("Select your choice", options=["Once", "Repeating", "Never"], index=2, horizontal=True)
    result = None
    
    if genre == "Once":
        once_date = st.date_input("From Date", min_value=datetime.now().date(), value=None)
        if once_date:
            formatted_date = once_date.strftime('%d %b %y')
            st.write(f"You will get a notification on {formatted_date}")
            result = {"type": "Once", "date": once_date}
    
    elif genre == "Repeating":
        col1, col2 = st.columns(2)
        with col1:
            from_date = st.date_input("From Date", min_value=datetime.now().date(), value=None)
        with col2:
            to_date = st.date_input("To Date", min_value=datetime.now().date(), value=None)
        
        if from_date and to_date:
            if from_date > to_date:
                st.error("Error: 'To Date' must fall after 'From Date'.")
            else:
                option = st.selectbox("Recurring type", ("", "Daily", "Weekly", "Monthly", "Quarterly"), index=0)
                if not option:
                    st.stop()
                
                def generate_dates(from_date, to_date, option):
                    dates = []
                    current_date = from_date
                    while current_date <= to_date and len(dates) < 20:
                        if option == "Daily":
                            if current_date.weekday() in selected_days.values():
                                dates.append(current_date)
                        elif option == "Weekly":
                            dates.append(current_date)
                            current_date += timedelta(weeks=1)
                        elif option == "Monthly":
                            dates.append(current_date)
                            current_date += timedelta(days=30)
                        elif option == "Quarterly":
                            dates.append(current_date)
                            current_date += timedelta(days=90)
                        current_date += timedelta(days=1)
                    return dates
                result_dates=[]
                selected_days = {}
                if option == "Daily":
                    col3, col4, col5, col6, col7, col8, col9 = st.columns(7)
                    with col3:
                        sunday = st.checkbox('SU')
                    with col4:
                        monday = st.checkbox('MO')
                    with col5:
                        tuesday = st.checkbox('TU')
                    with col6:
                        wednesday = st.checkbox('WE')
                    with col7:
                        thursday = st.checkbox('TH')
                    with col8:
                        friday = st.checkbox('FR')
                    with col9:
                        saturday = st.checkbox('SA')
                    if sunday:
                        selected_days['Sunday'] = 0
                    if monday:
                        selected_days['Monday'] = 1
                    if tuesday:
                        selected_days['Tuesday'] = 2
                    if wednesday:
                        selected_days['Wednesday'] = 3
                    if thursday:
                        selected_days['Thursday'] = 4
                    if friday:
                        selected_days['Friday'] = 5
                    if saturday:
                        selected_days['Saturday'] = 6
                    while from_date <= to_date and len(result_dates) < 20:
                        if from_date.weekday() in selected_days.values():
                            result_dates.append(from_date)
                        from_date += timedelta(days=1)
                    
                    result = {"type": "Daily", "from_date": from_date, "to_date": to_date, "dates": result_dates}

                elif option in ["Weekly", "Monthly", "Quarterly"]:
                    result_dates = generate_dates(from_date, to_date, option)
                    result = {"type": option, "from_date": from_date, "to_date": to_date, "dates": result_dates}
    
    elif genre == "Never":
        st.write("You have chosen not to receive notifications.")
        result = {"type": "Never"}
    
    return result

def print_dates(dates):
    max_columns = 10
    num_dates = len(dates)
    num_rows = (num_dates + max_columns - 1) // max_columns

    for row in range(num_rows):
        with st.container():
            cols = st.columns(max_columns)
            for col in range(max_columns):
                index = row * max_columns + col
                if index < num_dates:
                    formatted_date = dates[index].strftime('%d %b %y')
                    with cols[col]:
                        st.write(formatted_date)
                else:
                    with cols[col]:
                        st.write('')
def to_df(dates):
    lis_to_df=[]
    for i in range(len(dates)):
        lis_to_df.append(dates[i].strftime('%d %b %y'))
    dates_df=pd.DataFrame(lis_to_df)
    return dates_df    


def main():
    result = recurring_task()
    if result:
        notification_type = result.get("type", "Not set")
        from_date = result.get("from_date", None)
        to_date = result.get("to_date", None)
        dates = result.get("dates", None)
        if notification_type == "Once":
            st.success(f"Notification will be sent on {result.get('date').strftime('%d %b %y')}")
        elif notification_type in ["Daily", "Weekly", "Monthly", "Quarterly"]:
            st.success(f"{notification_type} notifications set from {from_date.strftime('%d %b %y')} to {to_date.strftime('%d %b %y')}")
            if dates:
                st.write(f"Dates between {from_date.strftime('%d %b %y')} and {to_date.strftime('%d %b %y')}:")
                print_dates(dates)
                dates_df = to_df(dates)
                st.write(dates_df)
        elif notification_type == "Never":
            st.success("You have chosen not to receive notifications.")
        else:
            st.error("Invalid selection or no selection made.")
    else:
        st.info("No notification settings made.")

if __name__ == "__main__":
    main()
