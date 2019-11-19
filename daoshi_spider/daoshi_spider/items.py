# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class TalentItem(scrapy.Item):
    url = scrapy.Field() # 爬取地址
    tid = scrapy.Field() # 人才唯一标识
    name = scrapy.Field()
    orgId = scrapy.Field()
    orgName = scrapy.Field() # 机构名称（企业、机构）
    title = scrapy.Field() # 职称
    domain = scrapy.Field() # 主领域
    sex = scrapy.Field()
    highestEdu = scrapy.Field() # 最高学历
    talentClass = scrapy.Field() # 人才分类（研究性；产业型；技能型；工程型）
    professionGrade = scrapy.Field() # 职业资格（正高级；副高级；中级；初级）
    mobile = scrapy.Field()
    telephone = scrapy.Field()
    email = scrapy.Field()
    wechat = scrapy.Field()
    personalHomepage = scrapy.Field() # 个人主页
    fax = scrapy.Field()
    address = scrapy.Field()
    birthday = scrapy.Field()
    coreAbility = scrapy.Field()  # 核心能力
    researchInterest = scrapy.Field() # 研究兴趣/研究领域（多个使用英文","拼接）
    quoteNum = scrapy.Field() # 成果被引用次数
    resultNum = scrapy.Field() # 成果数
    hfactor = scrapy.Field()  # H因子/H指数
    gfactor = scrapy.Field() # g指数/g因子
    talentDesc = scrapy.Field() # 人才简介
    createTime = scrapy.Field()
    updateTime = scrapy.Field()

class EduItem(scrapy.Item):
    tid = scrapy.Field()
    schoolName = scrapy.Field()
    getEdu = scrapy.Field()
    studyDate = scrapy.Field()
    getReward = scrapy.Field()
    createTime = scrapy.Field()
    updateTime = scrapy.Field()

class CompanyItem(scrapy.Item):
    url = scrapy.Field()
    companyName = scrapy.Field()
    companySize = scrapy.Field() #企业规模（员工人数）
    companyType = scrapy.Field() # 企业类型（民营、外企等）
    companyDesc = scrapy.Field() # 企业描述
    companyAddress = scrapy.Field() # 企业地址
    companyIndustry = scrapy.Field() # 行业类型
    createTime = scrapy.Field()
    updateTime = scrapy.Field()

class PaperItem(scrapy.Item):
    tid = scrapy.Field()
    paperName = scrapy.Field() #论文名称
    paperAuthor = scrapy.Field() # 作者
    quoteNum = scrapy.Field()  # 引用数量
    publishSpace = scrapy.Field() # 论文发布空间
    createTime = scrapy.Field()
    updateTime = scrapy.Field()

class PathenItem(scrapy.Item):
    tid = scrapy.Field()
    pathentName = scrapy.Field() # 专利名称
    pathentNo = scrapy.Field() # 专利号
    pathentDate = scrapy.Field() # 专利申请时间（string）
    createTime = scrapy.Field()
    updateTime = scrapy.Field()

class ProjectItem(scrapy.Item):
    tid = scrapy.Field()
    projectName = scrapy.Field() # 项目名称
    projectLeader = scrapy.Field() # 负责人
    projectLeaderOrg = scrapy.Field() # 负责人机构
    joinRole = scrapy.Field() # 参与角色
    projectDesc = scrapy.Field() # 描述
    projectResult = scrapy.Field() # 项目成果
    projectReward = scrapy.Field() # 项目奖励
    projectFund = scrapy.Field() # 项目资助金额
    projectKeyword = scrapy.Field() # 项目关键词（多个使用英文","拼接）
    createTime = scrapy.Field()
    updateTime = scrapy.Field()

class TeamItem(scrapy.Item):
    tid = scrapy.Field()
    tUrl = scrapy.Field()
    tName = scrapy.Field() # 合作者名称
    tOrg = scrapy.Field() # 合作者机构
    hfactor = scrapy.Field() # h因子
    workNum = scrapy.Field() # 合作次数
    createTime = scrapy.Field()
    updateTime = scrapy.Field()

class WorkItem(scrapy.Item):
    tid = scrapy.Field()
    company = scrapy.Field()
    post = scrapy.Field()
    postWork = scrapy.Field()
    postResult = scrapy.Field()
    createTime = scrapy.Field()
    updateTime = scrapy.Field()