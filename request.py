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
st.markdown('# Opaki vs Zebra')
st.markdown('**Step 1:** Download an image of an [opaki](https://www.google.com/search?q=opaki&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjM9oPtoaXnAhUiw1kKHf7ODgkQ_AUoAXoECA0QAw&cshid=1580179182106307&biw=1920&bih=946) or [zebra](https://www.google.com/search?q=zebra&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjT3rWFoqXnAhWQm1kKHcEQCq8Q_AUoAXoECBAQAw&biw=1920&bih=946)')
st.markdown('**Step 2:** Upload your image below')
st.markdown('**Step 3:** Click _Classify_ to see what my neural network thinks')


uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
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
    response = requests.post("{}/".format('http://0.0.0.0:22109'), json =post_data)
    response_loaded = json.loads(response.content)
    response_df = json_normalize(response_loaded)
    st.markdown("Your image contains a **"+response_df.iloc[0,0]+'**')