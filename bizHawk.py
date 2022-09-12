from bizhook import Memory

combined_wram = Memory('Combined WRAM')


class gameData:

    def __init__(self):
        self.memory = combined_wram
        self.player = self.getPlayerPos()
        self.tiles = self.getTiles()
        self.sprites = self.getAllSprites()

    def getPlayerPos(self):
        print('lol', )
        x = Memory('wram').read_s16_le(0x94)
        print(x)
        y = self.memory.read_s16_le(0x96)
        print(x, y)
        return x, y

    def getTiles(self):
        plX, plY = self.player

        for dy in range(10):
            for dx in range(10):
                x = (plX + dx + 8) // 16
                y = (plY + dy) // 16

                return self.memory.read_byte(0x1C800 + x // 0x10 * 0x1B0 + y * 0x10 + x % 0x10)

    def getSprites(self):
        pass

    def getExtSprites(self):
        pass

    def getAllSprites(self):
        pass


print('lol')
d = gameData()
print(d)
