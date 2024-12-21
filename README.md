# Easy User-Study Server

## 目录
- [项目结构](#项目结构)
  - [服务器部分](#服务器部分)
  - [前端模板](#前端模板)
- [使用指南](#使用指南)
  - [快速开始](#快速开始)
  - [自定义](#自定义)
- [界面展示](#界面展示)

## 项目结构

### 服务器部分
创建的服务器是 IP 服务器
- IP 地址为电脑连上的局域网的 IP 地址
- 端口号为 8000
```txt
├── server.py         // 服务器主文件
```

### 数据部分

```txt
├── images
    ├── input
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   ├──...
    ├── method_name
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   ├──...
    ├──...
```

## 使用指南

### 快速开始

#### 克隆项目
```shell
git clone https://github.com/Yangzhichen763/Easy-User-Study-Server.git
cd Easy-User-Study-Server
```
#### 配置环境
```shell
pip install -r requirements.txt
```
#### 启动服务器
```shell
python server.py
```
启动完服务器后：
- 访问 `http://{IP地址}:8000` 即可看到 User-Study 的登录页面
- 访问 `http://{IP地址}:8000/server` 即可看到服务器中的内容

### 自定义

- 自定义首页：在 `index.html` 中进行修改
- 自定义 User-Study 界面：在 `pages/interface.html` 中进行修改
  - 在 `pages/templates/` 中有一些预设的模板，可以直接使用吗，比如：
    - `interface_click.html` 文件专注于选择更好的图片
    - `interface_rating` 专注于评分图片）
- 自定义服务器内容：在 `server.py` 的 `UserStudyHandler` 中进行修改
  - 对于需要通过少量参数获取的数据，在 `do_GET` 函数中添加条件分支
  - 对于需要通过大量数据获取的数据，在 `do_POST` 函数中添加条件分支

## 界面展示

### 登录界面

![login\.png](figures/login.png)

### User-Study 界面

![interface\.png](figures/interface.png)

### 服务器内容

![server\.png](figures/server.png)

## 未来展望
- 使用 Flask 作为服务器 Web 开发框架