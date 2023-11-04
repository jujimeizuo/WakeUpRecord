import argparse
import os
import random
import requests
import pendulum
import openai
import telebot

from github import Github
from telebot.types import InputMediaPhoto

# 14 for test 12 real get up
GET_UP_ISSUE_NUMBER = 1   
GET_UP_MESSAGE_TEMPLATE = (
    "今天的起床时间是--{get_up_time}.\r\n\r\n 懒狗🐶起床啦，不要玩手机，喝杯咖啡，背个单词，去跑步。\r\n\r\n 今天的一句诗:\r\n {sentence}"
)
SENTENCE_API = "https://v1.jinrishici.com/all"
DEFAULT_SENTENCE = "赏花归去马如飞\r\n去马如飞酒力微\r\n酒力微醒时已暮\r\n醒时已暮赏花归\r\n"
TIMEZONE = "Asia/Shanghai"


def login(token):
    return Github(token)


def get_one_sentence():
    try:
        r = requests.get(SENTENCE_API)
        if r.ok:
            return r.json().get("content", DEFAULT_SENTENCE)
        return DEFAULT_SENTENCE
    except:
        print("get SENTENCE_API wrong")
        return DEFAULT_SENTENCE


def make_pic_and_save(sentence):
    """
    return the link for md
    """
    sentence = sentence + ", textless"
    date_str = pendulum.now(TIMEZONE).to_date_string()
    image_dir_name = "images"
    image_dir = os.path.join(os.curdir, image_dir_name)
    if not os.path.exists(image_dir):
        os.mkdir(image_dir)
    generation_response = openai.Image.create(prompt=sentence, n=1, size="1024x1024", response_format="url")
    
    generated_image_name = f"{date_str}.png"
    generated_image_filepath = os.path.join(image_dir, generated_image_name)
    generated_image_url = generation_response["data"][0]["url"]
    generated_image = requests.get(generated_image_url).content

    with open(generated_image_filepath, "wb") as image_file:
        image_file.write(generated_image)

    image_url_for_issue = f"https://github.com/jujimeizuo/WakeUpRecord/blob/master/{image_dir}/{generated_image_name}?raw=true"
    
    return generated_image_url, image_url_for_issue


def get_today_get_up_status(issue):
    comments = list(issue.get_comments())
    if not comments:
        return False
    latest_comment = comments[-1]
    now = pendulum.now(TIMEZONE)
    latest_day = pendulum.instance(latest_comment.created_at).in_timezone(
        "Asia/Shanghai"
    )
    is_today = (latest_day.day == now.day) and (latest_day.month == now.month)
    return is_today


def make_get_up_message():
    sentence = get_one_sentence()
    now = pendulum.now(TIMEZONE)
    # 3 - 7 means early for me
    is_get_up_early = 3 <= now.hour <= 8
    get_up_time = now.to_datetime_string()
    image_link, link_for_issue = "", ""
    try:
        image_link, link_for_issue = make_pic_and_save(sentence)
    except Exception as e:
        print(str(e))
        # give it a second chance
        try:
            sentence = get_one_sentence()
            print(f"Second: {sentence}")
            image_link, link_for_issue = make_pic_and_save(sentence)
        except Exception as e:
            print(str(e))
    body = GET_UP_MESSAGE_TEMPLATE.format(get_up_time=get_up_time, sentence=sentence)
    return body, is_get_up_early, image_link, link_for_issue


def main(github_token, repo_name, weather_message, tele_token, tele_chat_id):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    u = login(github_token)
    repo = u.get_repo(repo_name)
    issue = repo.get_issue(GET_UP_ISSUE_NUMBER)
    is_toady = get_today_get_up_status(issue)
    if is_toady:
        print("Today I have recorded the wake up time")
        return
    early_message, is_get_up_early, image_link, link_for_issue = make_get_up_message()
    body = early_message
    if weather_message:
        weather_message = f"现在的天气是{weather_message}\n"
        body = weather_message + early_message
    if is_get_up_early:
        comment = body + f"![image]({link_for_issue})" if link_for_issue else ""
        issue.create_comment(comment)
        # send to telegram
        if tele_token and tele_chat_id:
            bot = telebot.TeleBot(tele_token)
            print(image_link, link_for_issue)
            photo_list = [InputMediaPhoto(image_link)]
            photo_list[0].caption = body

            print(photo_list)
            bot.send_media_group(tele_chat_id, photo_list, disable_notification=True)

            # requests.post(
            #     url="https://api.telegram.org/bot{0}/{1}".format(
            #         tele_token, "sendMessage"
            #     ),
            #     data={
            #         "chat_id": tele_chat_id,
            #         "text": body,
            #     },
            # )
        else:
            print("You wake up late")
            if tele_token and tele_chat_id:
                bot = telebot.TeleBot(tele_token)
                bot.send_media_group(tele_chat_id, "You wake up late", disable_notification=True)
            
            # requests.post(
            #     url="https://api.telegram.org/bot{0}/{1}".format(
            #         tele_token, "sendMessage"
            #     ),
            #     data={
            #         "chat_id": tele_chat_id,
            #         "text": "You wake up late",
            #     },
            # )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("github_token", help="github_token")
    parser.add_argument("repo_name", help="repo_name")
    parser.add_argument(
        "--weather_message", help="weather_message", nargs="?", default="", const=""
    )
    parser.add_argument("--tele_token", help="tele_token", nargs="?", default="", const="")
    parser.add_argument("--tele_chat_id", help="tele_chat_id", nargs="?", default="", const="")
    options = parser.parse_args()
    main(
        options.github_token,
        options.repo_name,
        options.weather_message,
        options.tele_token,
        options.tele_chat_id,
    )
