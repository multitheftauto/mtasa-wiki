addCommandHandler( "cursoralpha", 
    function ()
        -- check if cursor is showing
        if ( isCursorShowing ( ) ) then
            outputChatBox( "The cursor alpha: "..getCursorAlpha( ) )
        else
            outputChatBox( "The cursor is not showing!" )
        end
    end
)
