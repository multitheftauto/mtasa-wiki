function teleportToRandomPlayer(uPlayer)
    -- get a random player (does not exclude the player executing this command!)
    local uRandomPlayer = getRandomPlayer();

    -- get the position of the random player
    local fX, fY, fZ = getElementPosition(uRandomPlayer);

    -- teleport the player to random one with slight offset to not get stuck
    setElementPosition(uPlayer, fX + 2, fY + 2, fZ);
end
addCommandHandler("tprandom", teleportToRandomPlayer);