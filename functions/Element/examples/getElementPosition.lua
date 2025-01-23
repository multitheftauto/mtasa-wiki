-- Create the elegy
local myElegy = createVehicle(562, 1591.596680, -2495.323242, 18.098244)
-- Get the vehicle's position
local x, y, z = getElementPosition(myElegy)
-- Create the samsite
local samsite = createObject(3267, x, y, z + 3)
-- Attach the samsite to the elegy
attachElements(samsite, myElegy)
