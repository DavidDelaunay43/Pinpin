from dataclasses import dataclass
from datetime import datetime
from email.message import EmailMessage
import os
from pathlib import Path
import smtplib
from typing import Union
import requests
from Packages.utils.logger import Logger


@dataclass
class EmailContent:
    
    date_time: datetime
    user: str
    message: str = ''
    
    
    def __post_init__(self):
        self.date = self.date_time.date()
        self.time = self.date_time.time().replace(microsecond=0)


    def __repr__(self) -> str:
        return f'Date: {self.date}\nTime: {self.time}\nUser: {self.user}\n{self.get_location()}\n\n{self.message}'
    
    
    def string(self) -> str:
        return f'Date: {self.date}\nTime: {self.time}\nUser: {self.user}\n{self.get_location()}\n\n{self.message}'
    
    
    @staticmethod
    def get_location(return_string: bool = True) -> Union[dict, str]:
        
        data: dict = requests.get("https://ipinfo.io/").json()
        
        if return_string:
            return f'Location: {data.get("loc")}\nCity: {data.get("city")}\nCountry: {data.get("country")}'
        
        return {
            'location': data.get('loc'),
            'city': data.get('city',),
            'country': data.get('country')
        }


class Email:
    
    
    MAIL_SENDER: str = 'david.delaunay43@gmail.com'
    MAIL_RECEIVE: str = 'pinpin.pipeline@gmail.com'
    PASSWORD: str = 'vcgi pdiq yhux pqsp'
    
    email_message: EmailMessage = EmailMessage()
    message: str = ''
    attachment_files: list = []
    
    
    @classmethod
    def set_attachment_file(cls, file_path: Path) -> None:
        
        if not file_path.exists():
            Logger.error(f'Attachment file : {file_path} does not exists.')
            return
        
        with open(file_path, 'rb') as file:
            file_data = file.read()
            file_name = file_path.name
            cls.email_message.add_attachment(file_data, maintype='application', subtype='octet-stream', filename = file_name)
    
    
    @classmethod
    def send(cls, file_path: Union[str, Path, None] = None) -> None:
        
        date_time: datetime = datetime.now()
        content: EmailContent = EmailContent(
            date_time = date_time,
            user = os.getenv('USERNAME'),
            message = cls.message
        )
        subject: str = f'Pinpin Report {date_time.strftime("%Y-%m-%d %H:%M:%S")}'
        
        cls.email_message['Subject'] = subject
        cls.email_message['From'] = cls.MAIL_SENDER
        cls.email_message['To'] = cls.MAIL_RECEIVE
        cls.email_message.set_content(content.string())
        
        for file_path in cls.attachment_files:
            cls.set_attachment_file(file_path=file_path)
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(cls.MAIL_SENDER, cls.PASSWORD)
            smtp.send_message(cls.email_message)
            Logger.info(f'Email sent.')


def main() -> None:
    Email.send(file_path = r'C:\Users\David\Desktop\doc.txt')


if __name__ == '__main__':
    main()
