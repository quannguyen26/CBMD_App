with open('dong_tpl\\mail.txt', 'r') as file:
         content_list = [line.strip() for line in file.readlines() if not line.startswith('#')]

email_list = [email.strip() for email in ", ".join(content_list[:]).split(',')]
print(email_list)