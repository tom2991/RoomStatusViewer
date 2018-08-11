from jinja2  import Environment, FileSystemLoader
from os import path
import boto3
from datetime import datetime, timedelta, timezone


# DB接続情報
dynamoDB = boto3.resource('dynamodb')
table = dynamoDB.Table('temperature')

templatePath = Environment(loader=FileSystemLoader(path.join(path.dirname(__file__), 'templates'), encoding='utf8'))

# lambdaのハンドラ
def handle(event, context):
    # パラメタ取得
    # if('date' not in event['queryStringParameters']):
    #     date = 0
    # else:
    #     date = event['queryStringParameters']['date']


    print("print log.")
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": createPage(0)
    }

# ページ生成メソッド
# 日付・時刻・気温
def createPage(date):

    # 日付が存在しないので今日の日付を取得する
    if(date == 0):
        date = getNowDate()
    
    renderData = cerateRenderData(date)
    index = templatePath.get_template('index.html', )
    date = "2018/08/11"
    return index.render(title=u"気温グラフ",renderData=renderData)

def cerateRenderData(date):
    # DBにアクセスし、その日の気温を取得する
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('datetime_key').begins_with(date)
    )
    temperateureList = []
    timeList = []
    responseItems = response['Items']
    responseItems = sorted(responseItems, key=lambda x:x['datetime_key'])
    for data in responseItems:
        temperateureList.append(data['value'])
        dateTime = data['datetime_key'].split("_")
        timeList.append(dateTime[1][:4])
    renderData = {}
    renderData['time'] = timeList
    renderData['temperature'] = temperateureList

    return renderData

# DB検索用に今日の日付を返す
def getNowDate():
    # JSTを指定しないと、たぶんUNIX標準時になる
    JST = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(JST)
    return now.strftime("%Y%m%d")
