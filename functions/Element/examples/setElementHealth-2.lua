function repairMyVehicle()
    -- check if we are in a vehicle
    local uVehicle = getPedOccupiedVehicle(localPlayer);

    if(uVehicle) then
        -- does our vehicle need repair? remember, vehicle health ranges from 0 to 1000
        if(getElementHealth(uVehicle) < 1000) then
            -- note: setElementHealth does not repair the visual aspect of vehicles, use fixVehicle instead!
            setElementHealth(uVehicle, 1000);
        else
            outputChatBox("Your vehicle is already at full health!", 255, 0, 0);
        end
    else
        outputChatBox("You are not in a vehicle!", 255, 0, 0);
    end
end
addCommandHandler("repairvehicle", repairMyVehicle);