import count_tdee
import def_add_profile
import def_search_kalleft
import def_newday
import def_add_food
import def_search_food
import psycopg2
import configparser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from linebot.exceptions import InvalidSignatureError
from linebot import LineBotApi, WebhookHandler
from flask.logging import create_logger
from flask import Flask, request, abort
from argparse import ArgumentParser
import sys
import os

# 載入需要的模組

# 設定應用程式
app = Flask(__name__)
LOG = create_logger(app)
config = configparser.ConfigParser()
config.read("config.ini")

# 認證
line_bot_api = LineBotApi(config.get("line-bot", "channel_access_token"))
handler = WebhookHandler(config.get("line-bot", "channel_secret"))


# 根路由，測試用
@app.route("/")
def hello():
    return "hello world"


# callback路由，和line連線


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    LOG.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("400 error")
        abort(400)
    return "OK"


# 文字訊息事件
@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    # 定義變數
    text = event.message.text
    user_id = event.source.user_id

    # 開啟資料庫連線
    DATABASE_URL = os.environ["DATABASE_URL"]
    # DATABASE_URL = os.popen(
    #     "heroku config:get DATABASE_URL -a linebotforkal").read()[:-1]  # 本地端使用

    conn = psycopg2.connect(DATABASE_URL, sslmode="require")

    # 首先要在登錄tdee時就insert userid到activities表，就不用每次判斷activities表裡面有沒有這個user)
    print("user_id:", user_id)
    cursor = conn.cursor()
    SQL_order = f"""
    select status,tdee from userinfo where userid = '{user_id}'
    """
    cursor.execute(SQL_order)
    search_result = cursor.fetchone()
    # 定義使用者狀態與TDEE
    if search_result is None:
        status, tdee = None, None
        print(f"SQL搜尋成功，user尚未設定完成TDEE，已將user_id加入activities表")
    else:
        status, tdee = search_result
        print(f"SQL搜尋成功，user的狀態: {status}；TDEE:{tdee}")
    cursor.close()

    # 設定TDEE
    if text == "[設定TDEE]":
        def_add_profile.prfile_record(line_bot_api, conn, event, user_id, text, status)

    # 設定TDEE的功能
    # 記錄性別
    elif status in ["新增 user_id", "更新 user_id"]:
        def_add_profile.add_gender(line_bot_api, conn, event, user_id, text, status)
    # 記錄身高
    elif status == "記錄性別":
        def_add_profile.add_high(line_bot_api, conn, event, user_id, text, status)
    # 紀錄體重
    elif status == "記錄身高":
        def_add_profile.add_weight(line_bot_api, conn, event, user_id, text, status)
    # 紀錄年齡
    elif status == "記錄體重":
        def_add_profile.add_age(line_bot_api, conn, event, user_id, text, status)
    # 紀錄活動量
    elif status == "記錄年齡":
        def_add_profile.add_activity(line_bot_api, conn, event, user_id, text, status)
    # 開始計算TDEE
    elif status == "記錄活動量":
        count_tdee.count_tdee(line_bot_api, conn, event, user_id, text, status)

    else:
        if tdee is None:
            # 如果使用者尚未設定完成TDEE，不可做其他操作
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="請先完成TDEE(每日消耗總熱量)設定！")
            )
        else:

            # 查詢每日剩餘熱量
            if text == "[查詢今日剩餘熱量]":
                print("執行def_search_kalleft.kal_left")
                def_search_kalleft.kal_left(
                    line_bot_api, conn, event, user_id, text, status
                )

            # 今日結算
            elif text == "[今日結算]":
                def_newday.newday(line_bot_api, conn, event, user_id)

            # 紀錄每日攝取熱量
            elif text == "[飲食記錄]":
                def_search_food.kal_record(
                    line_bot_api, conn, event, user_id, text, status
                )

            # 在任何紀錄熱量的步驟中取消紀錄
            elif status in ["輸入關鍵字", "搜尋成功", "輸入數量"] and text == "[取消紀錄]":
                def_search_food.cancel(line_bot_api, conn, event, user_id, text, status)

            # 建立食物資料
            elif text == "[開始建立食物資料]":
                def_add_food.add_food(line_bot_api, conn, event, user_id, text, status)

            # 紀錄熱量攝取的功能
            # 輸入關鍵字
            elif status == "輸入關鍵字":
                def_search_food.search_food(
                    line_bot_api, conn, event, user_id, text, status
                )
            # 確定或取消食物攝取紀錄
            elif status == "搜尋成功" and text == "[確定紀錄]":
                def_search_food.confirm(
                    line_bot_api, conn, event, user_id, text, status
                )
            # 輸入攝取的食物數量
            elif status == "輸入數量":
                def_search_food.quantity_record(
                    line_bot_api, conn, event, user_id, text, status
                )

            # 新增食物資料的功能
            # 定義要建立的食物名稱
            elif status == "定義食物名稱":
                def_add_food.food_name(line_bot_api, conn, event, user_id, text, status)
            # 定義要建立的食物單位
            elif status == "定義單位":
                def_add_food.food_unit(line_bot_api, conn, event, user_id, text, status)
            # 定義要建立的食物熱量
            elif status == "定義熱量":
                def_add_food.food_kal(line_bot_api, conn, event, user_id, text, status)
            # 確認是否建立食物資料
            elif status == "確認是否建立":
                print("執行def_add_food.confirm")
                def_add_food.confirm(line_bot_api, conn, event, user_id, text, status)

    conn.close()


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage="Usage: python " + __file__ + " [--port <port>] [--help]"
    )
    arg_parser.add_argument("-p", "--port", default=8000, help="port")
    arg_parser.add_argument("-d", "--debug", default=False, help="debug")

    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
