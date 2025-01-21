function healMePlease()
    -- heal the player if health is 50 or lower
    if(getElementHealth(localPlayer) <= 50) then
        setElementHealth(localPlayer, 100);
        outputChatBox("You got healed!");
    end
end
addCommandHandler("healme", healMePlease);