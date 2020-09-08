import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",       # 数据库主机地址
  user="root",    # 数据库用户名
  passwd="734660",   # 数据库密码
  database="shopping",
  buffered = True
   
)

mycursor = mydb.cursor()


user_name = "admin"    #全局变量，获取用户名
user_passwd = "123456"   #全局变量，获取用户密码
no_count = 0    #用户编号计数器

#接收用户名和密码函数
def login(name, passwd):
    user_name = name
    user_passwd = passwd


#与数据库中的用户名和密码进行比对
#比对方法：将所有用户名取出，进行逐一比对，用户名匹配则匹配密码，不一致返回密码错误，若用户名未成功匹配，则返回用户名错误
def login_test(name,passwd):
    global mycursor
    mycursor.execute("select user_name, passwd from user_login")   #不确定mycursor是否可以直接在函数中作为调用，如果写成全局变量是否会出现错误
    myresult = mycursor.fetchall()  

    count = 0

    for x in myresult:
        count = count + 1
        if x[0] == name:
            if x[1] == passwd:
                print("登录成功！")
                c = 0
                break
            else:
                print("密码错误！")
                c = 1
                break
    

    if count == len(myresult):
        c = 1
        print("您输入的用户名不存在！")

    return c  #c为0登录成功，c为1登录不成功      

#用户类，用于储存用户个人信息，和用户购买商品信息

class User(object):

    def __init__(self，name):
        #global no_count    #用来生成用户编号

        mycursor.execute("select * from user_login where user_name ='name")


        self.name = user_name
        self.passwd = user_passwd

        self.no = no_count
        no_count = no_count + 1

        self.goods_list = ["商品列表"] #用来储存bk_name字典
        self.bk_name = None #字典，用键值对的形式储存书名和图书编号，储存的是用户购买的图书信息

        self.price = 0
    
    def welcome(self):
        print("欢迎光临，%s" %self.name)

    #用户购买图书方法,根据输入的图书编号确定,每购买一本书，即调用一次该方法,需要修改，直接从数据库里面调取数据
    def bookShopping(self,bkno):
        bkno = input("请输入图书编号：")
        bk_name = {"书名":a.bk_name,"图书编号":bkno}
        goods_list.append(bk_name)
        self.price = self.price + a.bk_price
    
    # 显示用户已购图书列表
    def showShoppingList(self):
        print(self.goods_list)
        


class book_info(object):
    #要实现的功能是，在生成图书类对象的时候，可以只输入一个编号，即从数据库中调取该书所有信息
    def __init__(self,no):     #输入图书编号
        self.bk_name = None
        self.bk_no = None
        self.bk_price = None
        self.bk_author = None
        self.bk_type = None
        self.bk_url = None
    
    #打印图书信息
    def __showBookInfo(self):
        self.infoList = [self.bk_name,self.bk_no,self.bk_price,self.bk_author,self.bk_type,self.bk_url]
        for item in infoList:
            print(item)


#图书管理系统类
class book_manage(object):

    #按编号查询图书
    def findBook(self,num):
        num = input("请输入图书编号：")
        if mycursor.execute("select * from book_info where bk_no = 'num'" ):     #此处不确定，num值应该怎么出现在命令行中
            content1 = mycursor.fetchone()
            print(content1)
        else:
            print("您输入的图书编号有误")

    #按类型查询图书
    def findBookList(self,type):
        type = input("请输入图书类型：")
        if mycursor.execute("select * from book_info where bk_type = 'type'" ):
            content1 = mycursor.fetchone()
            print(content1)
        else:
            print("您输入的图书类型有误")

    def delete(self, id):
        pass
    




        
    


        



User1 = User()