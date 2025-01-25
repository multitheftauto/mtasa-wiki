function teleportPlayerToMapCenter()
    -- teleport player to 0,0,0 coordinates (map origin/center)
    setElementPosition(localPlayer, 0, 0, 0 + 3);	-- add +3 to z coordinate to not fall below map!
end
addCommandHandler("zero", teleportPlayerToMapCenter);