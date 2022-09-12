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


-- importing HTTP package
local http = require("http")

-- making HTTP call
response, err = http.request("GET", "https://example.com")
if err then error(err) end

-- parsing response body from the API
local api_response, err = json.decode(response.body)
if err then error(err) end
