addCommandHandler( "cursoralpha", 
    function ()
        -- Show the cursor if it is not showing or hide the cursor if it is
        showCursor( not isCursorShowing ( ) )
        
        -- Set the alpha to 100
        setCursorAlpha(100)
    end
)
