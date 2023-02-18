import boto3
import pandas as pd
import argparse
import yaml
import os
import jsonify

class s3_function:
    def __init__(self,config_path):

        with open(config_path) as yaml_file:
            self.config = yaml.safe_load(yaml_file)
        self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource(
            service_name='s3',
            region_name='us-east-1',
            aws_access_key_id=self.config['auth']['Access key ID'],
            aws_secret_access_key=self.config['auth']['Secret access key']
        )
        self.bucket_name = 'speechsummary'

    # def read_params(self,config_path):
    #     """
    #     read parameters from the params.yaml file
    #     input: params.yaml location
    #     output: parameters as dictionary
    #     """
    #     with open(config_path) as yaml_file:
    #         config = yaml.safe_load(yaml_file)
    #     return config


    def upload_prediction_file(self):
        # config = self.read_params(config_path)
        # self.s3 = boto3.client('s3')
        #
        # self.s3 = boto3.resource(
        #     service_name='s3',
        #     region_name='us-east-1',
        #     aws_access_key_id=config['auth']['Access key ID'],
        #     aws_secret_access_key=config['auth']['Secret access key']
        # )
        # Print out bucket names
        # for bucket in s3.buckets.all():
        #     if bucket == 'speechsummary':
        #         bucket_name = bucket
        # self.bucket_name = 'speechsummary'
        folder_paths = ['summary_prediction/']
        #wordcldfolders='wordcloud/BoeWordCloud/','wordcloud/EcbWordCloud/','wordcloud/FedWordCloud/'
        for folder_path in folder_paths:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    # construct the full local path of the file
                    local_path = os.path.join(root, file)
                    print(local_path)

                    # construct the full S3 path of the file
                    # s3_path = os.path.join(local_path, folder_path, file)
                    # print('s3_path',s3_path)
                    # upload the file to S3
                    self.s3_resource.Bucket(self.bucket_name).upload_file(local_path,local_path)
            # s3.Bucket(bucket_name).upload_file(Filename=folder, Key=folder)


    def upload_imaage_zip_file_for_banks(self):
        import boto3
        import zipfile
        import os

        # Set the S3 bucket name, the S3 folder name, and the local directory containing the images to be zipped
        import os
        import zipfile
        import boto3

        s3 = boto3.client('s3')
        bucket_name = 'speechsummary'
        s3_folders = ['wordcloud/FedWordCloud', 'wordcloud/BoeWordCloud', 'wordcloud/EcbWordCloud']
        local_dirs = ['wordcloud/FedWordCloud', 'wordcloud/BoeWordCloud', 'wordcloud/EcbWordCloud']
        zip_filenames = ['fed_images.zip', 'boe_images.zip', 'ecb_images.zip']

        for s3_folder, local_dir, zip_filename in zip(s3_folders, local_dirs, zip_filenames):
            # Create a new zip file and add all the images from the local directory to it
            with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                for filename in os.listdir(local_dir):
                    if filename.endswith('.jpg') or filename.endswith('.png'):
                        zip_file.write(os.path.join(local_dir, filename))

            # Upload the zip file to the S3 bucket and folder
            with open(zip_filename, 'rb') as f:
                s3.upload_fileobj(f, bucket_name, f"{s3_folder}/{zip_filename}")

            # Print a message to indicate that the file has been uploaded
            print(f'{zip_filename}File uploaded to S3')


if __name__ == "__main__":
    # args = argparse.ArgumentParser()
    # args.add_argument("--config", default="config.yml")
    # parsed_args = args.parse_args()
    obj=s3_function("config.yml")
    obj.upload_prediction_file()
    # obj.upload_imaage_zip_file_for_banks()
