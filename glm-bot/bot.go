package main

import (
	"fmt"
	"os"
	"os/exec"

	"github.com/eatmoreapple/openwechat"
)

func main() {
	bot := openwechat.DefaultBot(openwechat.Desktop) // 桌面模式

	// 注册消息处理函数
	bot.MessageHandler = func(msg *openwechat.Message) {
		if msg.IsText() && msg.Content == "ping" {
			msg.ReplyText("pong")
		}
	}
	// 尝试热重载
	reloadStorage := openwechat.NewFileHotReloadStorage("storage.json")
	defer reloadStorage.Close()
	err := bot.HotLogin(reloadStorage, openwechat.NewRetryLoginOption())
	// 热重载失败，登陆
	if err != nil {
		fmt.Println(err)
		bot.UUIDCallback = openwechat.PrintlnQrcodeUrl
		bot.Login()
		return
	}

	// 注册消息处理函数
	bot.MessageHandler = func(msg *openwechat.Message) {
		if msg.IsText() && msg.IsSendByFriend() {
			fmt.Println(msg.Content)
			cmd := exec.Command("python", "bot.py", fmt.Sprintf("message=\"%s\"", msg.Content))
			err := cmd.Run() // This will wait for the command to complete
			if err != nil {
				fmt.Println("运行脚本失败:", err)
				return
			}
			reply_message, err := os.ReadFile("message.txt")
			if err != nil || string(reply_message) == "" {
				fmt.Println("无法读取文件:", err)
				return
			}
			text := "[QiuYi.ai]"+string(reply_message)
			msg.ReplyText(text)
			err = os.WriteFile("message.txt", []byte(""), 0644)
			if err != nil {
				fmt.Println("清空文件失败:", err)
				return
			}
			
		}
	}

	bot.Block()
}
