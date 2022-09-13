-- Include necessary socket modules using a hack

console.log('start')
local version = _VERSION:match("%d+%.%d+")
console.log(version)
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
-- console.log('requiring')

-- local HOST, PORT = "DESKTOP-DL0JINT", 4321
local CHOST, CPORT = "localhost", 1234
-- local socket = require("socket")

-- -- Create the client and initial connection
-- console.log('binding/connecting')
-- -- s = socket.bind(HOST, PORT)
-- local client, err = socket.connect(CHOST, CPORT)

-- -- Attempt to ping the server once a second
-- console.log('receiving')
-- local res = client:receive()
-- console.log(res)


-- local HOST, PORT = "localhost", 9999
local socket = require('socket')
local tcp = assert(socket.tcp())
tcp:settimeout(0.01)
-- console.log(tcp)
tcp:connect(CHOST, CPORT)
tcp:send('connect')
local s, status, partial = tcp:receive('*l')
console.log('s')
console.log(type(s))
console.log('status')
console.log(status)
console.log('partial')
console.log(partial)
tcp:close()


---
-- -- Create the client and initial connection
-- client, err = socket.connect(CHOST, CPORT)
-- -- Attempt to ping the server once a second
-- -- Receive data from the server and print out everything
-- console.log(client:getsockname())
-- s, status, partial = client:receive(1)
-- console.log(s)
-- console.log(status)
-- console.log(partial)
-- client:close()
-- client:shutdown()
