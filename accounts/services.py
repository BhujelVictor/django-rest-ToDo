import random

class GenOTP:
    @staticmethod
    def generate_otp():
        return random.randint(1000, 9999)
