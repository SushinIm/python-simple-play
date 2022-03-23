from imap_tools import MailboxLoginError
from imap_tools import MailBox
import pandas as pd
import re

def mailChk(id, pw):
    mailbox = MailBox('imap.naver.com')

    mailbox.login(id,pw,initial_folder = 'inbox')

    mail_info = []
    for mail in mailbox.fetch('(UNSEEN)', limit = 100, reverse = True): #모든 안읽은 메일에 대해 데이터를 긁어오려면 limit 생략 가능 
        mail_date = re.sub('(.+):(.+)', '\\1시 \\2분', str(mail.date)[:16])

        tmp = []
        #메일 날짜, 발신일, 제목, 본문, 첨부파일 개수  
        tmp.append(mail_date)
        tmp.append(mail.from_values.name)
        tmp.append(mail.from_values.email)
        tmp.append(mail.subject)
        tmp.append(re.sub('\\n|\\r', '', mail.text))
        tmp.append(len(mail.attachments))
        mail_info.append(tmp)

        #파일 다운로드 : 
        for att in mail.attachments:
            #download_수신시간_메일제목_파일이름 형태로 다운로드 : 
            with open('download_' + mail_date + '_' + mail.subject + '_'+ att.filename,'wb') as f:
                f.write(att.payload) #payload 파일에다가 첨부파일을 쓰는 것 
                print('첨부파일{} 다운로드 완료'.format(att.filename))

    mailbox.logout()

    return mail_info

def main():
    #inbox : 받은 편지함
    file = open('./setting/userInfo.txt', 'r', encoding='utf-8')
    id = re.sub('\W$', '', file.readline())
    pw = re.sub('\W$', '', file.readline())
    file.close

    try:
        mail_info = mailChk(id, pw)
        print('불러온 읽지 않은 메일의 수 : ', len(mail_info))
    
        df = pd.DataFrame([(x[0], x[1], x[2], x[3], x[4], x[5]) for x in mail_info], columns=['날짜','발신자 이름','발신자 메일','제목','내용','첨부파일 개수'])
        
        #openpyxl 필요
        df.to_excel('mail_info.xlsx', sheet_name='받은메일함')

        print('메일 정리가 완료되었습니다.')

    except MailboxLoginError as e:
        print(e)
    except OSError as e:
        print(e)

if __name__ == '__main__':
    main()