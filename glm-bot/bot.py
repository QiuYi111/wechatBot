import chatglm_cpp
import hydra
from omegaconf import DictConfig,OmegaConf
from typing import List
import json
model_path= "/home/jingyi/Data/CodeBase/ChatBot/models/qiuyi.bin"
@hydra.main(config_path="../config", config_name="config")
def main(cfg: DictConfig,)->None:
    prompt=cfg.message
    generation_kwargs = dict(
        max_length=cfg.max_length,
        max_new_tokens=cfg.max_new_tokens,
        max_context_length=cfg.max_context_length,
        do_sample=cfg.temp > 0,
        top_k=cfg.top_k,
        top_p=cfg.top_p,
        temperature=cfg.temp,
        repetition_penalty=cfg.repeat_penalty,
        stream=True,
    )
    pipeline=chatglm_cpp.Pipeline(model_path,max_length=512)
    system_messages: List[chatglm_cpp.ChatMessage] = []
    if cfg.system is not None:
        system_messages.append(chatglm_cpp.ChatMessage(role="system", content=cfg.system))
    messages = system_messages.copy()
    messages.append(chatglm_cpp.ChatMessage(role="user", content=prompt))
    reply = ""
    for chunk in pipeline.chat(messages, **generation_kwargs):
        reply += chunk.content
    with open("/home/jingyi/Data/CodeBase/ChatBot/wechatBot/glm-bot/message.txt", "w", encoding="utf-8") as f:
        print(reply)
        f.write(reply)
    

main()