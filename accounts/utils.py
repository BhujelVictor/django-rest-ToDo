import math, random
 
#generate OTP
class Util:
    @staticmethod
    def generateOTP() :
    
        # Declare a string variable  
        # which stores all string 
        string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        otp = ""
        length = len(string)
        for i in range(6) :
            otp += string[math.floor(random.random() * length)]
    
        return otp