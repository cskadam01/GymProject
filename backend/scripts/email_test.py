import smtplib

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login("flux.note.gym@gmail.com", "xtbp zxgi uvso ishe")
server.sendmail("flux.note.gym@gmail.com", "adam.csokonyi@gmail.com", "teszt")
server.quit()