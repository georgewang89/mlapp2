import requests
from pandas.io.json import json_normalize
import streamlit as st
from PIL import Image
import json

# for communication with AWS S3
import boto3

BUCKET_NAME = 'gwherokubucket'

# ================================================== streamlit ================================================== #

# ----- upload file via streamlit and save to folder directory ----- #

FOLDER = './images'
FILENAME = 'upload.jpg'
uploaded_file = st.file_uploader("Choose a jpg file", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    data = Image.open(uploaded_file)
    data.save(FOLDER+'/'+FILENAME)


def upload_s3(bucket_name, folder, filename):

    # Create an S3 client
    s3 = boto3.client('s3')

    # Uploads the given file using a managed uploader, which will split up large
    # files automatically and upload parts in parallel.
    s3.upload_file(folder + '/'+ filename, bucket_name, filename)

    # ----- get URL from s3 ----- #
    location = boto3.client('s3').get_bucket_location(Bucket=bucket_name)['LocationConstraint']
    aws_url = "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, filename)

    return aws_url

# ================================================== streamlit butt ================================================== #
if st.button("classify"):
    url = upload_s3(BUCKET_NAME, FOLDER, FILENAME)
    post_data = {"filename": FILENAME, "bucket": BUCKET_NAME}
    response = requests.post("{}/".format("http://127.0.0.1:5000"), json =post_data)
    response_loaded = json.loads(response.content)
    response_df = json_normalize(response_loaded)
    st.write("Your image contains a "+ response_df["class"])