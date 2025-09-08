import json
import os
import subprocess
import time

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

from NpcItem import NpcItem
from NpcNeutralItem import NpcNeutralItem
from NpcUnit import NpcUnit
from GeneralLua import GeneralLua
from untitled import Ui_Form

version = '0.0.1'


class MainWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        if os.path.exists('config.json'):
            with open('config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {}
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.vpk = os.path.join(self.path, 'vpk', 'vpk.bat')
        self.ni = os.path.join(self.path, 'npc', 'neutral_items.txt')
        self.ni_out = os.path.join(self.path, 'vpk', 'pak01_dir', 'scripts', 'npc', 'neutral_items.txt')
        self.un = os.path.join(self.path, 'npc', 'npc_units.txt')
        self.un_out = os.path.join(self.path, 'vpk', 'pak01_dir', 'scripts', 'npc', 'npc_units.txt')
        self.it = os.path.join(self.path, 'npc', 'items.txt')
        self.it_out = os.path.join(self.path, 'vpk', 'pak01_dir', 'scripts', 'npc', 'items.txt')
        self.lua = os.path.join(self.path, 'general.lua')
        self.NI = NpcNeutralItem(self.ni)
        self.UN = NpcUnit(self.un)
        self.IT = NpcItem(self.it)
        self.LUA = GeneralLua(self.lua)
        self.setupUi(self)
        self.Init()

    def Init(self):
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
        self.luaWrite.clicked.connect(self.WriteLua)
        self.VPK.clicked.connect(self.Vpk)
        # 读取配置
        try:
            self.gamePath.setText(self.config['GamePath'])
            self.ni1.setText(self.config['Time'][0])
            self.ni2.setText(self.config['Time'][1])
            self.ni3.setText(self.config['Time'][2])
            self.ni4.setText(self.config['Time'][3])
            self.ni5.setText(self.config['Time'][4])
            self.ni6.setText(self.config['Time'][5])
            self.unXP.setText(self.config['unXP'])
            self.unGold.setText(self.config['unGold'])
            self.unTowerHp.setText(self.config['unTowerHp'])
            self.unTowerRegen.setText(self.config['unTowerRegen'])
            self.unFortHp.setText(self.config['unFortHp'])
            self.unFortRegen.setText(self.config['unFortRegen'])
            self.shardCD.setText(self.config['shardCD'])
            self.eyeMax.setText(self.config['eyeMax'])
            self.eyeInit.setText(self.config['eyeInit'])
            self.eye2Max.setText(self.config['eye2Max'])
            self.eye2Init.setText(self.config['eye2Init'])
            self.eyeCD.setText(self.config['eyeCD'])
            self.eye2CD.setText(self.config['eye2CD'])
        except Exception as e:
            self.status.setText(f'配置文件错误：{e}')

    def closeEvent(self, event):
        self.config['GamePath'] = self.gamePath.text()
        times = [self.ni1.text(),
                 self.ni2.text(),
                 self.ni3.text(),
                 self.ni4.text(),
                 self.ni5.text(),
                 self.ni6.text()]
        self.config['Time'] = times
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
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

    def WriteLua(self):
        self.LUA.UndateOption('Customize.Localization', self.Localization.text())
        self.LUA.UndateOption('Customize.Weak_Hero_Cap', self.Weak_Hero_Cap.text())
        self.LUA.UndateOption('Customize.Allow_Trash_Talk', self.Allow_Trash_Talk.text())
        self.LUA.UndateOption('Customize.Force_Group_Push_Level', self.Force_Group_Push_Level.text())
        self.LUA.UndateOption('Default_Difficulty', self.Default_Difficulty.text())
        self.LUA.UndateOption('Default_Ally_Scale', self.Default_Ally_Scale.text())
        self.LUA.UpdateBanHero(['BanHero1', 'BanHero2', 'BanHero3'])
        self.LUA.UpdateFriend(['Friend1', 'Friend2', 'Friend3', 'Friend4'])
        self.LUA.UpdateEnemy(['Enemy1', 'Enemy2', 'Enemy3', 'Enemy4', 'Enemy5'])
        self.LUA.Write(r'C:\Users\Jeremy\Desktop\d3\general_2.lua')
        self.status.setText(f'阵容数据已写入')

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
        self.status.setText(f'配置已保存')

    def Browse(self):
        path = QFileDialog.getExistingDirectory(self, "选择文件夹", "")
        if path:
            self.gamePath.setText(os.path.abspath(path))


if __name__ == '__main__':
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()
