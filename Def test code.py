
with open('Sensor_Info.txt', 'r') as f:
    lines = f.readlines()

print(lines[4])

if lines[4][-4] == 'x':
    d = lines[5][-3:-1]
    print(d)



# 0x 이후의 문자를 인덱스 하려면 아래의 방법이 좋다

with open('Sensor_Info.txt', 'r') as f:
    lines = f.readlines()

print(lines[4])

# '0x' 가 포함된 줄인지 확인
if '0x' in lines[4]:
    # '0x' 이후의 두 문자 추출
    start_index = lines[4].index('0x')
    d = lines[4][start_index:start_index + 2]
    print(d)
else :
    print('조건이 충족되지 않았습니다')



