import boto3
from botocore.client import Config
import StringIO
import zipfile

def lambda_handler(event, context):

    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:530763483519:deployPortfolioTopic')

    try:
        s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

        build_bucket = s3.Bucket('portfolio.vasishta.adiraju')
        portfolio_bucket = s3.Bucket('vasishta-adiraju-portfolio')
        build_file = 'portfoliobuild.zip'
        local_file_name = '/tmp/' + build_file

        build_bucket.download_file(build_file, local_file_name)

        with zipfile.ZipFile(local_file_name) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm)
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')


        print "Process Successful!"
        topic.publish(Subject="Portfolio Deployment", Message="Portfolio Deployment Successful")

    except:

        topic.publish(Subject="Portfolio Deployment Unsuccessful", Message="Portfolio Deployment was unsuccessful")
        raise

    return 'Deployment Successful'
