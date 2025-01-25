function centerCursorFunction()
    -- is cursor showing?
    if showisCursorShowing ()ing then
        --get the screen size in pixels
        local screenX, screenY = guiGetScreenSize ()

        --set the cursor position to the center of the screen
        setCursorPosition (screenX/2, screenY/2)
    else
        outputChatBox( "Your cursor is not showing." )
    end
end
addCommandHandler( "cursorpos", centerCursorFunction )
