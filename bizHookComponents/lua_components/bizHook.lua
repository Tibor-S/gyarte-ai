--- CONSTANTS

local BoxRadius = 6
local InputSize = (BoxRadius * 2 + 1) * (BoxRadius * 2 + 1)
local CHOST, CPORT = "localhost", 9999
local Inputs = InputSize + 1
local memory = memory
local console = console
local gui = gui
local event = event
local emu = emu

--- SET UP PACKETS AND SOCKET

local version = _VERSION:match("%d+%.%d+")
package.path = 'lua_modules/share/lua/'
    .. version
    .. '/?.lua;lua_modules/share/lua/'
    .. version
    .. '/?/init.lua;'
    .. package.path

package.cpath = 'lua_modules/lib/lua/'
    .. version
    .. '/?.so;'
    .. package.cpath

--- FUNCTIONS

local function connectSocket()
  local socket = require('socket')
  tcp = assert(socket.tcp())
  tcp:settimeout(0.01)
  -- console.log(tcp)
  tcp:connect(CHOST, CPORT)
  -- console.log('SOCKET CONNECTED TO: ' .. tcp:getsockname())
end

local function disconnectSocket()
  tcp:close()
end

local function sendBitmap(tbl)
  local s = ''
  for i = 1, #tbl do
    s = s .. tostring(tbl[i])
  end
  -- console.log('SENDING:')
  -- console.log(s)
  tcp:send(s)
end

local function recvActions()
  -- console.log('RECEIVING:')
  local s, status, partial = tcp:receive('*l')
  -- console.log('DATA: ' .. tostring(s))
  -- console.log('STATUS: ' .. tostring(status))
  -- console.log('PARTIAL: ' .. tostring(partial))
  local tbl = {}
  tbl['u'] = tonumber(partial[1])
  tbl['r'] = tonumber(partial[2])
  tbl['d'] = tonumber(partial[3])
  tbl['l'] = tonumber(partial[4])
  tbl['a'] = tonumber(partial[5])
  tbl['b'] = tonumber(partial[6])
  tbl['x'] = tonumber(partial[7])
  return tbl
end

local function getPositions()
  marioX = memory.read_s16_le(0x94)
  marioY = memory.read_s16_le(0x96)
end

local function getTile(dx, dy)
  local x = math.floor((marioX + dx + 8) / 16)
  local y = math.floor((marioY + dy) / 16)

  return memory.readbyte(0x1C800 + math.floor(x / 0x10) * 0x1B0 + y * 0x10 + x % 0x10)
end

local function getSprites()
  local sprites = {}
  for slot = 0, 11 do
    local status = memory.readbyte(0x14C8 + slot)
    if status ~= 0 then
      local spritex = memory.readbyte(0xE4 + slot) + memory.readbyte(0x14E0 + slot) * 256
      local spritey = memory.readbyte(0xD8 + slot) + memory.readbyte(0x14D4 + slot) * 256
      sprites[#sprites + 1] = { ["x"] = spritex, ["y"] = spritey }
    end
  end
  return sprites
end

local function getExtendedSprites()
  local extended = {}
  for slot = 0, 11 do
    local number = memory.readbyte(0x170B + slot)
    if number ~= 0 then
      local spritex = memory.readbyte(0x171F + slot) + memory.readbyte(0x1733 + slot) * 256
      local spritey = memory.readbyte(0x1715 + slot) + memory.readbyte(0x1729 + slot) * 256
      extended[#extended + 1] = { ["x"] = spritex, ["y"] = spritey }
    end
  end

  return extended
end

local function getInputs()
  -- local marioX, marioY =
  getPositions()
  local sprites = getSprites()
  local extended = getExtendedSprites()
  local inputs = {}

  for dy = -BoxRadius * 16, BoxRadius * 16, 16 do
    for dx = -BoxRadius * 16, BoxRadius * 16, 16 do
      inputs[#inputs + 1] = 0

      local tile = getTile(dx, dy)
      if tile == 1 and marioY + dy < 0x1B0 then
        inputs[#inputs] = 1
      end

      for i = 1, #sprites do
        local distx = math.abs(sprites[i]["x"] - (marioX + dx))
        local disty = math.abs(sprites[i]["y"] - (marioY + dy))
        if distx <= 8 and disty <= 8 then
          inputs[#inputs] = 2
        end
      end

      for i = 1, #extended do
        local distx = math.abs(extended[i]["x"] - (marioX + dx))
        local disty = math.abs(extended[i]["y"] - (marioY + dy))
        if distx < 8 and disty < 8 then
          inputs[#inputs] = 2
        end
      end
    end
  end
  return inputs
end

local function loop()
  local inps = getInputs()
  local s = '' .. tostring(marioX) .. ', ' .. tostring(marioY) .. '\n'
  for y = 0, 12 do
    for x = 1, 13 do
      -- console.log('lol')
      -- console.log(13 * y + x)
      -- console.log(inps[13 * y + x])

      s = s .. string.lpad(tostring(inps[13 * y + x]), 2) .. '|'
    end
    s = s .. '\n'
  end
  gui.text(50, 50, s)
  -- console.log(tostring(inps))
  connectSocket()
  sendBitmap(inps)
  recvActions()
  disconnectSocket()

end

string.lpad = function(str, len, char)
  if char == nil then char = ' ' end
  return str .. string.rep(char, len - #str)
end

console.log(InputSize - 1)

-- for x = 0, Inputs + 1, 1 do
--   console.log(x)
--   console.log(inps[x])
-- end
event.onframestart(loop)
