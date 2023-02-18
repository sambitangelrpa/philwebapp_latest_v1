import boto3
from upload_to_s3 import s3_function

class send_s3_function:
    def __init__(self):
        # s3_fun_obj=s3_function()
        pass




    def get_fed_prediction_link(self):
        url = boto3.client('s3').generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': 'speechsummary', 'Key': 'summary_prediction/ALL_FED_SPEECH_SUMMARY_DATA.xlsx'},
            ExpiresIn=172800)
        # Return the URL as a JSON response
        # return jsonify({'s3_url': url})
        return url

    def get_boe_prediction_link(self):
        url = boto3.client('s3').generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': 'speechsummary', 'Key': 'summary_prediction/ALL_BOE_SPEECH_SUMMARY_DATA.xlsx'},
            ExpiresIn=172800)
        # Return the URL as a JSON response
        # return jsonify({'s3_url': url})
        return url

    def get_ecb_prediction_link(self):
        url = boto3.client('s3').generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': 'speechsummary', 'Key': 'summary_prediction/ALL_ECB_SPEECH_SUMMARY_DATA .xlsx'},
            ExpiresIn=172800)
        # Return the URL as a JSON response
        # return jsonify({'s3_url': url})
        return url

    def get_fed_wordcloud_zip(self):
        url = boto3.client('s3').generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': 'speechsummary', 'Key': 'wordcloud/FedWordCloud/fed_images.zip'},
            ExpiresIn=172800)
        # Return the URL as a JSON response
        # return jsonify({'s3_url': url})
        return url
    def get_boe_wordcloud_zip(self):
        url = boto3.client('s3').generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': 'speechsummary', 'Key': 'wordcloud/BoeWordCloud/boe_images.zip'},
            ExpiresIn=172800)
        # Return the URL as a JSON response
        # return jsonify({'s3_url': url})
        return url

    def get_ecb_wordcloud_zip(self):
        url = boto3.client('s3').generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': 'speechsummary', 'Key': 'wordcloud/EcbWordCloud/ecb_images.zip'},
            ExpiresIn=172800)
        # Return the URL as a JSON response
        # return jsonify({'s3_url': url})
        return url


if __name__ == "__main__":
    # args = argparse.ArgumentParser()
    # args.add_argument("--config", default="config.yml")
    # parsed_args = args.parse_args()
    obj=send_s3_function()

    link=obj.get_fed_prediction_link()
    print('fed link',link)
    link1 = obj.get_boe_prediction_link()
    print('boe link', link1)
    link2 = obj.get_ecb_prediction_link()
    print('ecb link', link2)

    image_fed=obj.get_fed_wordcloud_zip()
    print('image_fed ',image_fed)
    image_ecb=obj.get_ecb_wordcloud_zip()
    print('image_ecb ', image_ecb)
    image_boe=obj.get_boe_wordcloud_zip()
    print('image_boe ', image_boe)
