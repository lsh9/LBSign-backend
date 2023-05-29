import random


def generate_random_string(length=4):
    """ 生成由数字和小写字母组成的4位签到字符串 """
    number_count = random.randint(0, 4)
    char_count = length - number_count
    # 生成一个随机数列表
    random_list = random.sample(range(0, 10), number_count)
    # 生成一个随机字母列表
    random_char_list = random.sample([chr(i) for i in range(97, 123)], char_count)
    # 将随机数列表和随机字母列表合并
    random_list.extend(random_char_list)
    # 将列表随机排序
    random.shuffle(random_list)
    # 将列表转换为字符串
    random_str = ''.join([str(i) for i in random_list])
    return random_str


def md5(string) -> str:
    """ 生成字符串的md5值 """
    import hashlib
    md5_obj = hashlib.md5()
    md5_obj.update(string.encode("utf-8"))
    return md5_obj.hexdigest()


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            print(func.__name__, "success")
            return func(*args, **kwargs)
        except Exception as e:
            print(func.__name__, "failure")
            print(e)
            return {"success": False}

    wrapper.__name__ = func.__name__
    return wrapper
