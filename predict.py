from fastai.vision import *

# allows access to aws s3 in order to retrive the file

import boto3
import botocore

from flask import Flask,jsonify,request
app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def index():
    if(request.method == 'POST'):
        data = request.get_json()
        filename = data["filename"]
        bucket_name = data["bucket"]
        # Create an S3 client
        s3 = boto3.resource('s3')
        try:
            s3.Bucket(bucket_name).download_file(filename, './images/download.jpg')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

        img = open_image('./images/download.jpg')

        defaults.device = torch.device('cpu')
        classifier = load_learner('')
        pred_class = classifier.predict(img)[0]
        string = pred_class.__str__()
        return jsonify({"class":string})
    else:
        return  jsonify({"about":"Hello World"})

if __name__ == '__main__':
    app.run(debug=True)