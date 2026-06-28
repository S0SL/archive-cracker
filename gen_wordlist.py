import itertools

base_date = '19980211'
base_name = 'shenling'
parts = ['shen', 'ling', 'shenling']

end_punct = ['', '.', ',', '?', '!', '~', "'", '"', ';', ':', ')', '>', '^']
start_punct = ['', '.', ',', '?', '!', '~', "'", '"', '(', '<', '@', '#', '$', '*']

passwords = set()

# 核心组合：名字 + 日期
core = [
    'shenling19980211', 'shenling980211', 'shenling1998',
    'shenling0211', 'shenling02111998', 'shenling021198',
    'ShenLing19980211', 'ShenLing980211', 'ShenLing1998',
    'shenLing19980211', 'shenLing980211',
    'SHENLING19980211', 'SHENLING980211', 'SHENLING1998',
    '19980211shenling', '980211shenling', '1998shenling',
    '02111998shenling', '0211shenling', '021198shenling',
    '19980211ShenLing', '980211ShenLing', '1998ShenLing',
    'shenling', 'ShenLing', 'shenLing', 'SHENLING', 'shen ling',
    'sl19980211', 'sl980211', 'SL19980211', 'SL980211',
    'shenling123', 'ShenLing123', 'shenling!', 'ShenLing!',
    'shenling@', 'ShenLing@', 'shenling#', 'ShenLing#',
]

# 分隔符组合
seps = ['', '_', '-', '.', '@']
date_shorts = ['19980211', '980211', '1998', '0211', '02111998', '021198']
name_vars = ['shenling', 'ShenLing', 'shenLing', 'SHENLING', 'shen ling']

for s in seps:
    for n in name_vars:
        for d in date_shorts:
            core.append(f'{n}{s}{d}')
            core.append(f'{d}{s}{n}')

# sl 缩写
core.extend(['sl98', 'sl980211', 'SL98', 'SL980211'])

# 数字后缀
for c in core[:]:
    for n in ['123', '456', '789', '666', '888', '520', '1314', '0']:
        core.append(f'{c}{n}')

# 日期倒序
core.extend(['11021998', '110298', '11-02-1998'])

# 先收集所有基础密码
for c in core:
    passwords.add(c)

# 只对最常见的组合加符号（控制数量）
symbol_base = []
for c in core:
    if len(c) <= 20:
        symbol_base.append(c)

for pw in symbol_base:
    for p in end_punct:
        if p:
            passwords.add(f'{pw}{p}')
    for p in start_punct:
        if p:
            passwords.add(f'{p}{pw}')

sorted_passwords = sorted(passwords, key=lambda x: (len(x), x))

with open('target_wordlist.txt', 'w', encoding='utf-8') as f:
    for pw in sorted_passwords:
        f.write(pw + '\n')

print(f'生成了 {len(sorted_passwords)} 个密码组合')
print('已保存到 target_wordlist.txt')
