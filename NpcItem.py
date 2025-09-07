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

class NpcItem:
    def __init__(self, path):
        self.path = path
        with open(self.path, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

    def UpdateItem(self, name: str, attr: dict[str, str]):
        lines = self.lines.copy()
        for i, line in enumerate(self.lines):
            if f'"{name}"' in line:
                print(i + 1, line, end='')
                for i2, line2 in enumerate(self.lines[i:], i):
                    for k, v in attr.items():
                        if f'"{k}"' in line2:
                            ov = GetValue(line2)
                            v = Calc(ov, v)
                            line3 = line2.replace(ov, v)
                            lines[i2] = line3
                            print(i2 + 1, line3, end='')
                    if '\t}' in line2:
                        break
                break
        self.lines = lines

    def Write(self, write_path):
        with open(write_path, 'w', encoding='utf-8') as f:
            f.writelines(self.lines)

    def Reset(self):
        self.__init__(self.path)



if __name__ == '__main__':
    it = NpcItem(r'C:\Users\Jeremy\Desktop\d3\npc\items.txt')
    it.UpdateItem('item_aghanims_shard', {"ItemInitialStockTime": "=0.0", "ItemInitialStockTimeTurbo": "=0.0"})
    it.Write(r'C:\Users\Jeremy\Desktop\d3\vpk\pak01_dir\scripts\npc\items.txt')
