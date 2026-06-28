import itertools
import random


class PasswordGenerator:
    LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
    UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    DIGITS = '0123456789'
    SYMBOLS = '!@#$%^&*()_+-=[]{}|;:,.<>?'
    
    def __init__(self):
        self.charset = self.LOWERCASE + self.UPPERCASE + self.DIGITS
        self.min_length = 6
        self.max_length = 12
        self.patterns = []
        
    def set_charset(self, lowercase=True, uppercase=True, digits=True, symbols=False, custom=""):
        self.charset = ""
        if lowercase:
            self.charset += self.LOWERCASE
        if uppercase:
            self.charset += self.UPPERCASE
        if digits:
            self.charset += self.DIGITS
        if symbols:
            self.charset += self.SYMBOLS
        if custom:
            self.charset += custom
    
    def set_length(self, min_len, max_len):
        self.min_length = min_len
        self.max_length = max_len
    
    def generate_random(self, count=1000, output_file=None):
        passwords = []
        for _ in range(count):
            length = random.randint(self.min_length, self.max_length)
            pw = ''.join(random.choice(self.charset) for _ in range(length))
            passwords.append(pw)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(passwords))
        
        return passwords
    
    def generate_pattern(self, name_parts, date_parts, separators=['', '_', '-', '.']):
        passwords = set()
        
        for name in name_parts:
            for date in date_parts:
                for sep in separators:
                    passwords.add(f'{name}{sep}{date}')
                    passwords.add(f'{date}{sep}{name}')
                    
                    for s in separators:
                        if s != sep:
                            passwords.add(f'{name}{s}{date}')
        
        return list(passwords)
    
    def apply_rules(self, passwords, rules):
        result = list(passwords)
        
        for rule in rules:
            new_passwords = []
            for pw in result:
                if rule == 'capitalize':
                    new_passwords.append(pw.capitalize())
                elif rule == 'upper':
                    new_passwords.append(pw.upper())
                elif rule == 'lower':
                    new_passwords.append(pw.lower())
                elif rule == 'append_numbers':
                    for i in range(10):
                        new_passwords.append(f'{pw}{i}')
                elif rule == 'append_symbols':
                    for s in '!@#$%^&*':
                        new_passwords.append(f'{pw}{s}')
                elif rule == 'leet':
                    leet_map = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5'}
                    leet_pw = pw
                    for k, v in leet_map.items():
                        leet_pw = leet_pw.replace(k, v)
                    new_passwords.append(leet_pw)
                else:
                    new_passwords.append(pw)
            
            result = new_passwords
        
        return result
    
    def generate_from_clues(self, clues, output_file=None):
        passwords = set()
        
        for clue in clues:
            if clue['type'] == 'pattern':
                passwords.update(self.generate_pattern(
                    clue.get('names', []),
                    clue.get('dates', []),
                    clue.get('separators', ['', '_', '-'])
                ))
            elif clue['type'] == 'base':
                base = clue['value']
                passwords.add(base)
                passwords.add(base.capitalize())
                passwords.add(base.upper())
                passwords.add(base.lower())
                
                for i in range(10):
                    passwords.add(f'{base}{i}')
                    passwords.add(f'{i}{base}')
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(sorted(passwords)))
        
        return list(passwords)
