module protrusion(angle, height) {
    rotate([0, 0, angle])
        translate([CYLINDER_RADIUS, 0, height])
            rotate([0, 90, 0])
                cylinder(h = PROTRUSION_HEIGHT, r = PROTRUSION_RADIUS);
}

module music_box_cylinder() {
    difference () {
        cylinder(h = CYLINDER_HEIGHT, r = CYLINDER_RADIUS);
        translate([0,0,-1])

        cylinder(h = INNER_CYLINDER_HEIGHT, r = INNER_CYLINDER_RADIUS);
    }
    
    for (track = [0 : NUM_TRACKS - 1]) {
        for (i = [0 : TRACK_LENGTH - 1]) {
            if (TRACKS[track][i] == 1) {
                protrusion(i * (360 / TRACK_LENGTH), EDGE_OFFSET + track * (TRACK_TO_TRACK_DISTANCE));
            }
        }
    }
}

music_box_cylinder();