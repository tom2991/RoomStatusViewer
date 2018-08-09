from jinja2  import Environment, FileSystemLoader
from os import path
import boto3

# DB接続情報
dynamoDB = boto3.resource('dynamodb')
table = dynamoDB.Table('temperature')

templatePath = Environment(loader=FileSystemLoader(path.join(path.dirname(__file__), 'templates'), encoding='utf8'))

# lambdaのハンドラ
def handle(event, context):
    print("print log.")
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": createPage()
    }

# ページ生成メソッド
# 日付・時刻・気温
def createPage():
    index = templatePath.get_template('index.html', )
    return index.render(title=u"気温グラフ")

def getTemperatue(date):
    # DBにアクセスし、その日の気温を取得する
    # return temperatue
    return 0