include <threads.scad>;

mm = 1;

slop = 0.4*mm;

pen_rad = 8.2*mm + slop;
wall = 1.5*mm;
chuck_len = 20*mm;

num_fingers = 8;
finger_extend =0.3*mm;
base_rad = 15*mm;
eps = 0.01;
nut_th = 3*wall;

difference(){
    union(){
        cylinder(r=pen_rad+wall, h=chuck_len);
        translate([0,0,wall])
        metric_thread(angle=50, length=chuck_len*0.6, pitch=2, diameter = 2*pen_rad+4*wall);
        cylinder(r=base_rad, h=wall);
        
    }
    union(){
        translate([0,0,-chuck_len/2])
        cylinder(r1=pen_rad, r2 = pen_rad - finger_extend, h=2*chuck_len);
        for(i=[0:num_fingers-1]) {
            rotate([0,0,360/num_fingers*i])
            translate([0,-wall/2,wall+eps])
            cube([2*pen_rad, wall, chuck_len]);
        }
        
    }
}

!translate([30,0,0])
difference(){
    cylinder(r=pen_rad+4*wall, h=nut_th);
    translate([0,0,-wall/2])
    metric_thread(angle=50, pitch=2, length=wall+nut_th, diameter = 2*pen_rad+4*wall+3*slop, internal=true);
        
}

