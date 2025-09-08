def GetValue(line) -> str:
    return line.split('"')[3]


def Calc(ov: str, mul: int | float | str) -> str:
    if isinstance(mul, str):
        if '=' in mul:
            return str(mul.split('=')[-1])
        if '+' in mul or '-' in mul or '*' in mul or '/' in mul:
            return str(eval(f"{ov}{mul}"))
        return str(eval(f"{ov}*{mul}"))
    return str(int(int(ov) * mul))


class NpcUnit:
    def __init__(self, path):
        self.path = path
        with open(self.path, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

    def UpdateXP(self, xp: int | float | str):
        lines = self.lines.copy()
        for i, line in enumerate(self.lines):
            if '"BountyXP"' in line:
                ov = GetValue(line)
                v = Calc(ov, xp)
                line2 = line.replace(ov, v)
                lines[i] = line2
                print(i + 1, line2, end='')
        self.lines = lines

    def UpdateGold(self, gold: int | float | str):
        lines = self.lines.copy()
        for i, line in enumerate(self.lines):
            if '"BountyGoldMin"' in line or '"BountyGoldMax"' in line:
                ov = GetValue(line)
                v = Calc(ov, gold)
                line2 = line.replace(ov, v)
                lines[i] = line2
                print(i + 1, line2, end='')
        self.lines = lines

    def UpdateTowerHpAndRegen(self, hp: int | float | str, regen: int | float | str):
        names = ['tower1', 'tower2', 'tower3']
        lines = self.lines.copy()
        for i, line in enumerate(self.lines):
            for name in names:
                if name in line:
                    print(i + 1, line, end='')
                    for i2, line2 in enumerate(self.lines[i:], i):
                        if '"StatusHealth"' in line2:
                            ov = GetValue(line2)
                            v = Calc(ov, hp)
                            line3 = line2.replace(ov, v)
                            lines[i2] = line3
                            print(i2 + 1, line3, end='')
                        if '"StatusHealthRegen' in line2:
                            ov = GetValue(line2)
                            v = Calc(ov, regen)
                            line3 = line2.replace(ov, v)
                            lines[i2] = line3
                            print(i2 + 1, line3, end='')
                        if '\t}' in line2:
                            break
        self.lines = lines

    def UpdateFortHpAndRegen(self, hp: int | float | str, regen: int | float | str):
        names = ['npc_dota_goodguys_fort', 'npc_dota_badguys_fort']
        lines = self.lines.copy()
        for i, line in enumerate(self.lines):
            for name in names:
                if name in line:
                    print(i + 1, line, end='')
                    for i2, line2 in enumerate(self.lines[i:], i):
                        if '"StatusHealth"' in line2:
                            ov = GetValue(line2)
                            v = Calc(ov, hp)
                            line3 = line2.replace(ov, v)
                            lines[i2] = line3
                            print(i2 + 1, line3, end='')
                        if '"StatusHealthRegen' in line2:
                            ov = GetValue(line2)
                            v = Calc(ov, regen)
                            line3 = line2.replace(ov, v)
                            lines[i2] = line3
                            print(i2 + 1, line3, end='')
                        if '\t}' in line2:
                            break
        self.lines = lines

    def Write(self, write_path):
        with open(write_path, 'w', encoding='utf-8') as f:
            f.writelines(self.lines)

    def Reset(self):
        self.__init__(self.path)


if __name__ == '__main__':
    UN = NpcUnit(r'C:\Users\Jeremy\Desktop\d3\npc\npc_units.txt')
    UN.UpdateXP('2')
    UN.UpdateGold('2')
    UN.UpdateTowerHpAndRegen('1', '1')
    UN.UpdateFortHpAndRegen('1', '1')
    UN.Write(r'C:\Users\Jeremy\Desktop\d3\vpk\pak01_dir\scripts\npc\npc_units.txt')
