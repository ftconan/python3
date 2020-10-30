# Python3

Python3 study notes

- [Python3](#python3)
    - [python3 practice](#python3-practice)
    - [python start](#python-start)
    - [python machine algorithm](#python-machine-algorithm)
    - [Numpy](#Numpy)
    - [Fluent Python](#Fluent-Python)
    - [Python Tricks](#Python-Tricks)
    - [Effective Python](#Effective-Python)
    - [Python Tricks](#Python-Tricks)
    - [leetcode](#leetcode)
    - [flask tutorial](#flask-tutorial)
    - [flask restful](#flask-restful)
    - [marshmallow](#marshmallow)
    - [flask sqlalchemy](#flask-sqlalchemy)
    - [SQLAlchemy documentation](#SQLAlchemy-documentation)
    - [flask mail](#flask-mail)
---

## python3 practice
1.  Hello World!
2.  number game
3.  string method(built-in)
4.  sequence method(list，tuple built-in)
5.  function
6.  dict
7.  file
8.  pickle
9.  inherit(fish)
10. timer
11. craw youdao dictionary translation
12. proxy ip select
13. html -> pdf(xhtml2pdf)

## python start
1. remove ad text
2. 21 point#

## python machine algorithm
1. KNN

## Numpy
1. description
2. array structure

## python core skill
1. lambda demo
2. class demo
3. search_engine demo
4. decorator demo
5. metaclass demo
6. iterator generator demo
7. coroutine demo <b>(python3.7+!!!)</b>
8. futures demo
9. asyncio demo
10. GIL demo
11. gl demo
12. context demo
13. unit demo
14. qt_demo
15. qt_crawler

## Fluent Python
### 1. Python数据类型
1. 一摞Python风格的纸牌
2. 如何使用特殊方法 
3. 特殊方法一览
4. 为什么len不是普通方法
5. 本章小结
6. 延伸阅读
### 2. 序列化构成数组
1. 内置序列类型概览
2. 列表推导和生成器表达式 
3. 元组不仅仅是不可变的列表
4. 切片
5. 对序列使用+和*
6. 序列的增量赋值
7. list.sort方法和内置函数sorted
8. 用bisect来管理已排序的序列
9. 当列表不是首选
10. 本章小结
11. 延伸阅读
### 3. 字典和集合
1. 泛映射类型
2. 字典推导
3. 常见映射类型方法
4. 映射的弹性键查询
5. 字典的变种
6. 子类化UserDict
7. 不可变映射类型
8. 集合论 
9. dict和set的背后
10. 本章小结
11. 延伸阅读
### 4. 文本和字节序列
1. 字符问题
2. 字节概要
3. 基本的编解码器
4. 了解编解码问题
5. 处理文本文件
6. 为了正确比较而规范化Unicode字符串
7. Unicode文本排序
8. Unicode数据库 
9. 支持字符串和字节序列的双模式API
10. 本章小结
11. 延伸阅读
### 5. 一等函数
1. 把函数视为对象
2. 高阶函数
3. 匿名函数
4. 可调用对象
5. 用户定义的可调用类型
6. 函数内省
7. 从定位参数到仅限关键字参数
8. 获取关于参数的信息 
9. 函数注解
10. 本章小结
11. 延伸阅读
### 6. 使用一等函数实现设计模式
1. 案例分析：重构“策略”模式
2. “命令”模式
3. 本章小结
4. 延伸阅读
### 7. 函数装饰器和闭包
1. 装饰器基础知识
2. Python何时执行装饰器
3. 使用装饰器改进“策略”模式
4. 变量作用域规则
5. 闭包
6. nonlocal声明
7. 实现一个简单的装饰器
8. 标准库中的装饰器 
9. 叠放装饰器
10. 参数化装饰器
11. 本章小结
12. 延伸阅读
### 8. 对象引用、可变性和垃圾回收
1. 变量不是盒子
2. 标识、相等性和别名
3. 默认做浅复制
4. 函数的参数作为引用时
5. del和垃圾回收
6. 弱引用
7. Python对不可变类型施加的把戏
8. 本章小结 
9. 延伸阅读
### 9. 对象引用、可变性和垃圾回收
1. 对象表示形式
2. 再谈向量类
3. 备选构造方法
4. classmethod与staticmethod
5. 格式化显示
6. 可散列的Vector2d
7. Python的私有属性和“受保护的”属性
8. 使用 __slots__ 类属性节省空间
9. 覆盖类属性 
10. 本章小结 
11. 延伸阅读
### 10. 序列的修改、散列和切片
1. Vector类：用户定义的序列类型
2. Vector类第1版：与Vector2d类兼容
3. 协议和鸭子类型
4. Vector类第2版：可切片的序列
5. Vector类第3版：动态存取属性
6. Vector类第4版：散列和快速等值测试
7. Vector类第5版：格式化
8. 本章小结
9. 延伸阅读

## Python Tricks
### 1. Introduction
### 2. Patterns for Cleaner Python
 1. Covering Your A** With Assertions
 2. Complacent Comma Placement
 3. Context Managers and the with Statement
 4. Underscores, Dunders, and More
 5. A Shocking Truth About String Formatting
 6. “The Zen of Python” Easter Egg
### 3. Effective Function 
 1. Python’s Functions Are First-Class
 2. Lambdas Are Single-Expression Functions
 3. The Power of Decorators
 4. Fun With *args and **kwargs
 5. Function Argument Unpacking
 6. Nothing to Return Here
### 4. Classes & OOP
 1. Object Comparisons: “is” vs “==”
 2. String Conversion (Every Class Needs a __repr__)
 3. Defining Your Own Exception Classes
 4. Cloning Objects for Fun and Profit
 5. Abstract Base Classes Keep Inheritance in Check
 6. What Namedtuples Are Good For
 7. Class vs Instance Variable Pitfalls
 8. Instance, Class, and Static Methods Demystified
### 5. Common Data Structures in Python
 1. Dictionaries, Maps, and Hashtables
 2. Array Data Structures
 3. Records, Structs, and Data Transfer Objects
 4. Sets and Multisets
 5. Stacks (LIFO)
 6. Queues (FIFOs)
 7. Priority Queues
### 6. Looping & Iteration
 1. Writing Pythonic Loops
 2. Comprehending Comprehensions
 3. List Slicing Tricks and the Sushi Operator
 4. Beautiful Iterators
 5. Generators Are Simplified Iterators
 6. Generator Expressions
 7. Iterator Chains
### 7. Dictionary Tricks
 1. Dictionary Default Values
 2. Sorting Dictionaries for Fun and Profit
 3. Emulating Switch/Case Statements With Dicts
 4. The Craziest Dict Expression in the West
 5. So Many Ways to Merge Dictionaries
 6. Dictionary Pretty-Printing
### 8. Pythonic Productivity Techniques
 1. Exploring Python Modules and Objects
 2. Isolating Project Dependencies With Virtualenv
 3. Peeking Behind the Bytecode Curtain
### 9. Closing Thoughts

## Effective Python
### 1. 用Pythonic方式思考
 1. 确认自己所用的python版本
 2. 遵循PEP8风格之南
 3. 了解bytes,str与unicode的区别
 4. 用辅助函数来取代复杂的表达式
 5. 了解切割序列的方法
 6. 在单次切片操作内，不要同时指定start，end，和stride
 7. 用列表推导来取代map和filter
 8. 不要使用含有两个以上表达式的列表推导
 9. 用生成器表达式来改写数据量较大的列表推导式
 10. 尽量用enumerate取代range
 11. 用zip函数同时遍历两个迭代器
 12. 不要在for和while循环后面写else块
 13. 合理利用try/except/else/finally结构中的每个代码块
### 2. 函数
 14. 尽量用异常来表示特殊情况，而不要返回None
 15. 了解如何在闭包里使用外围作用域中的变量
 16. 考虑用生成器来改写直接返回列表的函数
 17. 在参数上面迭代时，要多加小心
 18. 用数量可变的位置参数减少视觉杂讯
 19. 用关键字参数来表达可选的行为
 20. 用None和文档字符串来描述具体动态默认值的参数
 21. 用只能以关键字形式指定的参数来确保代码明晰
### 3. 类与继承
 22. 尽量用辅助类来维护程序的状态，而不要用字典和元组
 23. 简单的接口应该接受函数，而不是类的实例
 24. 以@classmethod形式的多态去通用地构建对象
 25. 用super初始化父类
 26. 只在使用Min-in组件制作工具类时进行多重继承
 27. 多用public属性，少用private属性
 28. 继承collection.abc以实现自定义容器类型
### 4. 元类及属性
 29. 用纯属性取代get和set方法
 30. 考虑用@property来代替属性重构
 31. 用描述符来改写需要复用的@property方法
 32. 用__getattr__，__getattribute__和__setattr__实现按需生成的属性
 33. 用元类来验证子类
 34. 用元类来注册子类
 35. 用元类来注解类的属性
### 5. 并发和并行
 36. 用subprocess模块来管理子进程
 37. 可以用线程来执行阻塞式I/O，但不要用它做平行计算
 38. 在线程中使用Lock来防止数据竞争
 39. 用Queue来协调各线程之间的工作
 40. 考虑用协程来并发地运行多个函数
 41. 考虑用concurrent.futures来实现真正的平行计算
### 6. 内置模块
 42. 用functools.wraps定义函数修饰器
 43. 考虑以contextlib和with语句来改写可复用的try/finally代码
 44. 用copyreg实现可靠的pickle操作
 45. 应该用datetime模块来处理本地时间,而不是time模块
 46. 使用内置算法和数据结构
 47. 在重视精确度的场合，应该使用decimal
 48. 学会安装由Python开发者社区所构建的模块
### 7. 协作开发
 49. 为每个函数、类和模块编写文档字符串
 50. 用包来安排模块，并提供稳固的的API
 51. 为自编的模块定义根异常，以便将调用者与API相隔离
 52. 用适当的方式打破循环依赖的关系
 53. 用虚拟环境隔离项目，并重建其依赖关系
### 8. 部署
 54. 考虑用模块级别的代码来配置不同的部署环境
 55. 通过repr字符串来输出调试信息
 56. 用unittest来测试全部代码
 57. 考虑用pdb实现交互调试
 58. 先分析性能，然后再优化
 59. 用tracemalloc来掌握内存的使用及泄漏情况
 

## leetcode
### 算法
1. 两数之和
2. 整数反转
3. 回文数
4. 罗马数字转整数
5. 最长公共前缀
6. 有效的括号
7. 删除排序数组中的重复项
8. 移除元素
9. 实现 strStr()
10. 加一
11. 最后一个单词的长度
12. x 的平方根
13. 二进制求和
14. 搜索插入位置
15. 只出现一次的数字
16. 合并两个有序数组
17. 多数元素
18. 快乐数
19. 旋转数组
20. 2的幂
21. 各位相加
22. 缺失数字
23. 3的幂

# flask-tutorial
### Tutorial
  * Project Layout
  * Application Setup(Linux and Mac)
    1. export FLASK_APP=flaskr
    2. export FLASK_ENV=development
    3. flask run
  * Define and Access the Database
    1. flask init-db
  * Blueprints and Views
  * Templates
  * Blog Blueprint
  * Make the Project Installable
    1. venv\Scripts\activate
    2. pip install -e .
    3. pip list
  * Test Coverage
    1. coverage run -m pytest
    2. coverage report
    3. coverage html
  * Deploy to Production
    1. pip install wheel
    2. python setup.py bdist_wheel
    3. pip install flaskr-1.0.0-py3-none-any.whl
    4. export FLASK_APP=flaskr
    5. flask init-db
  * Keep Developing!
  * Templates
  * Testing Flask Applications
    1. pip install pytest
  * Application Errors
  * Debugging Application Errors
 

## flask-restful
  * Quickstart
  * Request Parsing(marshmallow: deserializing objects(loading))
  * Output Fields(marshmallow: serializing objects(dumping))
  * Extending Flask-RESTful
  * Intermediate Usage

## marshmallow
  * Quickstart
  * nesting schemas
  * extending schemas
  * examples

## flask-sqlalchemy
  * Quickstart
  * Introduction into Contexts(init_app)
  * Configuration(SQLAlchemy configuration)
  * Declaring Models
  * Select, Insert, Delete
  * Multiple Databases with Binds(SQLALCHEMY_BINDS, bind, __bind_key__)
  * Signalling Support
  * Customizing
    1. Model Class(db = SQLAlchemy(model_class=IdModel))
    2. Model Mixins(class Post(TimestampMixin, db.Model))
    3. Query Class(db = SQLAlchemy(query_class=GetOrQuery))
    4. Model Metaclass(db = SQLAlchemy(model_class=declarative_base(cls=Model, metaclass=CustomMeta, name='Model')))
  
## SQLAlchemy-documentation
### Object Relational Tutorial
  
## flask-mail
  * Quickstart

## requirement.txt
  * pip freeze > requirements.txt
  * pip install -r requirements.txt
