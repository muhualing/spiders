import requests

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}

url='https://www.google.com/search'
#处理url所携带的参数，将其封装到字典当中
kw=input("enter a word：")
param={
    'q':kw
}
#对指定url发起的请求url是携带参数的
response=requests.get(url=url,params=param,headers=headers)
page_text=response.text
print(page_text)
file_name=kw+'.html'
with open(file_name,'w',encoding='utf-8') as fp:
    fp.write(page_text)