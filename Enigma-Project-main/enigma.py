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
        "turn": 2 # 현재 wheel 위치가 turn 도달 시, 다음 wheel로..
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "turn": 4
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
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

    wheel_poses = wheel_pos.split(' ') # 해당 로터에서, 통과시킬 위치 정하기
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
    # Implement Wheel Logics ()
    # Keep in mind that reflected signals pass wheels in reverse order
    if reverse:
        # 0 -> 1 -> 2
        pass
    else:
        # 2 -> 1 -> 0
        pass
    return input

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
    SETTINGS["WHEEL_POS"][2] = update_wheel_count(SETTINGS["WHEEL_POS"][2], SETTINGS["WHEELS"][2]["turn"])
    pos_first += 1
    
    # 3. second wheel rotate (1째 wheel이 다 돌면 +1)
    if pos_first % SETTINGS["WHEELS"][2]["turn"] == 0:
        SETTINGS["WHEELS"][1]["wire"] = SETTINGS["WHEELS"][1]["wire"][1:] + SETTINGS["WHEELS"][1]["wire"][:1]
        SETTINGS["WHEEL_POS"][1] = update_wheel_count(SETTINGS["WHEEL_POS"][1], SETTINGS["WHEELS"][1]["turn"])
        pos_sec += 1
       
        # 4. third wheel rotate (2쨰 wheel이 다 돌면 +1)
        if pos_sec % SETTINGS["WHEELS"][1]["turn"] == 0 and pos_sec != 0:
            SETTINGS["WHEELS"][0]["wire"] = SETTINGS["WHEELS"][0]["wire"][1:] + SETTINGS["WHEELS"][0]["wire"][:1]
            SETTINGS["WHEEL_POS"][0] = update_wheel_count(SETTINGS["WHEEL_POS"][0], SETTINGS["WHEELS"][0]["turn"])
            pos_third += 1

def update_wheel_count(current_wheel_pos, wheel_turn):
    if current_wheel_pos < wheel_turn:
        return current_wheel_pos + 1
    else:
        return 0
    

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

for ch in plaintext:
    rotate_wheels()

    encoded_ch = ch

    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse = True)
    encoded_ch = pass_plugboard(encoded_ch)

    print(encoded_ch, end='')
