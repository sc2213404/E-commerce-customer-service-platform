import os
import mysql.connector
from os.path import dirname
from flask import Flask, request, jsonify
from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS, Chroma
import fitz  # PyMuPDF
from langchain_core.documents import Document
import requests
import base64
import cv2
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage, AIMessage
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import Tool
from langchain.chains import LLMChain

# 设置 API 密钥
os.environ["ZHIPUAI_API_KEY"] = "268f6a4112547dc35e5cffde932915db.kC6oTyfW6hXNP3iJ"
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
os.environ["SERPAPI_API_KEY"] = "8593821804b4f98c3835ba249a7931d0c0d445bb"

# 生成/构建 语言模型- Chat Model
from langchain_community.chat_models import ChatZhipuAI

zhipuai_chat_model = ChatZhipuAI(model="glm-4")
chat_model = zhipuai_chat_model

'''
获取当前文件所在的文件夹的根目录
----------------------------------------------
'''
def get_root_path():
    return os.path.abspath(dirname(__file__))

root_path = get_root_path()
'''
----------------------------------------------
'''

# 提供额外的数据-context（从网页加载），放入 Document 中
# 加载本地txt文件
def load_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
# 加载本地pdf文件
def load_pdf_file(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# 获取网页搜索资源
def search_web(query):
    params = {
        "q": query,
        "api_key": os.environ["SERPAPI_API_KEY"]
    }
    response = requests.get("https://serpapi.com/search", params=params)
    results = response.json()
    return results.get("organic_results", [])

# 读取视频按帧率保存图片
def VLink(video_path, images_path, interval):
    num = 1
    vid = cv2.VideoCapture(video_path)  # 打开视频
    while vid.isOpened():
        is_read, frame = vid.read()  # 按帧读取视频 frame是读取图像 is_read是布尔值。文件读取到结尾返回FALSE
        if is_read:
            if num % interval == 0:
                file_name = num
                cv2.imwrite(images_path + str(file_name) + '.jpg', frame)
            num += 1
        else:
            break
    vid.release()

# 调用百度API生成字幕
def requestApi(img):
    general_word_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    params = {"image": img,
              "language_type": "CHN_ENG"}
    access_token = '24.9871f17589cff759604d1f10e40d5c18.2592000.1723617741.282335-94807717'
    request_url = general_word_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    results = response.json()
    return results

# 生成字幕txt文件
def subtitle(fname, begin, end, step_size):
    # 定义一个数组用来存放字幕
    array = []  
    for i in range(begin, end, step_size):
        fname1 = fname % str(i)  # 字幕image D:/Resource/images/img_subtitle/100.jpg
        with open(fname1, 'rb') as fp:
            image = base64.b64encode(fp.read())
        try:
            results = requestApi(image)["words_result"]  # 调用requestApi函数，获取json字符串中的words_result
            for item in results:
                array.append(item['words'])
        except Exception as e:
            pass  # 忽略异常
    # 生成文本文件
    text = ''
    result = list(set(array))  # 去重
    result.sort(key=array.index)  # 排序
    for item in result:
        text += item + '\n'
    file = open(root_path+"\\Resource\\subtitle.txt", 'w', encoding='utf-8')
    file.write(text)
    file.close()

# 视频转图片
video_path = root_path+"\\Resource\\culture.mp4"  # 视频文件路径
images_path = root_path+"\\Resource\\images\\"  # 视频帧图片存放路径
# VLink(video_path, images_path, 10)

# 生成字幕txt文件
path1 = root_path+"\\Resource\\images\\%s.jpg"  # 视频转为图片存放的路径（帧）
# subtitle(path1, 100, 1000, 10)

'''
多方式获取数据
----------------------------------------------
'''
# 从网页加载数据
web_loader = WebBaseLoader("https://baike.baidu.com/item/%E7%BA%A2%E6%A5%BC%E6%A2%A6/10578542")
web_docs = web_loader.load()
web_docs = [{"page_content": doc.page_content} for doc in web_docs]

# 从本地文件（txt）加载数据
txt_docs = [{"page_content": load_txt_file(root_path+"\\Resource\\西游记.txt")}]

# 从本地文件（pdf）加载数据
pdf_docs = [{"page_content": load_pdf_file(root_path+"\\Resource\\水浒传.pdf")}]

# 从搜索引擎获取数据
search_results = search_web("三国演义")
search_docs = [{"page_content": result["snippet"]} for result in search_results]

# 从视频提取字幕数据
video_docs = [{"page_content": load_txt_file(root_path+"\\Resource\\subtitle.txt")}]
'''
----------------------------------------------
'''
# 合并所有数据来源的文档
docs = web_docs + txt_docs + pdf_docs + search_docs + video_docs

# 将字典转换为 Document 对象
docs = [Document(page_content=doc["page_content"]) for doc in docs]

# 将网页数据进行分词和向量存储
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(documents=docs)

# 选择不同的嵌入模型
embedding_models = {
    "model1": root_path+"\\m3e-base",
    "model2": "sentence-transformers/all-MiniLM-L6-v2"
}

# 选择不同的向量数据库
vector_stores = {
    "faiss": FAISS,
    "chroma": Chroma
}

# 使用指定的嵌入模型和向量数据库
selected_embedding_model = embedding_models["model1"]
selected_vector_store = vector_stores["faiss"]

embeddings = HuggingFaceEmbeddings(model_name=selected_embedding_model, model_kwargs={'device': 'cpu'})

# 使用指定的向量数据库进行向量存储
if selected_vector_store == FAISS:
    vector_store = FAISS.from_documents(documents=documents, embedding=embeddings)
elif selected_vector_store == Chroma:
    vector_store = Chroma.from_documents(documents=documents, embedding=embeddings)

retriever = vector_store.as_retriever()

# 生成带有历史记录的检索链
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])
retriever_chain = create_history_aware_retriever(chat_model, retriever, prompt)

prompt = ChatPromptTemplate.from_messages([
    ("system", "根据以下上下文回答用户的问题:\n\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])
document_chain = create_stuff_documents_chain(chat_model, prompt)
retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)

# 定义数学计算 Agent
python_repl = PythonREPLTool()
math_chain = LLMChain(llm=chat_model, prompt=ChatPromptTemplate.from_messages([
    ("system", "你是一个可以进行复杂数学计算的助手。"),
    ("user", "{input}")
]))
math_tool = Tool(name="MathTool", func=math_chain, description="适用于进行数学计算")

# 定义工具函数，识别问题类型并委派给合适的 Agent
def handle_book_chat(input_text):
    if any(keyword in input_text.lower() for keyword in ["calculate", "compute", "math", "sum", "difference"]):
        return math_chain
    return retrieval_chain

# 获取数据库连接
def getconnection():
    return mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='shops'
    )

# 定义一个处理数据库查询的函数
def handle_book_database_query(input_text):
    keywords = ["查询", "数据库", "库存", "订单", "用户", "商品"]
    if any(keyword in input_text for keyword in keywords):
        try:
            db_query = generate_query(input_text)
            result = execute_query(db_query)
            return True, result
        except Exception as e:
            return True, f"数据库查询失败: {str(e)}"
    return False, ""

# 定义一个生成数据库查询语句的函数
def generate_query(input_text):
    if "库存" in input_text:
        return "SELECT name, stock FROM Book_Goods"
    elif "订单" in input_text:
        return "SELECT Book_Orders.id, Users.username, Book_Orders.total_amount FROM Book_Orders JOIN Users ON Book_Orders.user_id = Users.id"
    elif "用户" in input_text:
        return "SELECT * FROM Users"
    elif "商品" in input_text:
        return "SELECT * FROM Book_Goods"
    else:
        raise ValueError("无法识别的查询类型")

# 定义一个执行数据库查询的函数
def execute_query(query):
    db = getconnection()
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results
