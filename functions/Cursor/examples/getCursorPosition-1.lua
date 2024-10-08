function cursorInfo()
    if isCursorShowing() then -- if the cursor is showing
        local screenx, screeny, worldx, worldy, worldz = getCursorPosition()

        outputChatBox( string.format( "Cursor screen position (relative): X=%.4f Y=%.4f", screenx, screeny ) ) -- make the accuracy of floats 4 decimals
        outputChatBox( string.format( "Cursor world position: X=%.4f Y=%.4f Z=%.4f", worldx, worldy, worldz ) ) -- make the accuracy of floats 4 decimals accurate
    else
        outputChatBox( "Your cursor is not showing." )
    end
end
addCommandHandler( "cursorpos", cursorInfo )
