import streamlit as st
import base64
from io import BytesIO
from PIL import Image
from supabase import create_client, Client

url = "https://oapcmcmjmpwtujvlsmsb.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9hcGNtY21qbXB3dHVqdmxzbXNiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjUzNjczMjMsImV4cCI6MjA0MDk0MzMyM30.49kGv7qHG8tdAr-Hreox0o4wK8LdkgmlHxbiVTVPVt8"  # Replace with your Supabase API key
supabase: Client = create_client(url, key)
st.title("Feedback Page")

def image_to_base64(image_file):
    buffered = BytesIO()
    image_file.seek(0)
    buffered.write(image_file.read())
    encoded_string = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return encoded_string

def base64_to_image(base64_str):
    image_data = base64.b64decode(base64_str)
    image = Image.open(BytesIO(image_data))
    return image

def handle_images(images):
    image_base64_list = []
    for image in images:
        buffered = BytesIO()
        image.seek(0)
        buffered.write(image.read())
        encoded_string = base64.b64encode(buffered.getvalue()).decode('utf-8')
        image_base64_list.append(encoded_string)
    return image_base64_list

type = st.radio("Type", options=["Feedback", "Painpoint"], horizontal=True, label_visibility="hidden")
has_submitted = False
if type == "Feedback":
    col3, col4 = st.columns(2)
    with col3:
        name = st.text_input("Enter Your name", placeholder="Name", label_visibility="collapsed")
    with col4:
        email = st.text_input("Enter your email", placeholder="Email", label_visibility="collapsed", autocomplete="@finanshels.com")

    st.write("Select an issue")
    feedback_type = st.multiselect(
        "Issue type",
        [
            "Task Prioritization Problems",
            "Notification Issues",
            "User Interface Concerns",
            "Synchronization Errors",
            "Performance Problems",
            "Task Management Features",
            "Search and Filtering Problems",
            "Onboarding and Help Resources",
            "Security Concerns",
            "Others"
        ],
        label_visibility="hidden"
    )

    feedback_description = st.text_area("Description", placeholder="Describe your issue", height=170, label_visibility="hidden")
    has_image = st.checkbox("Do you have screenshot")
    if has_image:
        images = st.file_uploader("Upload screenshots", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    if st.button("Submit Feedback"):
        image_base64_list = handle_images(images) if images else None
        feedback_data = {
            'type': 'Feedback',
            'name': name,
            'email': email,
            'issue_type': ', '.join(feedback_type),
            'description': feedback_description,
            'has_screenshot': bool(images),
            'screenshot_base64': image_base64_list
        }
        try:
            response = supabase.table('feedback').insert(feedback_data).execute()
            if response.data:
                st.success("Feedback submitted successfully!")
                has_submitted = True
            else:
                st.error("Failed to submit feedback.")
                st.write("Response data:", response)
        except Exception as e:
            st.error(f"An error occurred while submitting feedback: {str(e)}")

elif type == "Painpoint":
    st.write("Describe your pain point")
    painpoint_description = st.text_area("Description", placeholder="Describe your pain point", height=250, label_visibility="hidden")
    images = st.file_uploader("Upload screenshots", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    if st.button("Submit Pain Point"):
        image_base64_list = handle_images(images) if images else None
        painpoint_data = {
            'type': 'Painpoint',
            'description': painpoint_description,
            'has_screenshot': bool(images),
            'screenshot_base64': image_base64_list
        }
        try:
            response = supabase.table('feedback').insert(painpoint_data).execute()
            if response.data:
                st.success("Pain point submitted successfully!")
            else:
                st.error("Failed to submit pain point.")
                st.write("Response data:", response)
        except Exception as e:
            st.error(f"An error occurred while submitting pain point: {str(e)}")

if email:
    try:
        past_entries_response = supabase.table('feedback').select('*').eq('email', email).execute()
        if past_entries_response.data:
            st.subheader("Your Past Entries:")
            for entry in past_entries_response.data:
                col5, col6 = st.columns(2)
                with col5:
                    st.write(f"**ID:** {entry['id']}")
                    st.write(f"**Type:** {entry['type']}")
                    st.write(f"**Issue Type:** {entry.get('issue_type', 'N/A')}")
                    st.write(f"**Description:** {entry['description']}")
                with col6:
                    if entry['has_screenshot'] and entry.get('screenshot_base64'):
                        st.write("**Screenshots:**")
                        for screenshot_base64 in entry['screenshot_base64']:
                            image = base64_to_image(screenshot_base64)
                            st.image(image, caption='Uploaded Screenshot')
                st.write("---")
        else:
            st.write("No past entries found.")
    except Exception as e:
        st.error(f"An error occurred while fetching past entries: {str(e)}")
