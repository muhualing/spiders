from pprint import pprint
class Article(object):
    def __init__(self, title="", author="", pub_time="", pmid=None,
                    type='Autism', keywords="", author_info="", create_time=None, update_time=None, abstract=None):
        # 标题
        self.title = title
        # 作者名字
        self.author = author
        # 发布时间
        self.pub_time = pub_time
        # 文献id
        self.pmid = pmid
        # 疾病类型
        self.type = type
        # 关键词
        self.keywords = keywords
        # 作者信息
        self.author_info = author_info
        # 创建时间
        self.create_time = create_time
        # 更新时间
        self.update_time = update_time
        # 摘要
        self.abstract = abstract
    def printAll(self):
        pprint(self.__dict__)