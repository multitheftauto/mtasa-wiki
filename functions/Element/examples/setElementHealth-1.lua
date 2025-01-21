function setMyHealth(uPlayer, strCommand, fAmount)
    -- safety check if we got a valid new health value
    local fAmount = tonumber(fAmount);

    if(not fAmount) then
        return outputChatBox("Invalid health value entered!", uPlayer, 255, 0, 0);
    end

    -- change the player's health
    setElementHealth(uPlayer, fAmount);
    outputChatBox("Your health was set to "..fAmount.." HP!", uPlayer, 0, 255, 0);
end
addCommandHandler("sethealth", setMyHealth)