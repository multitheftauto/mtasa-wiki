function cursorInfo()
    -- is the cursor showing?
    if isCursorShowing() then
        -- get the cursor postion
        local screenx, screeny, worldx, worldy, worldz = getCursorPosition()

        -- make the accuracy of floats 4 decimals and print to chatbox
        outputChatBox( string.format( "Cursor screen position (relative): X=%.4f Y=%.4f", screenx, screeny ) )
        outputChatBox( string.format( "Cursor world position: X=%.4f Y=%.4f Z=%.4f", worldx, worldy, worldz ) )
    else
        outputChatBox( "Your cursor is not showing." )
    end
end
addCommandHandler( "cursorpos", cursorInfo )
