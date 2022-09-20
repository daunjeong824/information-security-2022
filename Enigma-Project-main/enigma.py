# Enigma Template Code for CNU Information Security 2022
# Resources from https://www.cryptomuseum.com/crypto/enigma

# This Enigma code implements Enigma I, which is utilized by 
# Wehrmacht and Luftwaffe, Nazi Germany. 
# This version of Enigma does not contain wheel settings, skipped for
# adjusting difficulty of the assignment.

from copy import deepcopy
from ctypes import ArgumentError

# Enigma Components
# entry disc (input)
ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

WHEELS = {
    "I" : {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", # wheel 원판 순서
        "mapped": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "turn": 21 # 현재 wheel 위치가 turn 도달 시, 다음 wheel로..
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "mapped": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "turn": 21
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",   
        "mapped": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "turn": 21
    }
}
# Reflector
UKW = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

# Enigma Settings
SETTINGS = {
    "UKW": None,
    "WHEELS": [],
    "WHEEL_POS": [],
    "ETW": ETW,
    "PLUGBOARD": []
}

def apply_settings(ukw, wheel, wheel_pos, plugboard):
    if not ukw in UKW: # 반사판 A,B,C 중 하나 고르기
        raise ArgumentError(f"UKW {ukw} does not exist!")
    SETTINGS["UKW"] = UKW[ukw]

    wheels = wheel.split(' ') # 로터 I, II, III 순서 정하기 
    for wh in wheels: 
        if not wh in WHEELS:
            raise ArgumentError(f"WHEEL {wh} does not exist!")
        SETTINGS["WHEELS"].append(WHEELS[wh])

    wheel_poses = wheel_pos.split(' ') # 해당 로터 wire에서 shift 위치 정하기
    for wp in wheel_poses:
        if not wp in ETW:
            raise ArgumentError(f"WHEEL position must be in A-Z!")
        SETTINGS["WHEEL_POS"].append(ord(wp) - ord('A'))
    
    plugboard_setup = plugboard.split(' ') # 플러그 설정
    for ps in plugboard_setup:
        if not len(ps) == 2 or not ps.isupper():
            raise ArgumentError(f"Each plugboard setting must be sized in 2 and caplitalized; {ps} is invalid")
        SETTINGS["PLUGBOARD"].append(ps)

# Enigma Logics Start

# Plugboard
def pass_plugboard(input):
    for plug in SETTINGS["PLUGBOARD"]:
        if str.startswith(plug, input):
            return plug[1]
        elif str.endswith(plug, input):
            return plug[0]

    return input

# ETW
def pass_etw(input):
    return SETTINGS["ETW"][ord(input) - ord('A')]

# Wheels
def pass_wheels(input, reverse = False):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order
    if reverse:
        # 0 -> 1 -> 2
        input_idx = SETTINGS["ETW"].find(input)
        right_reverse = SETTINGS["WHEELS"][0]["mapped"][input_idx]
        right_reverse_index = SETTINGS["WHEELS"][0]["wire"].index(right_reverse) # Z의 index, M번째, idx = 12
        
        middle_reverse = SETTINGS["WHEELS"][1]["mapped"][right_reverse_index] # mapped idx = 12, M
        middle_reverse_index = SETTINGS["WHEELS"][1]["wire"].index(middle_reverse) # 2nd wheel의 M의 index

        left_reverse = SETTINGS["WHEELS"][2]["mapped"][middle_reverse_index] # mapped idx = 15
        left_reverse_index = SETTINGS["WHEELS"][2]["wire"].index(left_reverse)

        return SETTINGS["ETW"][left_reverse_index]

    else:
        # 2 -> 1 -> 0
        input_index = SETTINGS["ETW"].index(input)
        left_wheel_mapped = SETTINGS["WHEELS"][2]["wire"][input_index]
        
        middle_index = SETTINGS["WHEELS"][2]["mapped"].index(left_wheel_mapped)
        middle_wheel_mapped = SETTINGS["WHEELS"][1]["wire"][middle_index]
        #print(SETTINGS["WHEELS"][1]["wire"], middle_wheel_mapped)

        right_index = SETTINGS["WHEELS"][1]["mapped"].index(middle_wheel_mapped)
        right_wheel_mapped = SETTINGS["WHEELS"][0]["wire"][right_index]
        
        final_index = SETTINGS["WHEELS"][0]["mapped"].index(right_wheel_mapped)
        return SETTINGS["ETW"][final_index]

def update_index(idx, pos):
    if idx > 0:
        return idx - pos

# UKW
def pass_ukw(input):
    return SETTINGS["UKW"][ord(input) - ord('A')]

# Wheel Rotation (wheel의 위치에 따라 caesar 암호 적용?)
def rotate_wheels():
    # Implement Wheel Rotation Logics => 시계처럼 변경
    # 1. SETTING Wheel 
    global pos_first, pos_sec, pos_third

    # 2. first wheel rotate
    SETTINGS["WHEELS"][2]["wire"] = SETTINGS["WHEELS"][2]["wire"][1:] + SETTINGS["WHEELS"][2]["wire"][:1]
    SETTINGS["WHEELS"][2]["mapped"] = SETTINGS["WHEELS"][2]["mapped"][1:] + SETTINGS["WHEELS"][2]["mapped"][:1]
    SETTINGS["WHEEL_POS"][2] = update_wheel_count(SETTINGS["WHEEL_POS"][2])
    pos_first += 1
    
    
    # 3. second wheel rotate (1째 wheel이 다 돌면 +1)
    if pos_first % SETTINGS["WHEELS"][2]["turn"] == 0:
        SETTINGS["WHEELS"][1]["wire"] = SETTINGS["WHEELS"][1]["wire"][1:] + SETTINGS["WHEELS"][1]["wire"][:1]
        SETTINGS["WHEELS"][1]["mapped"] = SETTINGS["WHEELS"][1]["mapped"][1:] + SETTINGS["WHEELS"][1]["mapped"][:1]
        SETTINGS["WHEEL_POS"][1] = update_wheel_count(SETTINGS["WHEEL_POS"][1])
        pos_sec += 1
       
        # 4. third wheel rotate (2쨰 wheel이 다 돌면 +1)
        if pos_sec % SETTINGS["WHEELS"][1]["turn"] == 0 and pos_sec != 0:
            SETTINGS["WHEELS"][0]["wire"] = SETTINGS["WHEELS"][0]["wire"][1:] + SETTINGS["WHEELS"][0]["wire"][:1]
            SETTINGS["WHEELS"][0]["mapped"] = SETTINGS["WHEELS"][0]["mapped"][1:] + SETTINGS["WHEELS"][0]["mapped"][:1]
            SETTINGS["WHEEL_POS"][0] = update_wheel_count(SETTINGS["WHEEL_POS"][0])
            pos_third += 1

def update_wheel_count(current_wheel_pos):
    if current_wheel_pos > 0:
        return current_wheel_pos - 1
    else:
        return 25

'''def shift(letter, shift, alphabet):
    for i in range(0, len(alphabet)):
        if alphabet[i] == letter:
            return alphabet[(i+shift) % len(alphabet)] '''

# Enigma Exec Start
plaintext = input("Plaintext to Encode: ")
ukw_select = input("Set Reflector (A, B, C): ")
wheel_select = input("Set Wheel Sequence L->R (I, II, III): ") # 1. wheel 종류 택
wheel_pos_select = input("Set Wheel Position L->R (A~Z): ") # 2. wheel 설정(위치)
plugboard_setup = input("Plugboard Setup: ") # 3. 플러그 연결

apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)

pos_first = 0
pos_sec = 0
pos_third = 0
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# wheel position 만큼 wheel wire 조정
for i in range(2,-1,-1):
    to_shfit = SETTINGS["WHEEL_POS"][i]
    if to_shfit == 0:
        continue
    temp_wire = SETTINGS["WHEELS"][i]["wire"]
    wire = temp_wire[to_shfit:] + temp_wire[:to_shfit]
    SETTINGS["WHEELS"][i]["wire"] = wire
    #print(i, "RD WHELL WIRE SETTING COMPLETED : ", SETTINGS["WHEELS"][i]["wire"])
res = ""
for ch in plaintext:
    rotate_wheels()

    encoded_ch = ch

    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse = True)
    encoded_ch = pass_plugboard(encoded_ch)

    res += encoded_ch
print("encoded plaintext : ",res)
