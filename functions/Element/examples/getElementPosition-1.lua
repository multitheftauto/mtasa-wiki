function whatsMyPosition()
    -- get the position of local player
    local fX, fY, fZ = getElementPosition(localPlayer);

    -- output it to chat
    outputChatBox("My current position is X: "..fX.." Y: "..fY.." Z: "..fZ);
end
addCommandHandler("pos", whatsMyPosition);