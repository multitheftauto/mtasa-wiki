function randomPlayersToLocation(p)
	local playersOnline = getElementsByType("player")
	local amount = #playersOnline

	if amount == 0 then return end

	for index = 1,(amount > 5 and 5 or amount) do
		local player = playersOnline[index]
		setElementPosition(player, getElementPosition(p))
	end
end
addCommandHandler("tprandomplayers", randomPlayersToLocation)
