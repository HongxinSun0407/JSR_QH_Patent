import hashlib
import json
import time
import requests
from django.conf import settings

from patent_ai.exceptions import logger
from patent_ai.settings.base import KIMI_TIMEOUT

app_key = "e79c69c28d1a1a814f737253af5fd7f1"
app_secret = "1316057e6271e1c05c96dd22ee345b37b507339e8c51f7c9"


def request_tiangong_search_ai(data):
    """
    搜索
    :param data:
    :return:
    """
    url = 'https://api.singularity-ai.com/sky-saas-search/api/v1/search'
    timestamp = str(int(time.time()))
    sign_content = app_key + app_secret + timestamp
    sign_result = hashlib.md5(sign_content.encode('utf-8')).hexdigest()
    """
    :param data: [{"role": "user",
                "content": "你好呀"},{},{}]
    :param problem_id:
    :param stream:
    :return:
    """
    # 设置请求头，请求的数据格式为json
    headers = {
        "app_key": app_key,
        "timestamp": timestamp,
        "sign": sign_result,
        "Content-Type": "application/json",
    }
    # 发起请求并获取响应
    response = requests.post(url, headers=headers, json=data, timeout=KIMI_TIMEOUT)
    result = ""
    for line in response.iter_lines():
        if line:
            # 处理接收到的数据
            response_data = json.loads(line.decode('utf-8')[5:])
            if response_data['card_type'] == 'markdown' and response_data['target'] == 'finish':
                result = response_data['arguments'][0]['messages'][0]['text']
                break
    return result

def request_tiangong_chat_ai(data):
    """
    对话
    :param data:
    :return:
    """
    url = 'https://sky-api.singularity-ai.com/saas/api/v4/generate'
    timestamp = str(int(time.time()))
    sign_content = app_key + app_secret + timestamp
    sign_result = hashlib.md5(sign_content.encode('utf-8')).hexdigest()
    """
    :param data: [{"role": "user",
                "content": "你好呀"},{},{}]
    :param problem_id:
    :param stream:
    :return:
    """
    # 设置请求头，请求的数据格式为json
    headers = {
        "app_key": app_key,
        "timestamp": timestamp,
        "sign": sign_result,
        "Content-Type": "application/json",
    }
    request_data ={}
    request_data['messages'] = data['chat_history']
    request_data["model"] = "SkyChat-MegaVerse"
    # 发起请求并获取响应
    response = requests.post(url, headers=headers, json=request_data, stream=False, timeout=KIMI_TIMEOUT)
    result = json.loads(response.text)['resp_data']['reply']
    return result


def request_tiangong_writing_ai(data):
    """
    写作
    :param data:
    :return:
    """
    url = 'https://api.singularity-ai.com/sky-saas-writing/api/v1/chat'

    timestamp = str(int(time.time()))
    sign_content = app_key + app_secret + timestamp
    sign_result = hashlib.md5(sign_content.encode('utf-8')).hexdigest()
    """
    :param data: [{"role": "user",
                "content": "你好呀"},{},{}]
    :param problem_id:
    :param stream:
    :return:
    """
    # 设置请求头，请求的数据格式为json
    headers = {
        "app_key": app_key,
        "timestamp": timestamp,
        "sign": sign_result,
        "Content-Type": "application/json",
    }
    # 发起请求并获取响应
    response = requests.post(url, headers=headers, json=data, stream=False, timeout=KIMI_TIMEOUT)
    result = ""
    for line in response.iter_lines():
        if line:
            if line.decode('utf-8'):
                # 处理接收到的数据
                response_data = json.loads(line.decode('utf-8')[6:])
                arguments = response_data.get('arguments',None)
                if arguments and response_data['type'] == 1:
                    result = response_data['arguments'][0]['messages'][0]['text']
                if response_data['type'] == 2:
                    break
    return result

def request_tiangong_image_ai(data):
    """
    画图
    :param data:
    :return:
    """
    url = 'https://api-maas.singularity-ai.com/sky-saas-image/api/v1/generate'

    timestamp = str(int(time.time()))
    sign_content = app_key + app_secret + timestamp
    sign_result = hashlib.md5(sign_content.encode('utf-8')).hexdigest()
    """
    :param data: [{"role": "user",
                "content": "你好呀"},{},{}]
    :param problem_id:
    :param stream:
    :return:
    """
    # 设置请求头，请求的数据格式为json
    headers = {
        "app_key": app_key,
        "timestamp": timestamp,
        "sign": sign_result,
        "Content-Type": "application/json",
    }
    request_data = [i for i in data['chat_history'] if i['role'] == 'user'][-1]
    # 发起请求并获取响应
    response = requests.post(url, headers=headers, json=request_data, stream=False, timeout=KIMI_TIMEOUT)
    return response.json()['resp_data']['image_url']

def request_tiangong_copilot_ai(data):
    """
    增强
    :param data:
    :return:
    """
    url = "https://api.singularity-ai.com/sky-saas-search/api/v1/copilot"

    timestamp = str(int(time.time()))
    sign_content = app_key + app_secret + timestamp
    sign_result = hashlib.md5(sign_content.encode('utf-8')).hexdigest()
    """
    :param data: [{"role": "user",
                "content": "你好呀"},{},{}]
    :param problem_id:
    :param stream:
    :return:
    """
    # 设置请求头，请求的数据格式为json
    headers = {
        "app_key": app_key,
        "timestamp": timestamp,
        "sign": sign_result,
        "Content-Type": "application/json",
    }

    request_data = {}

    result_search_list = []
    request_data['content'] = [i for i in data['chat_history'] if i['role'] == 'user'][-1]['content']
    # 发起请求并获取响应
    response = requests.post(url, headers=headers, json=request_data, stream=False, timeout=KIMI_TIMEOUT)
    result_markdown = ""
    try:
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                # 处理接收到的数据
                if 'data: [DONE]' not in line:
                    response_data = json.loads(line[5:])
                    if response_data['card_type'] == 'markdown' and response_data['target'] == 'finish':
                        result_markdown = response_data['arguments'][0]['messages'][0]['text']
                    if response_data['card_type'] == 'search_result':
                        link = response_data['arguments'][0]['messages'][0]
                        if 'sourceAttributions' in link:
                            result_search_list = response_data['arguments'][0]['messages'][0]['sourceAttributions']
        return result_markdown, result_search_list
    except Exception as e:
        logger.error("增强模式出现错误", response.text, exc_info=True)
        raise e

def request_tiangong_research_ai(data):
    """
    研究
    :param data:
    :return:
    """
    url = "https://api.singularity-ai.com/sky-saas-search/api/v1/search/research"

    timestamp = str(int(time.time()))
    sign_content = app_key + app_secret + timestamp
    sign_result = hashlib.md5(sign_content.encode('utf-8')).hexdigest()
    """
    :param data: [{"role": "user",
                "content": "你好呀"},{},{}]
    :param problem_id:
    :param stream:
    :return:
    """
    # 设置请求头，请求的数据格式为json
    headers = {
        "app_key": app_key,
        "timestamp": timestamp,
        "sign": sign_result,
        "Content-Type": "application/json",
    }

    data = {
        "content": [i for i in data['chat_history'] if i['role'] == 'user'][-1]['content'],
    }
    data['stream_resp_type'] = 'all'
    data['is_scholar'] = True
    result_markdown = ""
    result_search_list = []
    response = requests.post(url, headers=headers, json=data, stream=False, timeout=KIMI_TIMEOUT)
    try:
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                # 处理接收到的数据
                if 'data: [DONE]' not in line:
                    response_data = json.loads(line[5:])
                    if response_data['card_type'] == 'expand_query':
                        break
                    if response_data['card_type'] == 'markdown' and response_data['target'] == 'finish':
                        result_markdown = response_data['arguments'][0]['messages'][0]['text']
                    if response_data['card_type'] == 'search_result':
                        link = response_data['arguments'][0]['messages'][0]
                        if 'sourceAttributions' in link:
                            result_search_list = response_data['arguments'][0]['messages'][0]['sourceAttributions']
        return result_markdown, result_search_list
    except Exception as e:
        logger.error("研究模式出现错误",response.text, exc_info=True)
        raise e

def get_money():
    return requests.get(url="https://api.moonshot.cn/v1/users/me/balance",
                        headers={"Authorization": f"Bearer {settings.API_KEY}"}).json()

def get_tokens_to_model(messages):
    """
    根据token获取model
    :param messages:
    :return:
    """
    model = "moonshot-v1-128k"
    tokens = 0
    try:
        data = requests.post(url="https://api.moonshot.cn/v1/tokenizers/estimate-token-count",
                             headers={"Authorization": f"Bearer {settings.API_KEY}"}, json={
                "model": model,
                "messages": messages
            })
        tokens = data.json().get("data").get("total_tokens")
        if tokens < 2900:
            model = "moonshot-v1-8k"
        elif tokens < 26000:
            model = "moonshot-v1-32k"
    finally:
        return model,tokens
if __name__ == '__main__':
    # data = {"chat_history": [{"role": "user", "content": "本专利信息如下：\n应用领域所属传统行业:医药制造业\n应用领域所属战略新兴产业:生物医药和高性能医疗器械\n解决问题:本专利针对现有技术中存在的不足，如数据分析局限于现有数据库、缺乏实验和临床验证、RNA测序技术耗时长不适用于临床需要快速用药的情形以及药效预测未提出具体快速的应用方案等问题，提出了一种能够基于较少基因数量快速预测癌症药效的方法，避免了对耗时较长的测序技术的依赖，并减少了药效预测的成本。\n技术效果:该药物敏感预测方法通过获取和预处理癌细胞组织的基因测序数据与药物特征数据，构建预测模型和基因预测列表，实现了快速精确地预测临床病人的药物反应性。此方法显著减少了预测成本和时间成本，提高了药效预测效率，有助于临床医生制定有效且毒性低的治疗方案。\n技术手段:技术手段包括：1) 获取待训练癌细胞组织的基因测序数据和药物特征数据；2) 对基因测序数据进行标准化处理和筛选，得到基因样本数据；3) 利用基因样本数据和药物特征数据，通过计算药敏相关系数和评分参数，对基因片段进行降序排列和验证处理，得到预测模型的模型参数和基因列表数目；4) 根据基因列表数目生成基因预测列表，确定预测模型。\n创新点:本专利的创新之处在于提供了一种快速且成本效益高的癌症药物敏感性预测方法，该方法不仅减少了对传统耗时测序技术的依赖，而且通过优化数据处理流程和预测模型的构建，提高了预测的精确度和效率。此外，该方法的实施不需要复杂的设备和技术，易于在临床环境中推广应用。\n专利描述:本专利公开了一种药物敏感预测方法，该方法涉及药物检测技术领域，特别是一种能够快速精确预测临床病人药物反应性的技术。通过优化基因测序数据处理和预测模型的构建，本发明大幅降低了药物敏感性预测的时间和成本，同时提高了预测效率，有助于实现精准医疗。\n潜在应用场景:【潜在应用场景】\n\n1. 癌症早期筛查\n   - 市场规模：随着人口老龄化和癌症发病率的上升，癌症早期筛查的需求持续增长。\n   - 市场环境：政府对医疗健康领域的投入增加，公众健康意识提高，为癌症早期筛查提供了良好的市场环境。\n   - 主要参与企业：暂无具体信息。\n   - 已有解决方案和产品：市场上已有一些癌症早期筛查技术，但成本较高，普及率有限。\n   - 市场痛点：癌症早期筛查的普及率不高，部分原因是筛查成本较高，且缺乏快速、准确的筛查方法。\n\n2. 临床试验设计\n   - 市场规模：新药研发过程中，临床试验是关键环节，市场需求巨大。\n   - 市场环境：中国政府鼓励创新药物研发，为临床试验提供了政策支持和资金投入。\n   - 主要参与企业：中源协和、国际医学等生物医药企业在新药研发领域具有优势。\n   - 已有解决方案和产品：传统的临床试验设计依赖于大量的患者数据和长时间的观察，效率较低。\n   - 市场痛点：临床试验周期长、成本高，且成功率不高，影响了新药研发的效率和成功率。\n\n3. 个体化治疗方案制定\n   - 市场规模：随着个性化医疗理念的普及，个体化治疗方案的需求日益增长。\n   - 市场环境：基因测序技术的发展为个体化医疗提供了技术支持，但成本和普及率仍有待提高。\n   - 主要参与企业：暂无具体信息。\n   - 已有解决方案和产品：市场上已有一些基因测序服务，但价格较高，且与治疗方案的结合不够紧密。\n   - 市场痛点：个体化治疗方案的制定受到技术和成本的限制，普及率有待提高。\n\n4. 药物复审和重新定位\n   - 市场规模：对于已上市的药物，通过重新评估其疗效，可以发现新的适应症，延长药物的生命周期，市场潜力巨大。\n   - 市场环境：政府鼓励药品创新和再评价，为药物复审和重新定位提供了政策支持。\n   - 主要参与企业：北陆药业、冠昊生物等在药品研发和再评价方面具有优势。\n   - 已有解决方案和产品：传统的药物复审和重新定位依赖于大量的临床数据和长时间的观察，效率较低。\n   - 市场痛点：药物复审和重新定位的过程繁琐、耗时，且成功率不高，影响了药物的市场竞争力。\n(1)分析以上列出的每一个潜在应用场景的产业化前景；\n(2)产业化前景的分析要加入未来3年内市场空间规模和增长预测，要搜索到具体的数字，不能出现假设的数字或者未知数XX%、**%、YY%；\n市场空间和增长预测可以搜索头部机构的行业分析报告作为参考，并且列出其中某一家头部机构给出的市场规模调查数据和未来3年增长预测。"}], "stream_resp_type": "all"}
    # a,b = request_tiangong_research_ai(data)
    # print()
    data = settings.KIMI_CLIENT.files.list()
    for i in data:
        settings.KIMI_CLIENT.files.delete(file_id=i.id)




