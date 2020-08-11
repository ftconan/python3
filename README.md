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
### data structures
1. list is not the only answer(arrays, memoryview, numpy and scipy, deque, asyncio, multiprocessing)

### function as object
1. list comprehension can replace (map, filter, reduce function)
2. reduce is not built-in function in Python3(from fuctools import reduce)
3. decorators

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
