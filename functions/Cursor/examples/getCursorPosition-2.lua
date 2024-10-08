addEventHandler( "onClientRender", root,
    function()
        if isCursorShowing() then
            local screenx, screeny, worldx, worldy, worldz = getCursorPosition()
            local px, py, pz = getCameraMatrix()
            local hit, x, y, z, elementHit = processLineOfSight ( px, py, pz, worldx, worldy, worldz )

            if hit then
                dxDrawText( "Cursor at " .. x .. " " .. y .. " " ..  z, 200, 200 )
                if elementHit then
                    dxDrawText( "Hit element " .. getElementType(elementHit), 200, 220 )
                end
            end
        end
    end
)
