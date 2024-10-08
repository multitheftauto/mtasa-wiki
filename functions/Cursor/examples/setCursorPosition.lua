function centerCursorFunction()
    local showing = isCursorShowing ()
    if showing then -- if the cursor is showing
        local screenX, screenY = guiGetScreenSize () --get the screen size in pixels
        setCursorPosition (screenX/2, screenY/2) --set the cursor position to the center of the screen
    else
        outputChatBox( "Your cursor is not showing." )
    end
end
addCommandHandler( "cursorpos", centerCursorFunction )
