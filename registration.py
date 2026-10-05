import hashlib
import os

def get_machine_code():
    # 示例：使用环境变量生成一个简单的机器码
    raw_code = os.environ.get('USER', 'default_user') + os.environ.get('COMPUTERNAME', 'default_computer')
    return hashlib.sha256(raw_code.encode()).hexdigest()[:15]

def generate_registration_code(machine_code):
    # 示例：对机器码进行两次加密以生成注册码
    intermediate_code = hashlib.sha256(machine_code.encode()).hexdigest()
    registration_code = hashlib.sha256(intermediate_code.encode()).hexdigest()
    return registration_code

def is_registered():
    # 示例：检查是否已注册
    try:
        with open('registration.txt', 'r') as file:
            stored_code = file.read().strip()
            return stored_code == generate_registration_code(get_machine_code())
    except FileNotFoundError:
        return False

def register(registration_code):
    # 示例：验证并保存注册码
    if registration_code == generate_registration_code(get_machine_code()):
        with open('registration.txt', 'w') as file:
            file.write(registration_code)
        return True
    return False
