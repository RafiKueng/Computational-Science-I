#--------------------------------------------------------------------------
# RSA encrypt / decrypt / brute force crack
#--------------------------------------------------------------------------
# Explanation:
#   
#
# How this code works 
#
#
# Notes / Convention:
#
#--------------------------------------------------------------------------
# Rafael Kueng
# v1
# 
# BUGS / TODO:
#
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# SETTINGS
#--------------------------------------------------------------------------

def encrypt(msg, N, c):
    return pow(msg, c, N)
    
def decrypt(msg, N, d):
    return pow(msg, d, N)
    
    
def encode(plain_word):
	enc_word = 0
	for i, c in enumerate(plain_word):
		if c < "a" or c > "z": c = "{"
		enc_word += (ord(c) - 96)*32**i
	return enc_word
    
    
def decode(enc_word):
	plain_word = ""
	while enc_word > 0:
		c = chr(enc_word % 32 + 96)
		if c < "a" or c > "z": c = " "
		plain_word += c
		enc_word /= 32
    return plain_word
    
def gen_key():
	return 0