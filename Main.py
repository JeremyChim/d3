import json
import os
import subprocess
import time

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QListView
from PyQt5.QtCore import QStringListModel

from NpcItem import NpcItem
from NpcNeutralItem import NpcNeutralItem
from NpcUnit import NpcUnit
from GeneralLua import GeneralLua
from HeroNameDict import *
from untitled import Ui_Form

version = '0.0.4'


class MainWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        if os.path.exists('config.json'):
            with open('config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {}
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.vpk = os.path.join(self.path, 'vpk', 'vpk.bat')
        self.heroes = os.path.join(self.path, 'npc', 'heroes')
        self.ni = os.path.join(self.path, 'npc', 'neutral_items.txt')
        self.ni_out = os.path.join(self.path, 'vpk', 'pak01_dir', 'scripts', 'npc', 'neutral_items.txt')
        self.un = os.path.join(self.path, 'npc', 'npc_units.txt')
        self.un_out = os.path.join(self.path, 'vpk', 'pak01_dir', 'scripts', 'npc', 'npc_units.txt')
        self.it = os.path.join(self.path, 'npc', 'items.txt')
        self.it_out = os.path.join(self.path, 'vpk', 'pak01_dir', 'scripts', 'npc', 'items.txt')
        self.lua = os.path.join(self.path, 'general.lua')
        self.lua_out = os.path.join(self.path, 'general_2.lua')
        self.NI = NpcNeutralItem(self.ni)
        self.UN = NpcUnit(self.un)
        self.IT = NpcItem(self.it)
        self.LUA = GeneralLua(self.lua)
        self.HeroMod = QStringListModel()
        self.BanMod = QStringListModel()
        self.BanList = []
        self.Team = []
        self.Init()

    def Init(self):
        # 读取配置
        self.gamePath.setText(self.config.get('GamePath')) if self.config.get('GamePath') else None
        self.ni1.setText(self.config.get('Time')[0]) if self.config.get('Time') and len(self.config.get('Time')) > 0 else None
        self.ni2.setText(self.config.get('Time')[1]) if self.config.get('Time') and len(self.config.get('Time')) > 1 else None
        self.ni3.setText(self.config.get('Time')[2]) if self.config.get('Time') and len(self.config.get('Time')) > 2 else None
        self.ni4.setText(self.config.get('Time')[3]) if self.config.get('Time') and len(self.config.get('Time')) > 3 else None
        self.ni5.setText(self.config.get('Time')[4]) if self.config.get('Time') and len(self.config.get('Time')) > 4 else None
        self.ni6.setText(self.config.get('Time')[5]) if self.config.get('Time') and len(self.config.get('Time')) > 5 else None
        self.unXP.setText(self.config.get('unXP')) if self.config.get('unXP') else None
        self.unGold.setText(self.config.get('unGold')) if self.config.get('unGold') else None
        self.unTowerHp.setText(self.config.get('unTowerHp')) if self.config.get('unTowerHp') else None
        self.unTowerRegen.setText(self.config.get('unTowerRegen')) if self.config.get('unTowerRegen') else None
        self.unFortHp.setText(self.config.get('unFortHp')) if self.config.get('unFortHp') else None
        self.unFortRegen.setText(self.config.get('unFortRegen')) if self.config.get('unFortRegen') else None
        self.shardCD.setText(self.config.get('shardCD')) if self.config.get('shardCD') else None
        self.eyeMax.setText(self.config.get('eyeMax')) if self.config.get('eyeMax') else None
        self.eyeInit.setText(self.config.get('eyeInit')) if self.config.get('eyeInit') else None
        self.eye2Max.setText(self.config.get('eye2Max')) if self.config.get('eye2Max') else None
        self.eye2Init.setText(self.config.get('eye2Init')) if self.config.get('eye2Init') else None
        self.eyeCD.setText(self.config.get('eyeCD')) if self.config.get('eyeCD') else None
        self.eye2CD.setText(self.config.get('eye2CD')) if self.config.get('eye2CD') else None
        self.Localization.setText(self.config.get('Localization')) if self.config.get('Localization') else None
        self.Weak_Hero_Cap.setText(self.config.get('Weak_Hero_Cap')) if self.config.get('Weak_Hero_Cap') else None
        self.Allow_Trash_Talk.setText(self.config.get('Allow_Trash_Talk')) if self.config.get('Allow_Trash_Talk') else None
        self.Force_Group_Push_Level.setText(self.config.get('Force_Group_Push_Level')) if self.config.get('Force_Group_Push_Level') else None
        self.Default_Difficulty.setText(self.config.get('Default_Difficulty')) if self.config.get('Default_Difficulty') else None
        self.Default_Ally_Scale.setText(self.config.get('Default_Ally_Scale')) if self.config.get('Default_Ally_Scale') else None
        self.BanList = self.config.get('BanList') if self.config.get('BanList') else []
        self.Team = self.config.get('Team') if self.config.get('Team') else []
        # 控件配置
        self.setWindowTitle('DOTA修改工具')
        self.status.setText(f'当前版本：{version}')
        self.niApply.clicked.connect(self.UpdateNI)
        self.niReset.clicked.connect(self.ResetNI)
        self.save.clicked.connect(self.SaveConfig)
        self.browse.clicked.connect(self.Browse)
        self.unApply.clicked.connect(self.UpdateUn)
        self.unReset.clicked.connect(self.ResetUn)
        self.itApply.clicked.connect(self.UpdateItem)
        self.itReset.clicked.connect(self.ResetItem)
        self.luaWrite.clicked.connect(self.WriteLuaConfig)
        self.VPK.clicked.connect(self.Vpk)
        self.heroView.doubleClicked.connect(self.DoubleClickedHeroView)
        self.banView.doubleClicked.connect(self.DoubleClickedBanView)
        self.HeroMod.setStringList([f'{en:50}{cn}' for en, cn in EN_CN.items()])
        self.heroView.setModel(self.HeroMod)
        self.heroView.setEditTriggers(QListView.NoEditTriggers)  # 禁止编辑
        self.BanMod.setStringList([f'{en:50}{EN_CN.get(en)}' for en in self.BanList])
        self.banView.setModel(self.BanMod)
        self.banView.setEditTriggers(QListView.NoEditTriggers)  # 禁止编辑
        self.BtnList = [self.Friend1, self.Friend2, self.Friend3, self.Friend4, self.Enemy1, self.Enemy2, self.Enemy3, self.Enemy4, self.Enemy5]
        [Btn.clicked.connect(lambda checked, btn=Btn: self.AddTeam(btn)) for Btn in self.BtnList]  # 这里会传两个参数，checked是布尔值参数（表示按钮是否被选中），b是按钮对象
        [Btn.setText(EN_CN.get(self.Team[i])) for i, Btn in enumerate(self.BtnList)] if self.Team else None
        self.TeamReset.clicked.connect(self.ResetTeam)
        self.luaRead.clicked.connect(self.ReadLuaConfig)
        self.luaOpen.clicked.connect(self.OpenLuaConfig)

    def closeEvent(self, event):
        self.config['GamePath'] = self.gamePath.text()
        self.config['Time'] = [self.ni1.text(), self.ni2.text(), self.ni3.text(), self.ni4.text(), self.ni5.text(), self.ni6.text()]
        self.config['unXP'] = self.unXP.text()
        self.config['unGold'] = self.unGold.text()
        self.config['unTowerHp'] = self.unTowerHp.text()
        self.config['unTowerRegen'] = self.unTowerRegen.text()
        self.config['unFortHp'] = self.unFortHp.text()
        self.config['unFortRegen'] = self.unFortRegen.text()
        self.config['shardCD'] = self.shardCD.text()
        self.config['eyeMax'] = self.eyeMax.text()
        self.config['eyeInit'] = self.eyeInit.text()
        self.config['eyeCD'] = self.eyeCD.text()
        self.config['eye2Max'] = self.eye2Max.text()
        self.config['eye2Init'] = self.eye2Init.text()
        self.config['eye2CD'] = self.eye2CD.text()
        self.config['Localization'] = self.Localization.text()
        self.config['Weak_Hero_Cap'] = self.Weak_Hero_Cap.text()
        self.config['Allow_Trash_Talk'] = self.Allow_Trash_Talk.text()
        self.config['Force_Group_Push_Level'] = self.Force_Group_Push_Level.text()
        self.config['Default_Difficulty'] = self.Default_Difficulty.text()
        self.config['Default_Ally_Scale'] = self.Default_Ally_Scale.text()
        self.config['Allow_To_Vote'] = self.Allow_To_Vote.text()
        self.config['Play_Sounds'] = self.Play_Sounds.text()
        self.config['Player_Death_Sound'] = self.Player_Death_Sound.text()
        self.config['BanList'] = self.BanList
        self.config['Team'] = [CN_EN.get(btn.text()) if btn.text() else '' for btn in self.BtnList]
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

    def OpenLuaConfig(self):
        if os.path.exists(self.lua_out):
            os.startfile(self.lua_out)
            time.sleep(1)
            self.status.setText('Lua配置已打开')
        else:
            self.status.setText('Lua配置未找到')

    def ReadLuaConfig(self):
        self.Localization.setText(self.config.get('Localization')) if self.config.get('Localization') else None
        self.Weak_Hero_Cap.setText(self.config.get('Weak_Hero_Cap')) if self.config.get('Weak_Hero_Cap') else None
        self.Allow_Trash_Talk.setText(self.config.get('Allow_Trash_Talk')) if self.config.get('Allow_Trash_Talk') else None
        self.Force_Group_Push_Level.setText(self.config.get('Force_Group_Push_Level')) if self.config.get('Force_Group_Push_Level') else None
        self.Default_Difficulty.setText(self.config.get('Default_Difficulty')) if self.config.get('Default_Difficulty') else None
        self.Default_Ally_Scale.setText(self.config.get('Default_Ally_Scale')) if self.config.get('Default_Ally_Scale') else None
        self.Allow_To_Vote.setText(self.config.get('Allow_To_Vote')) if self.config.get('Allow_To_Vote') else None
        self.Play_Sounds.setText(self.config.get('Play_Sounds')) if self.config.get('Play_Sounds') else None
        self.Player_Death_Sound.setText(self.config.get('Player_Death_Sound')) if self.config.get('Player_Death_Sound') else None
        self.BanList = self.config.get('BanList') if self.config.get('BanList') else []
        self.Team = self.config.get('Team') if self.config.get('Team') else []
        self.BanMod.setStringList([f'{en:50}{EN_CN[en]}' for en in self.BanList])
        [Btn.setText(EN_CN.get(self.Team[i])) for i, Btn in enumerate(self.BtnList)] if self.Team else None
        self.status.setText('Lua配置已读取')

    def ResetTeam(self):
        [Btn.setText('') for Btn in self.BtnList]
        self.status.setText(f'阵容已重置')

    def AddTeam(self, btn):
        index = self.heroView.selectedIndexes()
        if index:
            cho = self.HeroMod.stringList()[index[0].row()].split(' ')[0]
            btn.setText(EN_CN[cho])
            self.status.setText(f'添加：{EN_CN[cho]}')
        else:
            self.status.setText('未选中')

    def DoubleClickedHeroView(self, index):
        cho = self.HeroMod.stringList()[index.row()].split(' ')[0]
        if cho not in self.BanList:
            self.BanList.append(cho)
            self.BanMod.setStringList([f'{en:50}{EN_CN[en]}' for en in self.BanList])
            self.status.setText(f'禁用：{EN_CN[cho]}')
        else:
            self.status.setText(f'已禁用：{EN_CN[cho]}')

    def DoubleClickedBanView(self, index):
        cho = self.BanMod.stringList()[index.row()].split(' ')[0]
        if cho in self.BanList:
            self.BanList.remove(cho)
            self.BanMod.setStringList([f'{en:50}{EN_CN[en]}' for en in self.BanList])
            self.status.setText(f'解禁：{EN_CN[cho]}')

    def WriteLuaConfig(self):
        self.LUA.UndateOption('Customize.Localization', f'"{self.Localization.text()}"')
        self.LUA.UndateOption('Customize.Weak_Hero_Cap', self.Weak_Hero_Cap.text())
        self.LUA.UndateOption('Customize.Allow_Trash_Talk', self.Allow_Trash_Talk.text())
        self.LUA.UndateOption('Customize.Force_Group_Push_Level', self.Force_Group_Push_Level.text())
        self.LUA.UndateOption('Default_Difficulty', self.Default_Difficulty.text())
        self.LUA.UndateOption('Default_Ally_Scale', self.Default_Ally_Scale.text())
        self.LUA.UndateOption('Allow_To_Vote', self.Allow_To_Vote.text())
        self.LUA.UndateOption('Play_Sounds', self.Play_Sounds.text())
        self.LUA.UndateOption('Player_Death_Sound', self.Player_Death_Sound.text())
        self.LUA.UpdateBanHero([EN_FULL.get(en) for en in self.BanList])
        self.LUA.UpdateFriend([CN_FULL.get(btn.text()) if btn.text() else 'Random' for btn in self.BtnList][:4])
        self.LUA.UpdateEnemy([CN_FULL.get(btn.text()) if btn.text() else 'Random' for btn in self.BtnList][4:])
        self.LUA.Write(self.lua_out)
        self.status.setText(f'Lua配置已写入')

    def UpdateItem(self):
        self.IT.UpdateItem('item_aghanims_shard', {"ItemInitialStockTime": self.shardCD.text()})
        self.IT.UpdateItem('item_ward_observer', {"ItemStockMax": self.eyeMax.text(), "ItemStockInitial": self.eyeInit.text(), "ItemStockTime": self.eyeCD.text()})
        self.IT.UpdateItem('item_ward_sentry', {"ItemStockMax": self.eye2Max.text(), "ItemStockInitial": self.eye2Init.text(), "ItemStockTime": self.eye2CD.text()})
        self.status.setText(f'物品数据已更新')

    def ResetItem(self):
        self.IT.Reset()
        self.status.setText(f'物品数据已重置')

    def Vpk(self):
        self.UN.Write(self.un_out)
        self.NI.Write(self.ni_out)
        self.IT.Write(self.it_out)
        time.sleep(1)
        subprocess.run(self.vpk, shell=True)
        self.status.setText(f'数据已写入VPK')

    def UpdateUn(self):
        self.UN.UpdateXP(self.unXP.text())
        self.UN.UpdateGold(self.unGold.text())
        self.UN.UpdateTowerHpAndRegen(self.unTowerHp.text(), self.unTowerRegen.text())
        self.UN.UpdateFortHpAndRegen(self.unFortHp.text(), self.unFortRegen.text())
        self.status.setText(f'单位数据已更新')

    def ResetUn(self):
        self.UN.Reset()
        self.status.setText(f'单位数据已重置')

    def UpdateNI(self):
        times = [self.ni6.text(),
                 self.ni1.text(),
                 self.ni2.text(),
                 self.ni3.text(),
                 self.ni4.text(),
                 self.ni5.text()]
        self.NI.UpdateNeutralItem(times)
        self.status.setText(f'中立物品数据已更新')

    def ResetNI(self):
        self.NI.Reset()
        self.NI.Write(self.ni_out)
        self.status.setText(f'中立物品数据已重置')

    def SaveConfig(self):
        self.config['GamePath'] = self.gamePath.text()
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)
        self.status.setText(f'路径已保存')

    def Browse(self):
        path = QFileDialog.getExistingDirectory(self, "选择文件夹", "")
        if path:
            self.gamePath.setText(os.path.abspath(path))


if __name__ == '__main__':
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()
