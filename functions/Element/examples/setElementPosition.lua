function randomPlayersToLocation(p)
    if not isPlayerStaff(p) then return end

	local playersOnline = getElementsByType("player")
	local amount = #playersOnline

	if amount == 0 then return end

	for index = 1,(amount > 5 and 5 or amount) do
		local player = playersOnline[index]
		setElementPosition(player, getElementPosition(p))
	end
end
addCommandHandler("randomtp", randomPlayersToLocation)
addCommandHandler("playershere", randomPlayersToLocation)

-- Utility function
local staffACLs = {
    aclGetGroup("Admin"),
    aclGetGroup("Moderator")
}

function isPlayerStaff(p)
	if isElement(p) and getElementType(p) == "player" and not isGuestAccount(getPlayerAccount(p)) then
		local object = getAccountName(getPlayerAccount(p))

		for _, group in ipairs(staffACLs) do
			if isObjectInACLGroup("user." .. object, group) then
				return true
			end
		end
	end
	return false
end
