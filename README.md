# WechatBot 让大模型替你聊天

本项目基于以下项目：

+ 微信SDK：[OpenWechat](https://github.com/eatmoreapple/openwechat)
+ 智谱清言大模型：[ChatGLM3](https://github.com/THUDM/ChatGLM3)
+ 大模型运行优化：[ chatglm.cpp](https://github.com/li-plus/chatglm.cpp)
+ 微信数据获取：[WechatMsg](https://github.com/LC044/WeChatMsg)

## 安装

### 安装本仓库

```bash
git clone  https://github.com/QiuYi111/wechatBot

```

#### 创建虚拟环境，安装Hydra

```bash
conda create -n wechatbot
conda activate wechatbot
pip install -r requirements.txt
```

### 安装OpenWechat

首先创建模块

```bash
go mod init wechatbot
```

为模块安装OpenWechat

```bash
go get -u github.com/eatmoreapple/openwechat
```

### 安装ChatGLM3

```bash
git clone https://github.com/THUDM/ChatGLM3

```

### 安装chatglm.cpp

首先下载仓库

```bash
git clone --recursive https://github.com/li-plus/chatglm.cpp.git && cd chatglm.cpp
```

安装python binding

```bash
CMAKE_ARGS="-DGGML_CUDA=ON" pip install -U chatglm-cpp
```

## 获取数据

使用wechatmsg获得聊天数据。

前往 [memotrace下载](https://memotrace.cn/) ，安装。

使用微信自带的迁移功能将聊天记录迁移至电脑端。

点击左上角导出聊天记录后，选择只导出文字。

你应该获得 `聊天记录` 文件夹，将之移到 `Raw_Data`下，运行：

```bash
python ./data_process/data_merge.py
```

你应该能在 data文件夹下找到 `train.json` 和 `dev.json`

## Lora 训练

请参见：[chatglm3 官方实践](https://github.com/THUDM/ChatGLM3/blob/main/finetune_demo/README.md)

## 合并模型并量化

运行：

```bash
cd chatglm.cpp
python3 chatglm_cpp/convert.py -i THUDM/chatglm3-6b -t q4_0 -o models/<your_model>.bin -l path/<your_lora>
```

编译模型：

```bash
cd chatglm_cpp
cmake -B build -DGGML_CUDA=ON && cmake --build build -j
```

如果你的设备没有CUDA:

```bash
cd chatglm_cpp
cmake -B build && cmake --build build -j
```

你应该在 `chatglm.cpp/chatglm_cpp/models`下找到你的模型，将之剪切到本项目的 `models`

## 配置

### config

在项目仓库的 ` config` 下，配置 `config.yaml`。其中包括大模型参数和默认提示语，请将 <用户名> 换成你的微信昵称，保证与 `train.json `一致以启用lora。

### bot.go

这里需要配置的是用户名。


## 启动

运行：

```bash
cd glm-bot
go run bot.go
```

扫码登陆微信即可。
