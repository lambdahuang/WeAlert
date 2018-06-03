from mysql.wealert_db import WealertChatHistory, Session, engine


def main():
    WealertChatHistory.metadata.create_all(engine)
    record = WealertChatHistory(content="this is a test wechat record")
    session = Session()
    session.add(record)
    session.commit()
    print('I\'m here')


if __name__ == '__main__':
    main()
