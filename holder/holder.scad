bladeWidth = 4.2;

slotWidth = 1.05;
slotLength = 11;
slotDepth = 9.2;
slotLift = 0.5;

turnerWidth = bladeWidth - slotWidth * 2;
turnerHeight = slotWidth;
turnerDepth = 4;

bowLength = 15;
bowPad = 3;
bowCover = 0.8;

stubLength = 1.5;
stubWidth = 1.75;
stubHeight = 1;
stubCentreLine = 3.5; // Above bottom of turner stub
stubSlotHeight = 1.28;

module slot() {
    translate([turnerWidth/2, slotLift, -slotDepth]) cube([slotWidth, slotLength, slotDepth + 1]);
}

module slots() {
    slot();
    mirror([1, 0, 0]) slot();
}

module turner() {
    translate([-turnerWidth/2, 0, 0]) cube([turnerWidth, turnerHeight, turnerDepth]);
    translate([-turnerWidth/2, 1.5, -0.75]) rotate([45, 0, 0]) cube([turnerWidth, turnerHeight, 2]);
}

module bow() {
    minkowski() {
        translate([-bladeWidth/2, 0, -bowLength]) cube([bladeWidth, slotLength + slotLift, bowLength]);
        cylinder(d=bowPad*2, h=0.00001, $fn=20);
    }
}

module stubs() {
    // Lower
    translate([slotWidth+turnerWidth/2, stubCentreLine - (stubSlotHeight + stubHeight)/2, 0]) cube([stubWidth, stubHeight, stubLength]);
    translate([-slotWidth-turnerWidth/2-stubWidth, stubCentreLine - (stubSlotHeight + stubHeight)/2, 0]) cube([stubWidth, stubHeight, stubLength]);

    // Upper.
    translate([slotWidth+turnerWidth/2, stubCentreLine + (stubSlotHeight - stubHeight)/2, 0]) cube([stubWidth, stubHeight, stubLength]);
    translate([-slotWidth-turnerWidth/2-stubWidth, stubCentreLine + (stubSlotHeight - stubHeight)/2, 0]) cube([stubWidth, stubHeight, stubLength]);
}

difference() {
    bow();
    slots();
}
turner();
stubs();
