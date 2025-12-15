from openai import OpenAI
import json

def request_deepseek_ai(data, stream=False, model="deepseek-chat", json_response=False):
    client = OpenAI(
        api_key= "sk-5c8445cb2e544c6caf7cde2b4759eee4",
        base_url="https://api.deepseek.com"
    )

    message = data['messages']

    # Deepseek-chat支持64k上下文，设置较大的max_tokens以避免输出截断
    request_params = {
        "stream": stream,
        "model": model,
        "messages": message,
        "temperature": 0.7,
        "max_tokens": 60000  # 设置为60k，为输入预留空间
    }
    
    # 根据配置添加额外参数
    if json_response:
        request_params["response_format"] = {"type": "json_object"}
    
    # 发送请求
    completion = client.chat.completions.create(**request_params)
    return completion


def request_kimi_ai(data, stream=False, model="kimi-k2-0905-preview", json_response=False):
    """
    使用KIMI AI进行聊天请求
    
    Args:
        data (dict): 包含messages的请求数据
        stream (bool): 是否使用流式响应
        model (str): 使用的模型名称，默认为kimi-k2-0905-preview
        json_response (bool): 是否要求JSON格式响应
    
    Returns:
        OpenAI response object: AI的响应对象
    """
    from django.conf import settings
    
    messages = data['messages']
    
    # 根据模型设置合适的max_tokens（Kimi最新模型支持更大的上下文）
    # kimi-k2-0905-preview 支持128k上下文
    # kimi-k1-* 系列支持不同的上下文长度
    max_tokens = 120000  # 设置为120k，为输入预留一些空间
    
    request_params = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "stream": stream,
        "max_tokens": max_tokens
    }
    
    # 根据配置添加额外参数
    if json_response:
        request_params["response_format"] = {"type": "json_object"}
    
    # 发送请求
    completion = settings.KIMI_CLIENT.chat.completions.create(**request_params)
    return completion



def request_ai_with_fallback_json_response(data):
    try:
        analysis_result = request_deepseek_ai(data,json_response=True)
        analysis_content = analysis_result.choices[0].message.content
        return json.loads(analysis_content)
    except Exception as e:
        print(f"Deepseek AI请求失败，切换到Kimi AI: {str(e)}")
        try:
            analysis_result = request_kimi_ai(data, json_response=True)
            analysis_content = analysis_result.choices[0].message.content
            return json.loads(analysis_content)
        except Exception as e2:
            print(f"Kimi AI请求也失败: {str(e2)}")
            return {"team_scores": []} 


def request_kimi_ai_with_fallback_json_response(data):
    try:
        analysis_result = request_kimi_ai(data,json_response=True)
        analysis_content = analysis_result.choices[0].message.content
        return json.loads(analysis_content)
    except Exception as e:
        print(f"Kimi AI请求失败，切换到Deepseek AI: {str(e)}")
        try:
            analysis_result = request_deepseek_ai(data, json_response=True)
            analysis_content = analysis_result.choices[0].message.content
            return json.loads(analysis_content)
        except Exception as e2:
            print(f"Deepseek AI请求也失败: {str(e2)}")
            return {"team_scores": []}


def request_ai_chat(data):
    """
    替代天工对话模式的函数，使用Kimi优先，Deepseek作为备选
    
    Args:
        data (dict): 包含chat_history的请求数据，格式为{"chat_history": [{"role": "user", "content": "..."}]}
    
    Returns:
        str: AI的响应文本
    """
    # 转换数据格式：从天工的chat_history格式转换为标准messages格式
    messages = data.get('chat_history', [])
    request_data = {'messages': messages}
    
    try:
        # 优先使用Kimi AI
        result = request_kimi_ai(request_data)
        return result.choices[0].message.content
    except Exception as e:
        print(f"Kimi AI请求失败，切换到Deepseek AI: {str(e)}")
        try:
            # 备选使用Deepseek AI
            result = request_deepseek_ai(request_data)
            return result.choices[0].message.content
        except Exception as e2:
            print(f"Deepseek AI请求也失败: {str(e2)}")
            raise Exception(f"所有AI服务都失败: Kimi - {str(e)}, Deepseek - {str(e2)}")


def request_ai_with_search(data):
    """
    替代天工增强/研究模式的函数，使用Kimi或Deepseek
    注意：由于Kimi和Deepseek没有内置搜索功能，此函数只返回AI生成的内容，不返回搜索结果
    
    Args:
        data (dict): 包含chat_history的请求数据
    
    Returns:
        tuple: (answer_text, []) - 返回答案文本和空的搜索结果列表
    """
    answer = request_ai_chat(data)
    # 返回答案和空的搜索结果列表（因为Kimi/Deepseek没有搜索功能）
    return answer, []


def request_ai_image(data):
    """
    使用阿里云通义万相生成图片
    替代原天工AI的画图功能
    
    Args:
        data (dict): 包含chat_history的请求数据
            格式: {"chat_history": [{"role": "user", "content": "画图描述"}]}
    
    Returns:
        str: 图片URL
    
    Raises:
        Exception: 如果图片生成失败
    """
    try:
        import dashscope
        from dashscope import ImageSynthesis
        from django.conf import settings
        
        # 从chat_history中提取用户的画图描述
        messages = data.get('chat_history', [])
        prompt = ""
        for msg in messages:
            if msg.get('role') == 'user':
                prompt = msg.get('content', '')
        
        if not prompt:
            raise ValueError("画图描述不能为空")
        
        # 获取API Key（从settings中读取，或使用默认值）
        api_key = getattr(settings, 'DASHSCOPE_API_KEY', None)
        if not api_key:
            raise ValueError(
                "未配置通义万相API密钥。\n"
                "请在settings中添加: DASHSCOPE_API_KEY = 'your-api-key'\n"
                "获取API Key: https://dashscope.console.aliyun.com/"
            )
        
        # 设置API Key
        dashscope.api_key = api_key
        
        # 调用通义万相文生图API
        # 使用 wanx-v1 模型（稳定版本）
        response = ImageSynthesis.call(
            model='wanx-v1',
            prompt=prompt,
            n=1,  # 生成1张图片
            size='1024*1024',  # 图片尺寸，可选: 1024*1024, 720*1280, 1280*720
            # style='<auto>',  # 风格，可选: <auto>, <3d cartoon>, <anime>, <oil painting>, <watercolor>, <sketch>, <chinese painting>, <flat illustration>
        )
        
        # 检查响应状态
        if response.status_code == 200:
            # 获取图片URL
            image_url = response.output.results[0].url
            print(f"通义万相生成图片成功: {image_url}")
            return image_url
        else:
            error_msg = f"通义万相生成图片失败: {response.code} - {response.message}"
            print(error_msg)
            raise Exception(error_msg)
            
    except ImportError:
        raise ImportError(
            "未安装dashscope库。\n"
            "请运行: pip install dashscope\n"
            "或添加到requirements.txt"
        )
    except Exception as e:
        print(f"通义万相图片生成出错: {str(e)}")
        # 如果通义万相失败，返回文本描述作为后备方案
        return request_ai_chat(data)  