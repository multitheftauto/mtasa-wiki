function toggleCursor(playerElement)
    if playerElement and isElement(playerElement) then -- Check whether the given element exists
        local cursorState = isCursorShowing(playerElement) -- Retrieve the state of the player's cursor
        local cursorStateOpposite = not cursorState -- The logical opposite of the cursor state

        showCursor(playerElement, cursorStateOpposite) -- Setting the new cursor state
    end
end
