function teleportMePlease(uPlayer)
    -- get the position from the player executing the command
    local fX, fY, fZ = getElementPosition(uPlayer);

    -- set player position 50 units higher
    setElementPosition(uPlayer, fX, fY, fZ + 50);
end
addCommandHandler("tpme", teleportMePlease);