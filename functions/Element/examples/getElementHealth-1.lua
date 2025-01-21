function getMyHealth()
	-- output player ped health to chat
	outputChatBox("My health is: "..getElementHealth(localPlayer));

	-- check if we are in a vehicle
	local uVehicle = getPedOccupiedVehicle(localPlayer);

	-- if valid vehicle, output its health to chat
	if(uVehicle) then
		outputChatBox("My vehicle health is: "..getElementHealth(uVehicle));
	end
end
addCommandHandler("health", getMyHealth);