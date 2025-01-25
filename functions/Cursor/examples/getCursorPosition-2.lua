addEventHandler( "onClientRender", root,
    function()
        -- is cursor showing?
        if isCursorShowing() then
            -- get cursor position
            local screenx, screeny, worldx, worldy, worldz = getCursorPosition()

            -- get our camera matrix/position
            local px, py, pz = getCameraMatrix()

            -- calculate the exact distance between cursor and camera
            local hit, x, y, z, elementHit = processLineOfSight ( px, py, pz, worldx, worldy, worldz )

            -- draw the distance on screen
            dxDrawText( "Cursor at X:" .. x .. " Y:" .. y .. " Z:" ..  z, 200, 200 )

            -- if we got a collision detected and a valid element, draw it as well
            if hit and elementHit then
                dxDrawText( "Hit element " .. getElementType(elementHit), 200, 220 )
            end
        end
    end
)
