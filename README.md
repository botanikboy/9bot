# 9bot - memes without promotion and advertising
Simple telegram bot for parsing memes from one popular site, it filters only pics, without videos, promoted posts and adds.

## Launch instructions
To launch your onw bot instance, please register telegram bot 
(follow this tutorial https://core.telegram.org/bots/tutorial#getting-ready).

Clone the repo and create .env file with bot token inside (see [.env.example](.env.example))
Create and activate virtual envinronment:

```
python3.8 -m venv venv
```

* for Linux/macOS

    ```
    source venv/bin/activate
    ```

* For Windows

    ```
    source venv/scripts/activate
    ```

Install dependencies requirements.txt:

```
python3 -m pip install --upgrade pip

pip install -r requirements.txt
```

Start your bot:
```
python3 9bot.py
```

You can launch your bot on any vps using these instructions and enjoy personal ads free meme source.

## Stack
- [Python](https://www.python.org/)
- [python-telegram-bot](https://pypi.org/project/python-telegram-bot/)

## Author
Developed by:
[Ilya Savinkin](https://www.linkedin.com/in/ilya-savinkin-6002a711/)
