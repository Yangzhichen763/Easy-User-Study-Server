import socketserver
import socket
import http.server
import json
import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler

import os
import random
import re

class Response:
    NONE = "201-None"
    DATA_NOT_FOUND = "401-DataNotFound"

# 获得本机 IP
def get_host_ip():
    try:
        # 创建一个 socket 对象
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到一个公共 DNS 服务器（可以随便选择）
        s.connect(("8.8.8.8", 80))
        # 获取本地 IP 地址
        ip_address = s.getsockname()[0]
    finally:
        s.close()
    return ip_address
IP = get_host_ip()
# 设置服务器端口
PORT = 8000
url = f"http://{IP}:{PORT}"

# 一些本地路径
image_dir = "images"
user_data_dir = "users/datas"


# http://10.133.4.94:8000/image?group=FourLLIE&id=00690
# 服务器 HTTP 处理器
class UserStudyHandler(BaseHTTPRequestHandler):
    def get_image_ids(self):
        image_ids = []
        for group in os.listdir("images"):
            tmp_image_ids = []
            for image_id in os.listdir(os.path.join(image_dir, group)):
                tmp_image_ids.append(image_id)
            # 取交集
            if len(image_ids) == 0:
                image_ids = tmp_image_ids
            else:
                image_ids = list(set(image_ids) & set(tmp_image_ids))
        return image_ids

    def do_GET(self):
        # 获取请求路径
        path = self.path
        # e.g. /image?group=FourLLIE&id=00690.png
        if path.startswith("/image?"):
            # 获取所有 params
            params = dict(param.split("=") for param in path.split("?")[1].split("&"))
            group = params["group"]
            image_id = params["id"]

            # 发送响应头
            self.send_response(200)
            self.send_header("Content-type", "image/jpeg")
            self.end_headers()

            # 发送响应体
            if '.' not in image_id:
                image_id += '.png'
            image_path = os.path.join(image_dir, group, image_id)
            with open(image_path, "rb") as f:
                self.wfile.write(f.read())
        # e.g. /images/FourLLIE/00690.png
        elif path.startswith("/images/"):
            image_path = path[1:]
            if ".." in image_path:
                self.send_response(404)
                self.end_headers()
                return

            # 发送响应体
            if os.path.isdir(image_path):
                # # 发送响应头
                # self.send_response(200)
                # self.send_header("Content-type", "application/json")
                # self.end_headers()
                #
                # # 发送目录结构
                # dir_path = {"paths": os.listdir(image_path)}
                # json_data = json.dumps(dir_path)
                # self.wfile.write(json_data.encode())
                pass

            if os.path.isfile(image_path):
                # 发送响应头
                self.send_response(200)
                self.send_header("Content-type", "image/jpeg")
                self.end_headers()

                # 发送图片
                with open(image_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                return
        # e.g. /image_ids, /image_ids?group=FourLLIE
        elif path.startswith("/image_ids"):
            # 获取所有 params
            if len(path.split("?")) > 1:
                params = dict(param.split("=") for param in path.split("?")[1].split("&"))
            else:
                params = {}

            # 发送响应头
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            # 发送指定组的图片 ID 列表
            image_ids = []
            if params.get("group"):
                group = params["group"]
                for image_id in os.listdir(os.path.join(image_dir, group)):
                    image_ids.append(os.path.splitext(image_id)[0])
            else:
                image_ids = self.get_image_ids()

            # 排序
            image_ids.sort()

            # 发送响应体
            json_data = json.dumps({"ids": image_ids})
            self.wfile.write(json_data.encode())
        # 获取所有图像组
        elif path.startswith("/image_groups"):
            # 获取所有 params
            if len(path.split("?")) > 1:
                params = dict(param.split("=") for param in path.split("?")[1].split("&"))
            else:
                params = {}

            # 发送所有组的名称列表
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            image_groups = os.listdir(image_dir)
            if params.get("exclude"):
                exclude_group = params["exclude"].split(",")
                image_groups = [group for group in image_groups if group not in exclude_group]

            # 发送响应体
            json_data = json.dumps({"groups": image_groups})
            self.wfile.write(json_data.encode())
        # 获取所有图像组的数量（除了 input 和 GT）
        elif path.startswith("/available_image_groups_number"):
            # 获取所有 params
            if len(path.split("?")) > 1:
                params = dict(param.split("=") for param in path.split("?")[1].split("&"))
            else:
                params = {}

            # 发送所有组的名称列表
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            image_groups = os.listdir(image_dir)
            if params.get("exclude"):
                exclude_group = params["exclude"].split(",")
                image_groups = [group for group in image_groups if group not in exclude_group]

            # 发送响应体
            json_data = json.dumps({"number": len(image_groups)})
            self.wfile.write(json_data.encode())
        elif path.startswith("/js/"):
            css_path = path[1:]
            if ".." in css_path:
                self.send_response(404)
                self.end_headers()
                return

            if os.path.isfile(css_path):
                # 发送响应头
                self.send_response(200)
                self.send_header("Content-type", "text/javascript")
                self.end_headers()

                # 发送响应体
                with open(css_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                return
        elif path.startswith("/css/"):
            css_path = path[1:]
            if ".." in css_path:
                self.send_response(404)
                self.end_headers()
                return

            if os.path.isfile(css_path):
                # 发送响应头
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()

                # 发送响应体
                with open(css_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                return
        elif path == "/style.css":
            # 发送响应头
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.end_headers()

            # 发送响应体
            with open("style.css", "rb") as f:
                self.wfile.write(f.read())
        # 服务器数据
        elif path.startswith("/server"):
            # 处理默认请求
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # 发送响应体
            with open("index.html", "rb") as f:
                self.wfile.write(f.read())
        # 用户注册时，检查用户是否存在
        elif path.startswith("/interface/contains_user?"):
            # 获取所有 params
            params = dict(param.split("=") for param in path.split("?")[1].split("&"))
            user_id = params["user_id"]

            # 处理默认请求
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # 检查文件 users/datas/ 下是否包含 {user_id}.dat 文件
            any_exist = os.path.exists(os.path.join(user_data_dir, f"{user_id}.dat"))
            print(f"User {user_id} exists: {any_exist}")

            # 发送响应体
            json_data = json.dumps({"exists": any_exist})
            self.wfile.write(json_data.encode())
        # 用户 User-Study 测验界面
        elif path.startswith("/interface?"):
            # 处理默认请求
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # 发送响应体
            with open("pages/interface.html", "rb") as f:
                self.wfile.write(f.read())
        # 用户 User-Study 测验界面
        elif path.startswith("/interface/"):
            # 处理默认请求
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # 发送响应体
            with open("pages/interface.html", "rb") as f:
                self.wfile.write(f.read())
        # 用户登录界面
        elif path.startswith("/"):
            # 处理默认请求
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # 发送响应体
            with open("pages/login.html", "rb") as f:
                self.wfile.write(f.read())
        else:
            # 处理其他请求
            self.send_response(404)
            self.end_headers()


    def get_select_id(self, can_select_ids):
        # 随机选取一个 ID
        if not os.listdir(image_dir):
            select_id = Response.DATA_NOT_FOUND
        elif len(can_select_ids) == 0:
            select_id = Response.NONE
        else:
            select_id = random.choice(can_select_ids)
        return select_id

    def do_POST(self):
        # 获取请求路径
        path = self.path

        # e.g. /interface/select?user_id=test
        if path.startswith("/interface/select?"):
            # 获取所有 params
            params = dict(param.split("=") for param in path.split("?")[1].split("&"))
            user_id = params["user_id"]

            dat_path = os.path.join(user_data_dir, f"{user_id}.dat")
            print(f"User {user_id} selected an image.", end=" ")
            try:
                # 处理传送的数据，为 form-data 的格式
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": self.headers["Content-Type"]}
                )
                data = {field: form.getvalue(field) for field in form}
                print(f"Data: {data}")

                select_id = data["select_id"]
                select_group = data["select_group"]
                print(f"Selected image ID: {select_id}, Group: {select_group}", end=" ")

                # 将数据写入文件
                if select_id != "None" and select_group != "None":
                    any_exist = os.path.exists(dat_path)
                    if any_exist:
                        # 将 select_gid 以 append 方式写入文件
                        with open(dat_path, "a") as f:
                            if data.get("select_id") and data["select_id"] != Response.NONE:
                                f.write(f"{select_id}, {select_group}\n")
                    else:
                        # 创建文件并写入 select_gid
                        with open(dat_path, "w") as f:
                            if data.get("select_id") and data["select_id"] != Response.NONE:
                                f.write(f"{select_id}, {select_group}\n")
            except Exception as e:
                print(f"\nError: {e}")
            print("")

            # 处理默认请求
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # 读入文件内容
            select_ids = []
            if os.path.exists(dat_path):
                with open(dat_path, "r") as f:
                    select_ids = f.read().strip().split(",")[0]

            # 计算可以选取的 ID，即 image_ids 中不包含 select_ids 的 ID
            image_ids = self.get_image_ids()
            can_select_ids = list(set(image_ids) - set(select_ids))

            # 获取 ID
            select_id = self.get_select_id(can_select_ids)

            # 发送响应体
            json_data = json.dumps({"next_id": select_id})
            self.wfile.write(json_data.encode())
        elif path.startswith("/interface/rating?"):
            # 获取所有 params
            params = dict(param.split("=") for param in path.split("?")[1].split("&"))
            user_id = params["user_id"]

            dat_path = os.path.join(user_data_dir, f"{user_id}.dat")
            print(f"User {user_id} selected an image.", end=" ")
            try:
                # 处理传送的数据，为 form-data 的格式
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": self.headers["Content-Type"]}
                )
                data = {field: form.getvalue(field) for field in form}
                print(f"Data: {data}")

                # 将数据写入文件
                any_exist = os.path.exists(dat_path)
                if any_exist:
                    # 将 select_gid 以 append 方式写入文件
                    with open(dat_path, "a") as f:
                        if data.get("id") and data["id"] != Response.NONE:
                            f.write(f"{data}\n")
                else:
                    # 创建文件并写入 select_gid
                    with open(dat_path, "w") as f:
                        if data.get("id") and data["id"] != Response.NONE:
                            f.write(f"{data}\n")

            except Exception as e:
                print(f"\nError: {e}")
            print("")

            # 处理默认请求
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # 读入文件内容（其中的 id）
            select_ids = []
            if os.path.exists(dat_path):
                with open(dat_path, "r") as f:
                    read_datas = f.read().strip().split("\n")
                    for read_data in read_datas:
                        id_re = re.findall(r"'id': '(.*?)'", read_data)
                        if id_re:
                            _id = id_re[0]
                            select_ids.append(_id)

            # 计算可以选取的 ID，即 image_ids 中不包含 select_ids 的 ID
            image_ids = self.get_image_ids()
            can_select_ids = list(set(image_ids) - set(select_ids))

            # 获取 ID
            select_id = self.get_select_id(can_select_ids)

            # 发送响应体
            json_data = json.dumps({"next_id": select_id})
            self.wfile.write(json_data.encode())



if __name__ == "__main__":
    os.makedirs(user_data_dir, exist_ok=True)

    # 创建一个服务器，并绑定到指定的端口
    with HTTPServer((IP, PORT), UserStudyHandler) as httpd:
        print(f"Server started at {url}/")
        # 开始监听并处理请求
        httpd.serve_forever()
