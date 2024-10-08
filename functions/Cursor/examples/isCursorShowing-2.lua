function outputCursor(playerElement)
    if playerElement and isElement(playerElement) then -- Check whether the given element exists
        local cursorState = isCursorShowing(playerElement) -- Retrieve the state of the player's cursor
        local cursorStateText = cursorState and "visible" or "hidden" -- Calculate the context from the boolean variable.

        outputChatBox("Your cursor is " .. cursorStateText .. ".", playerElement) -- Output the text in the chatbox according to the cursor state.
    end
end
