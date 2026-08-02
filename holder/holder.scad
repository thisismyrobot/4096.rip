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

module slot() {
    translate([turnerWidth/2, slotLift, -slotDepth]) cube([slotWidth, slotLength, slotDepth + 1]);
}

module slots() {
    slot();
    mirror([1, 0, 0]) slot();
}

module turner() {
    translate([-turnerWidth/2, 0, 0]) cube([turnerWidth, turnerHeight, turnerDepth]);
    translate([-turnerWidth/2, slotLift, 0]) cube([turnerWidth, slotLength, bowCover]);
}

module bow() {
    minkowski() {
        translate([-bladeWidth/2, 0, -bowLength]) cube([bladeWidth, slotLength + slotLift, bowLength]);
        cylinder(d=bowPad*2, h=0.00001, $fn=20);
    }
}

difference() {
    bow();
    slots();
}
turner();
