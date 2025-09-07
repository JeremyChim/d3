def GetValue(line) -> str:
    return line.split('"')[3]


class NpcNeutralItem:
    def __init__(self, path):
        self.path = path
        with open(self.path, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

    def UpdateNeutralItem(self, time: list[str]):
        x = 0
        lines = self.lines.copy()
        for i, line in enumerate(self.lines):
            if '"start_time"' in line or '"madstone_no_limit_time"' in line:
                ov = GetValue(line)
                v = time[x]
                line2 = line.replace(ov, v)
                lines[i] = line2
                print(i + 1, line2, end='')
                x += 1
        self.lines = lines

    def Write(self, write_path):
        with open(write_path, 'w', encoding='utf-8') as f:
            f.writelines(self.lines)

    def Reset(self):
        self.__init__(self.path)


if __name__ == '__main__':
    ni = NpcNeutralItem(r'C:\Users\Jeremy\Desktop\d3\npc\neutral_items.txt')
    ni.UpdateNeutralItem(['25:00', '0:00', '5:00', '10:00', '15:00', '20:00'])
    ni.Write(r'C:\Users\Jeremy\Desktop\d3\vpk\pak01_dir\scripts\npc\neutral_items.txt')
