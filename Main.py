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
        self.Path = os.path.dirname(os.path.abspath(__file__))
        self.VpkBatPath = os.path.join(self.Path, 'vpk', 'vpk.bat')
        self.VpkHeroPath = os.path.join(self.Path, 'vpk', 'pak01_dir', 'scripts', 'npc', 'heroes')
        self.NpcPath = os.path.join(self.Path, 'npc', 'heroes')
        self.NeutralItemsTxtPath = os.path.join(self.Path, 'npc', 'neutral_items.txt')
        self.NeutralItemsTxtPathOut = os.path.join(self.Path, 'vpk', 'pak01_dir', 'scripts', 'npc', 'neutral_items.txt')
        self.NpcUnitsTxtPath = os.path.join(self.Path, 'npc', 'npc_units.txt')
        self.NpcUnitsTxtPathOut = os.path.join(self.Path, 'vpk', 'pak01_dir', 'scripts', 'npc', 'npc_units.txt')
        self.ItemsTxtPath = os.path.join(self.Path, 'npc', 'items.txt')
        self.ItemsTxtPathOut = os.path.join(self.Path, 'vpk', 'pak01_dir', 'scripts', 'npc', 'items.txt')
        self.GeneralLuaPath = os.path.join(self.Path, 'general.lua')
        self.GeneralLuaPathOut = os.path.join(self.Path, 'general_2.lua')
        self.NpcNeutralItem = NpcNeutralItem(self.NeutralItemsTxtPath)
        self.NpcUnit = NpcUnit(self.NpcUnitsTxtPath)
        self.NpcItem = NpcItem(self.ItemsTxtPath)
        self.GeneralLua = GeneralLua(self.GeneralLuaPath)
        self.TeamHeroModel = QStringListModel()
        self.TeamBanModel = QStringListModel()
        self.BrowseModel = QStringListModel()
        self.SelectModel = QStringListModel()
        self.GeneralLuaBanHeroList = []
        self.GeneralLuaTeamList = []
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
        self.Play_Sounds.setText(self.config.get('Play_Sounds')) if self.config.get('Play_Sounds') else None
        self.Player_Death_Sound.setText(self.config.get('Player_Death_Sound')) if self.config.get('Player_Death_Sound') else None
        self.GeneralLuaBanHeroList = self.config.get('BanList') if self.config.get('BanList') else []
        self.GeneralLuaTeamList = self.config.get('Team') if self.config.get('Team') else []
        # 控件配置
        self.setWindowTitle('DOTA修改工具')
        self.status.setText(f'当前版本：{version}')
        self.niApply.clicked.connect(self.UpdateNpcNeutralItem)
        self.niReset.clicked.connect(self.ResetNpcNeutralItem)
        self.save.clicked.connect(self.SaveGamePathConfig)
        self.browse.clicked.connect(self.BrowseFileDir)
        self.unApply.clicked.connect(self.UpdateNpcUnit)
        self.unReset.clicked.connect(self.ResetNpcUnit)
        self.itApply.clicked.connect(self.UpdateItem)
        self.itReset.clicked.connect(self.ResetItem)
        self.luaWrite.clicked.connect(self.WriteLuaConfig)
        self.VPK.clicked.connect(self.Vpk)
        self.TeamHeroModel.setStringList([f'{en:50}{cn}' for en, cn in EN_CN.items()])
        self.heroView.setModel(self.TeamHeroModel)
        self.heroView.setEditTriggers(QListView.NoEditTriggers)  # 禁止编辑
        self.heroView.doubleClicked.connect(self.DoubleClickedHeroView)
        self.TeamBanModel.setStringList([f'{en:50}{EN_CN.get(en)}' for en in self.GeneralLuaBanHeroList])
        self.banView.setModel(self.TeamBanModel)
        self.banView.setEditTriggers(QListView.NoEditTriggers)  # 禁止编辑
        self.banView.doubleClicked.connect(self.DoubleClickedBanView)
        self.BrowseModel.setStringList([f'{en:50}{cn}' for en, cn in EN_CN.items()])
        self.BrowseView.setModel(self.BrowseModel)
        self.BrowseView.setEditTriggers(QListView.NoEditTriggers)  # 禁止编辑
        self.BrowseView.doubleClicked.connect(self.DoubleClickedBrowseView)
        self.BtnList = [self.Friend1, self.Friend2, self.Friend3, self.Friend4, self.Enemy1, self.Enemy2, self.Enemy3, self.Enemy4, self.Enemy5]
        [Btn.clicked.connect(lambda checked, btn=Btn: self.AddTeam(btn)) for Btn in self.BtnList]  # 这里会传两个参数，checked是布尔值参数（表示按钮是否被选中），b是按钮对象
        [Btn.setText(EN_CN.get(self.GeneralLuaTeamList[i])) for i, Btn in enumerate(self.BtnList)] if self.GeneralLuaTeamList else None
        self.TeamReset.clicked.connect(self.ResetTeam)
        self.luaRead.clicked.connect(self.ReadLuaConfig)
        self.luaOpen.clicked.connect(self.OpenGeneralLua)
        self.SelectView.setModel(self.SelectModel)
        self.SelectView.setEditTriggers(QListView.NoEditTriggers)  # 禁止编辑
        # self.SelectView.doubleClicked.connect(self.DoubleClickedBrowseView)
        self.UpdateSelectedModel()

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
        self.config['BanList'] = self.GeneralLuaBanHeroList
        self.config['Team'] = [CN_EN.get(btn.text()) if btn.text() else '' for btn in self.BtnList]
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

    def UpdateSelectedModel(self):
        self.SelectModel.setStringList([f'{FILE_EN.get(f):20}{FILE_CN.get(f)}' for f in os.listdir(self.VpkHeroPath)])

    def OpenGeneralLua(self):
        if os.path.exists(self.GeneralLuaPathOut):
            os.startfile(self.GeneralLuaPathOut)
            time.sleep(1)
            self.status.setText('general.lua已打开')
        else:
            self.status.setText('general.lua未找到')

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
        self.GeneralLuaBanHeroList = self.config.get('BanList') if self.config.get('BanList') else []
        self.GeneralLuaTeamList = self.config.get('Team') if self.config.get('Team') else []
        self.TeamBanModel.setStringList([f'{en:50}{EN_CN[en]}' for en in self.GeneralLuaBanHeroList])
        [Btn.setText(EN_CN.get(self.GeneralLuaTeamList[i])) for i, Btn in enumerate(self.BtnList)] if self.GeneralLuaTeamList else None
        self.status.setText('Lua配置已读取')

    def WriteLuaConfig(self):
        self.GeneralLua.UndateOption('Customize.Localization', f'"{self.Localization.text()}"')
        self.GeneralLua.UndateOption('Customize.Weak_Hero_Cap', self.Weak_Hero_Cap.text())
        self.GeneralLua.UndateOption('Customize.Allow_Trash_Talk', self.Allow_Trash_Talk.text())
        self.GeneralLua.UndateOption('Customize.Force_Group_Push_Level', self.Force_Group_Push_Level.text())
        self.GeneralLua.UndateOption('Default_Difficulty', self.Default_Difficulty.text())
        self.GeneralLua.UndateOption('Default_Ally_Scale', self.Default_Ally_Scale.text())
        self.GeneralLua.UndateOption('Allow_To_Vote', self.Allow_To_Vote.text())
        self.GeneralLua.UndateOption('Play_Sounds', self.Play_Sounds.text())
        self.GeneralLua.UndateOption('Player_Death_Sound', self.Player_Death_Sound.text())
        self.GeneralLua.UpdateBanHero([EN_FULL.get(en) for en in self.GeneralLuaBanHeroList])
        self.GeneralLua.UpdateFriend([CN_FULL.get(btn.text()) if btn.text() else 'Random' for btn in self.BtnList][:4])
        self.GeneralLua.UpdateEnemy([CN_FULL.get(btn.text()) if btn.text() else 'Random' for btn in self.BtnList][4:])
        self.GeneralLua.Write(self.GeneralLuaPathOut)
        self.status.setText(f'Lua配置已写入')

    def ResetTeam(self):
        [Btn.setText('') for Btn in self.BtnList]
        self.status.setText(f'阵容已重置')

    def AddTeam(self, btn):
        index = self.heroView.selectedIndexes()
        if index:
            cho = self.TeamHeroModel.stringList()[index[0].row()].split(' ')[0]
            btn.setText(EN_CN[cho])
            self.status.setText(f'添加：{EN_CN[cho]}')
        else:
            self.status.setText('未选中')

    def DoubleClickedBrowseView(self, index):
        cho = self.BrowseModel.stringList()[index.row()].split(' ')[0]
        self.status.setText(f'添加：{EN_CN[cho]}')

    def DoubleClickedHeroView(self, index):
        cho = self.TeamHeroModel.stringList()[index.row()].split(' ')[0]
        if cho not in self.GeneralLuaBanHeroList:
            self.GeneralLuaBanHeroList.append(cho)
            self.TeamBanModel.setStringList([f'{en:50}{EN_CN[en]}' for en in self.GeneralLuaBanHeroList])
            self.status.setText(f'禁用：{EN_CN[cho]}')
        else:
            self.status.setText(f'已禁用：{EN_CN[cho]}')

    def DoubleClickedBanView(self, index):
        cho = self.TeamBanModel.stringList()[index.row()].split(' ')[0]
        if cho in self.GeneralLuaBanHeroList:
            self.GeneralLuaBanHeroList.remove(cho)
            self.TeamBanModel.setStringList([f'{en:50}{EN_CN[en]}' for en in self.GeneralLuaBanHeroList])
            self.status.setText(f'解禁：{EN_CN[cho]}')

    def UpdateItem(self):
        self.NpcItem.UpdateItem('item_aghanims_shard', {"ItemInitialStockTime": self.shardCD.text()})
        self.NpcItem.UpdateItem('item_ward_observer', {"ItemStockMax": self.eyeMax.text(), "ItemStockInitial": self.eyeInit.text(), "ItemStockTime": self.eyeCD.text()})
        self.NpcItem.UpdateItem('item_ward_sentry', {"ItemStockMax": self.eye2Max.text(), "ItemStockInitial": self.eye2Init.text(), "ItemStockTime": self.eye2CD.text()})
        self.status.setText(f'物品数据已更新')

    def ResetItem(self):
        self.NpcItem.Reset()
        self.status.setText(f'物品数据已重置')

    def Vpk(self):
        self.NpcUnit.Write(self.NpcUnitsTxtPathOut)
        self.NpcNeutralItem.Write(self.NeutralItemsTxtPathOut)
        self.NpcItem.Write(self.ItemsTxtPathOut)
        time.sleep(1)
        subprocess.run(self.VpkBatPath, shell=True)
        self.status.setText(f'数据已写入VPK')

    def UpdateNpcUnit(self):
        self.NpcUnit.UpdateXP(self.unXP.text())
        self.NpcUnit.UpdateGold(self.unGold.text())
        self.NpcUnit.UpdateTowerHpAndRegen(self.unTowerHp.text(), self.unTowerRegen.text())
        self.NpcUnit.UpdateFortHpAndRegen(self.unFortHp.text(), self.unFortRegen.text())
        self.status.setText(f'单位数据已更新')

    def ResetNpcUnit(self):
        self.NpcUnit.Reset()
        self.status.setText(f'单位数据已重置')

    def UpdateNpcNeutralItem(self):
        times = [self.ni6.text(),
                 self.ni1.text(),
                 self.ni2.text(),
                 self.ni3.text(),
                 self.ni4.text(),
                 self.ni5.text()]
        self.NpcNeutralItem.UpdateNeutralItem(times)
        self.status.setText(f'中立物品数据已更新')

    def ResetNpcNeutralItem(self):
        self.NpcNeutralItem.Reset()
        self.NpcNeutralItem.Write(self.NeutralItemsTxtPathOut)
        self.status.setText(f'中立物品数据已重置')

    def SaveGamePathConfig(self):
        self.config['GamePath'] = self.gamePath.text()
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)
        self.status.setText(f'路径已保存')

    def BrowseFileDir(self):
        path = QFileDialog.getExistingDirectory(self, "选择文件夹", "")
        if path:
            self.gamePath.setText(os.path.abspath(path))


if __name__ == '__main__':
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()
