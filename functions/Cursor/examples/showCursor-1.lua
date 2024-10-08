local thePlayer = getPlayerFromName ( "Dave" )              -- get the player named Dave
if thePlayer then                                           -- if we got him
    showCursor ( thePlayer, true )                          -- make his cursor show
    if isCursorShowing ( thePlayer ) then                   -- did it show?
        outputChatBox ( "Cursor is now showing for Dave." ) -- print a message to the chat box
    end
end
