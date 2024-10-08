-- Simple command to test the getCursorAlpha function
addCommandHandler( "cursorAlpha", 
    function ()
        if ( isCursorShowing ( ) ) then
            outputChatBox( "The cursor alpha: "..getCursorAlpha( ) )
        else
            outputChatBox( "The cursor is not showing!" )
        end
    end
)
