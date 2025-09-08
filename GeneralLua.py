class GeneralLua:
    def __init__(self, path):
        self.path = path
        with open(self.path, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

    def UndateOption(self, option: str, value: str):
        lines = self.lines.copy()
        for i, line in enumerate(self.lines):
            if option in line:
                ov = line.split(' = ')[-1].replace(',','').replace('\n', '')
                line2 = line.replace(ov, value)
                lines[i] = line2
                print(i + 1, line2, end='')
                break
        self.lines = lines

    def UpdateBanHero(self, heros: list[str]):
        lines = self.lines.copy()
        m1, m2 = None, None
        for i, line in enumerate(self.lines):
            if 'Customize.Ban = {' in line:
                m1 = i + 1
                for i2, line2 in enumerate(self.lines[i + 1:], i + 1):
                    if '}' in line2:
                        m2 = i2
                        break
        heros2 = [f"\t'{i}',\n" for i in heros]
        n = len(heros2) - len(lines[m1:m2]) + 1
        lines[m1:m2] = [*heros2]
        for i, line in enumerate(lines[m1 - 1:m2 + n], m1 - 1):
            print(i, line, end='')
        self.lines = lines

    def UpdateFriend(self, heros: list[str]):
        lines = self.lines.copy()
        m1, m2 = None, None
        for i, line in enumerate(self.lines):
            if 'Customize.Radiant_Heros = {' in line:
                m1 = i + 1
                for i2, line2 in enumerate(self.lines[i + 1:], i + 1):
                    if '}' in line2:
                        m2 = i2
                        break
        heros2 = [f"\t'{i}',\n" for i in heros]
        n = len(heros2) - len(lines[m1:m2]) + 1
        lines[m1:m2] = [*heros2]
        for i, line in enumerate(lines[m1 - 1:m2 + n], m1 - 1):
            print(i, line, end='')
        self.lines = lines

    def UpdateEnemy(self, heros: list[str]):
        lines = self.lines.copy()
        m1, m2 = None, None
        for i, line in enumerate(self.lines):
            if 'Customize.Dire_Heros = {' in line:
                m1 = i + 1
                for i2, line2 in enumerate(self.lines[i + 1:], i + 1):
                    if '}' in line2:
                        m2 = i2
                        break
        heros2 = [f"\t'{i}',\n" for i in heros]
        n = len(heros2) - len(lines[m1:m2]) + 1
        lines[m1:m2] = [*heros2]
        for i, line in enumerate(lines[m1 - 1:m2 + n], m1 - 1):
            print(i, line, end='')
        self.lines = lines

    def Write(self, write_path):
        with open(write_path, 'w', encoding='utf-8') as f:
            f.writelines(self.lines)

    def Reset(self):
        self.__init__(self.path)


if __name__ == '__main__':
    LUA = GeneralLua(r'C:\Users\Jeremy\Desktop\d3\general.lua')

    LUA.UndateOption('Customize.Localization', '"zh"')
    LUA.UndateOption('Customize.Weak_Hero_Cap', '0')
    LUA.UndateOption('Customize.Allow_Trash_Talk', 'false')
    LUA.UndateOption('Customize.Force_Group_Push_Level', '3')
    LUA.UndateOption('Default_Difficulty', '10')
    LUA.UndateOption('Default_Ally_Scale', '0')

    LUA.UpdateBanHero(['BanHero1', 'BanHero2', 'BanHero3'])
    LUA.UpdateFriend(['Friend1', 'Friend2', 'Friend3', 'Friend4'])
    LUA.UpdateEnemy(['Enemy1', 'Enemy2', 'Enemy3', 'Enemy4', 'Enemy5'])

    LUA.Write(r'C:\Users\Jeremy\Desktop\d3\general_2.lua')
