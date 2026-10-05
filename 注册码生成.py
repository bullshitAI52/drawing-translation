import hashlib

def generate_registration_code(machine_code):
    # 对机器码进行两次加密以生成注册码
    intermediate_code = hashlib.sha256(machine_code.encode()).hexdigest()
    registration_code = hashlib.sha256(intermediate_code.encode()).hexdigest()
    return registration_code

def main():
    machine_code ='填入自己的机器码'
    registration_code = generate_registration_code(machine_code)
    print("生成的注册码为:", registration_code)

if __name__ == "__main__":
    main()
