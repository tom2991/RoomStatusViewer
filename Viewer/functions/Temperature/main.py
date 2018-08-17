from jinja2  import Environment, FileSystemLoader
from os import path
import boto3
from datetime import datetime, timedelta, timezone


# DB接続情報
dynamoDB = boto3.resource('dynamodb')

templatePath = Environment(loader=FileSystemLoader(path.join(path.dirname(__file__), 'templates'), encoding='utf8'))

# lambdaのハンドラ
def handle(event, context):
    # パラメタ取得
    params = event.get('queryStringParameters', None)
    if(params != None):
        dispDate = params.get('date',0)
    else :
        dispDate = 0

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": createPage(dispDate)
    }

# ページ生成メソッド
# 日付・時刻・気温
def createPage(dispDate):

    # 日付が存在しないので今日の日付を取得する
    if(dispDate == 0):
        searchDate = getSearchDate(getNowDate())
        dispDate = getDispDate(getNowDate())
    else:
        searchDate = shapeDispDate(dispDate)

    renderData = cerateRenderData(searchDate)
    index = templatePath.get_template('index.html', )
    return index.render(title=u"気温グラフ",renderData=renderData, dispDate=dispDate)

def cerateRenderData(date):
    # DBにアクセスし、その日の気温を取得する
    table = dynamoDB.Table('temperature')
    responseItems = getResponceItems(table,date)
    temperateureList = []
    temperateureTimeList = []
    for data in responseItems:
        temperateureList.append(data['value'])
        dateTime = data['datetime_key'].split("_")
        temperateureTimeList.append(dateTime[1][:4])

    # DBにアクセスし、その日の湿度を取得する
    table = dynamoDB.Table('humidity')
    responseItems = getResponceItems(table,date)
    humidityList = []
    humidityTimeList = []
    for data in responseItems:
        humidityList.append(data['value'])
        dateTime = data['datetime_key'].split("_")
        humidityTimeList.append(dateTime[1][:4])

    # チャートデータ生成
    renderData = {}
    renderData['temp_time'] = temperateureTimeList
    renderData['temperature'] = temperateureList
    renderData['humid_time'] = humidityTimeList
    renderData['humidity'] = humidityList

    return renderData

def getResponceItems(table,date):
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('datetime_key').begins_with(date)
    )
    responseItems = response['Items']
    return sorted(responseItems, key=lambda x:x['datetime_key'])


# 今日の日付を返す
def getNowDate():
    # JSTを指定しないと、たぶんUNIX標準時になる
    JST = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(JST)
    return now

# 検索用の日付を取得する
def getSearchDate(now):
    return now.strftime("%Y%m%d")

# 画面表示用の日付を取得する
def getDispDate(now):
    return now.strftime("%m/%d/%Y")

# 画面表示用の日付を検索用に成形する
def shapeDispDate(dispDate):
    # 日付は"MM/DD/YYYY"の形でパラメタから入ってくるので
    # "YYYYMMDD"に変換する
    dispDateList = dispDate.split("/")
    return dispDateList[2] + dispDateList[0] + dispDateList[1]
